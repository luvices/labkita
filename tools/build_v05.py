#!/usr/bin/env python3
"""Bangun ISO LabKita Linux 0.5 di WSL/Linux menggunakan resep build bisect #3 (non-Cubic)."""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import subprocess
import sys


def parse_args():
    default_repo = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Build LabKita Linux 0.5 hybrid ISO from official Ubuntu 24.04.5.1 Desktop ISO."
    )
    parser.add_argument("--source-iso", required=True, help="Path to Ubuntu 24.04.5.1 desktop amd64 ISO.")
    parser.add_argument("--output-iso", required=True, help="Destination path for labkita-linux-0.5-amd64.iso.")
    parser.add_argument("--work-dir", default="/var/tmp/labkita-v05", help="Temporary Linux build directory.")
    parser.add_argument("--repo-root", default=str(default_repo), help="Path to labkita-linux repository root.")
    parser.add_argument(
        "--date",
        default=datetime.now(timezone.utc).strftime("%Y%m%d"),
        help="Release date stamp for .disk/info (YYYYMMDD).",
    )
    parser.add_argument("--keep-work", action="store_true", help="Keep temporary work directory after build.")
    return parser.parse_args()


def load_packages(repo_root: Path):
    pkg_file = repo_root / "config/packages.txt"
    pkgs = []
    for line in pkg_file.read_text(encoding="utf-8").splitlines():
        item = line.split("#", 1)[0].strip()
        if item:
            pkgs.append(item)
    if not pkgs:
        raise SystemExit(f"No packages found in {pkg_file}")
    return pkgs


def setup_base_packages_and_locale(min_dir: Path, pkgs):
    pkg_list = " ".join(pkgs)
    chroot_step1 = f"""#!/usr/bin/env bash
set -Eeuo pipefail
export DEBIAN_FRONTEND=noninteractive
cat <<'EOF' > /etc/apt/apt.conf.d/99no-check-valid
Acquire::Check-Valid-Until "false";
EOF
apt-get update
apt-get install -y --no-install-recommends software-properties-common
add-apt-repository -y universe
apt-get update
apt-get install -y --no-install-recommends {pkg_list}

locale-gen id_ID.UTF-8
update-locale LANG=id_ID.UTF-8 LANGUAGE=id_ID:id LC_ALL=id_ID.UTF-8
cat > /etc/default/locale <<'EOF'
LANG="id_ID.UTF-8"
LANGUAGE="id_ID:id"
LC_ALL="id_ID.UTF-8"
EOF

ln -sf /usr/share/zoneinfo/Asia/Jakarta /etc/localtime
echo "Asia/Jakarta" > /etc/timezone

cat > /etc/default/keyboard <<'EOF'
XKBMODEL="pc105"
XKBLAYOUT="us"
XKBVARIANT=""
XKBOPTIONS=""
BACKSPACE="guess"
EOF

apt-get clean
rm -rf /var/lib/apt/lists/* /etc/apt/apt.conf.d/99no-check-valid
"""
    script_path = min_dir / "tmp/v05_step1.sh"
    script_path.write_text(chroot_step1, encoding="utf-8")
    os.chmod(script_path, 0o755)

    mounts = []
    try:
        for mount_rel, opts in [
            ("dev", ["--bind", "/dev"]),
            ("dev/pts", ["--bind", "/dev/pts"]),
            ("proc", ["-t", "proc", "proc"]),
            ("sys", ["-t", "sysfs", "sysfs"]),
        ]:
            target = min_dir / mount_rel
            target.mkdir(parents=True, exist_ok=True)
            subprocess.run(["mount"] + opts + [str(target)], check=True)
            mounts.append(target)

        resolv = min_dir / "etc/resolv.conf"
        if resolv.is_symlink() or resolv.exists():
            resolv.unlink()
        shutil.copyfile("/etc/resolv.conf", resolv)

        print("Running chroot package installation & Indonesian locale configuration...", flush=True)
        subprocess.run(["chroot", str(min_dir), "/tmp/v05_step1.sh"], check=True)
    finally:
        for target in reversed(mounts):
            subprocess.run(["umount", "-lf", str(target)], check=False)

    script_path.unlink(missing_ok=True)
    resolv = min_dir / "etc/resolv.conf"
    if resolv.exists() and not resolv.is_symlink():
        resolv.unlink()
        os.symlink("../run/systemd/resolve/stub-resolv.conf", resolv)


def setup_payload_and_branding(min_dir: Path, repo_root: Path):
    print("Copying payload/. into rootfs...", flush=True)
    subprocess.run(["cp", "-a", f"{repo_root}/payload/.", f"{min_dir}/"], check=True)

    chroot_step2 = """#!/usr/bin/env bash
set -Eeuo pipefail

chmod 0755 /usr/local/bin/labkita-check /usr/local/bin/labkita-guide /usr/local/sbin/labkita-postinstall
find /usr/share/labkita -type d -exec chmod 0755 {} +
find /usr/share/labkita -type f -exec chmod 0644 {} +
chmod 0644 /etc/systemd/system/labkita-runtime.service
chmod 0644 /usr/share/applications/labkita-guide.desktop

if [[ -d /usr/share/themes ]]; then
    find /usr/share/themes -type d -exec chmod 0755 {} +
    find /usr/share/themes -type f -exec chmod 0644 {} +
fi
if [[ -d /usr/share/icons ]]; then
    find /usr/share/icons -type d -exec chmod 0755 {} +
    find /usr/share/icons -type f -exec chmod 0644 {} +
    gtk-update-icon-cache -q -t -f /usr/share/icons/WhiteSur 2>/dev/null || true
    gtk-update-icon-cache -q -t -f /usr/share/icons/WhiteSur-dark 2>/dev/null || true
    gtk-update-icon-cache -q -t -f /usr/share/icons/WhiteSur-light 2>/dev/null || true
fi

cat > /etc/labkita-release <<'EOF'
NAME="LabKita Linux"
VERSION="0.5"
BASE="Ubuntu 24.04 LTS"
PURPOSE="Praktikum pemrograman dasar offline"
EOF
cat > /etc/motd <<'EOF'
LabKita Linux 0.5 | Praktikum pemrograman offline (Bahasa Indonesia)
Panduan: Jalankan 'labkita-guide' atau buka menu 'Panduan LabKita'
Uji kesiapan: labkita-check
Ruang sementara: /run/labkita (RAM disk sementara)
EOF

if [[ -f /usr/lib/os-release ]]; then
    sed -i 's/^PRETTY_NAME=.*/PRETTY_NAME="LabKita Linux 0.5 (Noble Numbat)"/' /usr/lib/os-release
fi
if [[ -f /etc/lsb-release ]]; then
    sed -i 's/^DISTRIB_DESCRIPTION=.*/DISTRIB_DESCRIPTION="LabKita Linux 0.5"/' /etc/lsb-release
fi

install -d -m 0755 /etc/dconf/profile
if [[ ! -f /etc/dconf/profile/user ]]; then
    printf 'user-db:user\\nsystem-db:local\\n' > /etc/dconf/profile/user
elif ! grep -qxF 'system-db:local' /etc/dconf/profile/user; then
    printf '\\nsystem-db:local\\n' >> /etc/dconf/profile/user
fi
dconf update

getent group labkita-praktikum >/dev/null || groupadd --system labkita-praktikum

rm -rf /etc/skel/.local/share/labkita
install -d -m 0755 /etc/skel/Praktikum
cp -a /usr/share/labkita/examples/. /etc/skel/Praktikum/
install -d -m 0755 /etc/skel/Dokumen/Panduan-LabKita
cp -a /usr/share/labkita/guide/. /etc/skel/Dokumen/Panduan-LabKita/

install -d -m 0755 /etc/systemd/system/multi-user.target.wants
ln -sfn /etc/systemd/system/labkita-runtime.service \\
    /etc/systemd/system/multi-user.target.wants/labkita-runtime.service

install -d -m 0755 /usr/share/labkita/build
date -u '+%Y-%m-%dT%H:%M:%SZ' > /usr/share/labkita/build/build-time.txt
cp /etc/os-release /usr/share/labkita/build/base-os-release
dpkg-query -W -f='${binary:Package}\\t${Version}\\n' > /usr/share/labkita/build/packages.tsv
cat > /usr/share/labkita/build/LICENSES.txt <<'EOF'
Lisensi setiap paket tersedia di /usr/share/doc/<nama-paket>/copyright.
Skrip dan aset LabKita berada pada repositori proyek kelompok.
Sertakan sumber dan lisensi upstream dalam laporan dan repositori.
EOF
"""
    script_path = min_dir / "tmp/v05_step2.sh"
    script_path.write_text(chroot_step2, encoding="utf-8")
    os.chmod(script_path, 0o755)
    print("Running chroot branding, dconf, systemd, and labkita-praktikum group setup...", flush=True)
    subprocess.run(["chroot", str(min_dir), "/tmp/v05_step2.sh"], check=True)
    script_path.unlink(missing_ok=True)


def main():
    if os.geteuid() != 0:
        raise SystemExit("Error: build_v05.py must be run as root inside Linux/WSL.")

    args = parse_args()
    source_iso = Path(args.source_iso).resolve()
    output_iso = Path(args.output_iso).resolve()
    work_dir = Path(args.work_dir).resolve()
    repo_root = Path(args.repo_root).resolve()

    if not source_iso.is_file():
        raise SystemExit(f"Source ISO not found: {source_iso}")

    pkgs = load_packages(repo_root)
    disk_dir = work_dir / "disk"
    min_dir = work_dir / "min"

    if work_dir.exists():
        shutil.rmtree(work_dir)
    disk_dir.mkdir(parents=True)
    min_dir.mkdir(parents=True)

    print(f"Extracting source ISO {source_iso} -> {disk_dir}...", flush=True)
    subprocess.run(["xorriso", "-osirrox", "on", "-indev", str(source_iso), "-extract", "/", str(disk_dir)], check=True)
    subprocess.run(["chmod", "-R", "u+w", str(disk_dir)], check=True)

    print("Unsquashing minimal + minimal.standard layers...", flush=True)
    subprocess.run(["unsquashfs", "-d", str(min_dir), str(disk_dir / "casper/minimal.squashfs")], check=True)
    subprocess.run(["unsquashfs", "-f", "-d", str(min_dir), str(disk_dir / "casper/minimal.standard.squashfs")], check=True)
    (disk_dir / "casper/minimal.squashfs").unlink()
    (disk_dir / "casper/minimal.standard.squashfs").unlink()

    setup_base_packages_and_locale(min_dir, pkgs)
    setup_payload_and_branding(min_dir, repo_root)

    print("Updating casper/minimal.size and casper/minimal.manifest...", flush=True)
    du_out = subprocess.check_output(["du", "-sx", "--block-size=1", str(min_dir)], text=True).split()[0]
    (disk_dir / "casper/minimal.size").write_text(du_out + "\n", encoding="utf-8")
    manifest = subprocess.check_output(
        ["chroot", str(min_dir), "dpkg-query", "-W", "-f=${Package}\\t${Version}\\n"], text=True
    )
    (disk_dir / "casper/minimal.manifest").write_text(manifest, encoding="utf-8")

    print("Packing minimal.squashfs (zstd level 3)...", flush=True)
    subprocess.run(
        ["mksquashfs", str(min_dir), str(disk_dir / "casper/minimal.squashfs"), "-noappend", "-comp", "zstd", "-Xcompression-level", "3"],
        check=True,
    )
    shutil.rmtree(min_dir)

    std_link = disk_dir / "casper/minimal.standard.squashfs"
    if std_link.exists() or std_link.is_symlink():
        std_link.unlink()
    os.symlink("minimal.squashfs", std_link)

    # First word MUST be 'Ubuntu' so casper sets USERNAME=ubuntu instead of colliding.
    (disk_dir / ".disk/info").write_text(f"Ubuntu 24.04 LabKita 0.5 ({args.date})\n", encoding="utf-8")

    (disk_dir / "casper/install-sources.yaml").write_text(
        f"""-   default: true
    description:
        en: Noble Numbat
    id: ubuntu-desktop-minimal
    locale_support: none
    name:
        en: LabKita Linux 0.5
    path: minimal.squashfs
    size: {du_out}
    type: fsimage-layered
    variant: desktop
""",
        encoding="utf-8",
    )

    (disk_dir / "boot/grub/grub.cfg").write_text(
        """set timeout=10

loadfont unicode

set menu_color_normal=white/black
set menu_color_highlight=black/light-gray

menuentry "Coba atau Pasang LabKita Linux 0.5 (Bahasa Indonesia)" {
\tset gfxpayload=keep
\tlinux\t/casper/vmlinuz locale=id_ID.UTF-8 keyboard-configuration/layoutcode=us console-setup/layoutcode=us --- quiet splash
\tinitrd\t/casper/initrd
}

menuentry "LabKita Linux 0.5 (Safe Graphics)" {
\tset gfxpayload=keep
\tlinux\t/casper/vmlinuz nomodeset locale=id_ID.UTF-8 keyboard-configuration/layoutcode=us console-setup/layoutcode=us --- quiet splash
\tinitrd\t/casper/initrd
}
""",
        encoding="utf-8",
    )

    print("Regenerating md5sum.txt after all final files are written...", flush=True)
    cmd_md5 = (
        f"cd '{disk_dir}' && "
        "find . -type f ! -name md5sum.txt ! -name boot.catalog ! -path './boot/grub/i386-pc/eltorito.img' "
        "-print0 | sort -z | xargs -0 md5sum > md5sum.txt"
    )
    subprocess.run(["bash", "-c", cmd_md5], check=True)

    output_iso.parent.mkdir(parents=True, exist_ok=True)
    if output_iso.exists():
        output_iso.unlink()

    print(f"Building hybrid ISO {output_iso}...", flush=True)
    subprocess.run(
        [
            "xorriso",
            "-as",
            "mkisofs",
            "-r",
            "-J",
            "-joliet-long",
            "-l",
            "-iso-level",
            "3",
            "-V",
            "LabKita Linux 0.5 amd64",
            "--grub2-mbr",
            f"--interval:local_fs:0s-15s:zero_mbrpt,zero_gpt:{source_iso}",
            "--protective-msdos-label",
            "-partition_cyl_align",
            "off",
            "-partition_offset",
            "16",
            "--mbr-force-bootable",
            "-append_partition",
            "2",
            "28732ac11ff8d211ba4b00a0c93ec93b",
            f"--interval:local_fs:12196856d-12207015d::{source_iso}",
            "-appended_part_as_gpt",
            "-iso_mbr_part_type",
            "a2a0d0ebe5b9334487c068b6b72699c7",
            "-c",
            "/boot.catalog",
            "-b",
            "/boot/grub/i386-pc/eltorito.img",
            "-no-emul-boot",
            "-boot-load-size",
            "4",
            "-boot-info-table",
            "--grub2-boot-info",
            "-eltorito-alt-boot",
            "-e",
            "--interval:appended_partition_2:all::",
            "-no-emul-boot",
            "-boot-load-size",
            "10160",
            "-o",
            str(output_iso),
            str(disk_dir),
        ],
        check=True,
    )

    if not args.keep_work:
        shutil.rmtree(work_dir)
    print(f"BUILD_V05_DONE: {output_iso}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
