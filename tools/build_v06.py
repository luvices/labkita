#!/usr/bin/env python3
"""Bangun ISO LabKita Linux 0.6 di WSL/Linux (Autoinstall admin+praktikan, logo resmi Plymouth+GDM, WhiteSur pulih, panduan baru)."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import yaml


VERSION = "0.6"
CODENAME = "Noble Numbat"

PROTECTED_PACKAGES = {
    "ubuntu-desktop-minimal",
    "gnome-shell",
    "gdm3",
    "nautilus",
    "gnome-terminal",
    "gnome-control-center",
    "snapd",
    "plymouth",
    "plymouth-theme-spinner",
    "casper",
    "firefox",
    "network-manager",
}


def parse_args():
    default_repo = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description=f"Build LabKita Linux {VERSION} hybrid ISO from official Ubuntu 24.04.5.1 Desktop ISO."
    )
    parser.add_argument("--source-iso", required=True, help="Path to Ubuntu 24.04.5.1 desktop amd64 ISO.")
    parser.add_argument("--output-iso", required=True, help=f"Destination path for labkita-linux-{VERSION}-amd64.iso.")
    parser.add_argument("--work-dir", default="/var/tmp/labkita-v06", help="Temporary Linux build directory.")
    parser.add_argument("--repo-root", default=str(default_repo), help="Path to labkita-linux repository root.")
    parser.add_argument(
        "--date",
        default=datetime.now(timezone.utc).strftime("%Y%m%d"),
        help="Release date stamp for .disk/info (YYYYMMDD).",
    )
    parser.add_argument("--keep-work", action="store_true", help="Keep temporary work directory after build.")
    return parser.parse_args()


def load_list_file(path: Path, required: bool = True):
    if not path.is_file():
        if required:
            raise SystemExit(f"Required config file not found: {path}")
        return []
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        item = line.split("#", 1)[0].strip()
        if item:
            items.append(item)
    if required and not items:
        raise SystemExit(f"No entries found in {path}")
    return items


def check_safe_purge_candidates(min_dir: Path, candidates):
    """Filter remove-packages.txt safely so protected desktop packages are never removed."""
    if not candidates:
        return []
    installed_out = subprocess.check_output(
        ["chroot", str(min_dir), "dpkg-query", "-W", "-f=${Package}\t${Status}\n"],
        text=True,
    )
    installed = {
        line.split("\t", 1)[0]
        for line in installed_out.splitlines()
        if "\tinstall ok installed" in line
    }
    present = [pkg for pkg in candidates if pkg in installed]
    safe = []
    for pkg in present:
        sim = subprocess.run(
            ["chroot", str(min_dir), "apt-get", "purge", "-s", "-y", pkg],
            capture_output=True,
            text=True,
            check=True,
        )
        remv = [
            ln.split()[1].split(":", 1)[0]
            for ln in sim.stdout.splitlines()
            if ln.startswith(("Remv ", "Purg ")) and len(ln.split()) >= 2
        ]
        blocked = sorted(set(remv) & PROTECTED_PACKAGES)
        if blocked:
            print(f"[SKIP PURGE] {pkg} would remove protected packages: {blocked}", flush=True)
        else:
            safe.append(pkg)
    return safe


def setup_base_packages_and_locale(min_dir: Path, pkgs, remove_candidates):
    pkg_list = " ".join(pkgs)
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

        safe_purge = check_safe_purge_candidates(min_dir, remove_candidates)
        purge_cmd = ""
        if safe_purge:
            purge_str = " ".join(safe_purge)
            print(f"Purging non-lab bloat packages: {purge_str}", flush=True)
            purge_cmd = (
                f"apt-get purge -y {purge_str}\n"
                "apt-get autoremove -y --purge\n"
            )

        chroot_step1 = f"""#!/usr/bin/env bash
set -Eeuo pipefail
export DEBIAN_FRONTEND=noninteractive
cat <<'EOF' > /etc/apt/apt.conf.d/99no-check-valid
Acquire::Check-Valid-Until "false";
EOF
{purge_cmd}apt-get update
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
        script_path = min_dir / "tmp/v06_step1.sh"
        script_path.write_text(chroot_step1, encoding="utf-8")
        os.chmod(script_path, 0o755)
        print("Running chroot bloat cleanup, package installation, & Indonesian locale setup...", flush=True)
        subprocess.run(["chroot", str(min_dir), "/tmp/v06_step1.sh"], check=True)
        script_path.unlink(missing_ok=True)
    finally:
        for target in reversed(mounts):
            subprocess.run(["umount", "-lf", str(target)], check=False)

    resolv = min_dir / "etc/resolv.conf"
    if resolv.exists() and not resolv.is_symlink():
        resolv.unlink()
        os.symlink("../run/systemd/resolve/stub-resolv.conf", resolv)


def restore_git_symlinks(repo_root: Path, min_dir: Path):
    """Restore Git 120000 symlinks inside min_dir that Windows NTFS checked out as text stubs."""
    out = subprocess.check_output(
        ["git", "-c", "safe.directory=*", "-C", str(repo_root), "ls-files", "-s", "payload/"],
        text=True,
    )
    restored = 0
    verified = 0
    for line in out.splitlines():
        if "\t" not in line:
            continue
        meta, rel = line.split("\t", 1)
        if not meta.startswith("120000 "):
            continue
        rel_inside = Path(rel).relative_to("payload")
        dst = min_dir / rel_inside
        if dst.is_symlink():
            verified += 1
            continue
        if dst.is_file():
            target = dst.read_text(encoding="utf-8").strip()
            if not target or "\n" in target:
                raise RuntimeError(f"Invalid symlink stub content at {dst}: {target!r}")
            dst.unlink()
            os.symlink(target, dst)
            restored += 1
            verified += 1
        else:
            raise RuntimeError(f"Missing expected symlink entry in target rootfs: {dst}")

    stubs = 0
    for theme in (min_dir / "usr/share/icons").glob("WhiteSur*"):
        for f in theme.rglob("*"):
            if f.is_file() and not f.is_symlink() and f.suffix.lower() in (".svg", ".png") and f.stat().st_size < 120:
                raw = f.read_bytes()
                if not raw.startswith((b"\x89PNG", b"<svg", b"<?xml", b"<!--", b"\n<svg", b" <svg")):
                    stubs += 1
    if stubs:
        raise RuntimeError(f"Found {stubs} remaining broken WhiteSur icon text stubs after symlink restore!")
    print(f"Git symlinks restored={restored}, total_verified={verified}, broken_stubs={stubs}", flush=True)


def synthesize_missing_terminal_svg(min_dir: Path):
    """Restore WhiteSur/apps/scalable/terminal.svg on Linux ext4 (clobbered on Windows NTFS by Terminal.svg)."""
    scalable_dir = min_dir / "usr/share/icons/WhiteSur/apps/scalable"
    term_target = scalable_dir / "terminal.svg"
    term_prefs = scalable_dir / "org.gnome.Terminal.Preferences.svg"
    if not term_target.exists() and term_prefs.is_file():
        prefs_svg = term_prefs.read_text(encoding="utf-8")
        marker = '<image xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAg'
        if marker in prefs_svg:
            term_svg = prefs_svg.split(marker, 1)[0] + "</svg>\n"
            term_target.write_text(term_svg, encoding="utf-8")
            term_target.chmod(0o644)
    util_term = scalable_dir / "utilities-terminal.svg"
    if not util_term.is_file() or util_term.stat().st_size < 2000:
        raise RuntimeError(f"Expected valid WhiteSur utilities-terminal icon at {util_term}")


def setup_payload_and_branding(min_dir: Path, repo_root: Path):
    print("Copying payload/. into rootfs (tar stream)...", flush=True)
    subprocess.run(
        ["bash", "-c", f"tar -C '{repo_root}/payload' -cf - . | tar -C '{min_dir}' -xf -"],
        check=True,
    )
    restore_git_symlinks(repo_root, min_dir)
    synthesize_missing_terminal_svg(min_dir)

    chroot_step2 = f"""#!/usr/bin/env bash
set -Eeuo pipefail

rm -rf /usr/local/bin/__pycache__ /usr/local/sbin/__pycache__
for f in /usr/local/bin/labkita-check /usr/local/bin/labkita-guide /usr/local/sbin/labkita-postinstall \\
         /etc/systemd/system/labkita-runtime.service /etc/dconf/db/local.d/20-labkita \\
         /etc/dconf/profile/user /etc/dconf/profile/gdm /etc/dconf/db/gdm.d/99-labkita-logo \\
         /usr/share/gdm/dconf/99-labkita-logo /usr/share/glib-2.0/schemas/20_labkita-settings.gschema.override \\
         /etc/skel/.config/gnome-initial-setup-done /usr/share/applications/labkita-guide.desktop \\
         /usr/share/desktop-provision/whitelabel.yaml /usr/share/plymouth/themes/bgrt/bgrt.plymouth; do
    [[ -f "$f" ]] && sed -i 's/\\r$//' "$f"
done
find /usr/share/labkita -type f \\( -name '*.py' -o -name '*.c' -o -name '*.sh' -o -name '*.html' -o -name '*.css' -o -name '*.txt' \\) -exec sed -i 's/\\r$//' {{}} +
find /usr/share/icons -name 'index.theme' -type f -exec sed -i 's/\\r$//' {{}} +

chmod 0755 /usr/local/bin/labkita-check /usr/local/bin/labkita-guide /usr/local/sbin/labkita-postinstall
find /usr/share/labkita -type d -exec chmod 0755 {{}} +
find /usr/share/labkita -type f -exec chmod 0644 {{}} +
chmod 0644 /etc/systemd/system/labkita-runtime.service
chmod 0644 /usr/share/applications/labkita-guide.desktop
chmod 0644 /etc/skel/.config/gnome-initial-setup-done

install -d -m 0755 /usr/share/desktop-provision
if [[ -f /usr/share/desktop-provision/whitelabel.yaml ]]; then
    chmod 0644 /usr/share/desktop-provision/whitelabel.yaml
    ln -sfn whitelabel.yaml /usr/share/desktop-provision/whitelabel.yml
fi

if [[ -d /usr/share/plymouth/themes/spinner ]]; then
    chmod 0644 /usr/share/plymouth/themes/spinner/watermark.png /usr/share/plymouth/themes/spinner/bgrt-fallback.png
fi
if [[ -f /usr/share/plymouth/themes/bgrt/bgrt.plymouth ]]; then
    chmod 0644 /usr/share/plymouth/themes/bgrt/bgrt.plymouth
fi
if [[ -f /usr/share/pixmaps/labkita-gdm-logo.png ]]; then
    chmod 0644 /usr/share/pixmaps/labkita-gdm-logo.png
fi

if [[ -d /usr/share/themes ]]; then
    find /usr/share/themes -type d -exec chmod 0755 {{}} +
    find /usr/share/themes -type f -exec chmod 0644 {{}} +
fi
if [[ -d /usr/share/icons ]]; then
    find /usr/share/icons -type d -exec chmod 0755 {{}} +
    find /usr/share/icons -type f -exec chmod 0644 {{}} +
    for theme in WhiteSur WhiteSur-dark WhiteSur-light; do
        if [[ -d "/usr/share/icons/$theme" ]]; then
            gtk-update-icon-cache -q -f "/usr/share/icons/$theme"
            test -f "/usr/share/icons/$theme/icon-theme.cache"
        fi
    done
fi

# Nonaktifkan notifikasi upgrade rilis Ubuntu (offline lab)
if [[ -f /etc/update-manager/release-upgrades ]]; then
    sed -i 's/^Prompt=.*/Prompt=never/' /etc/update-manager/release-upgrades
fi

# Kompilasi schema GLib dan GDM greeter agar logo LabKita tampil di layar login
chmod 0644 /usr/share/glib-2.0/schemas/20_labkita-settings.gschema.override
glib-compile-schemas /usr/share/glib-2.0/schemas
chmod 0644 /usr/share/gdm/dconf/99-labkita-logo /etc/dconf/profile/gdm /etc/dconf/db/gdm.d/99-labkita-logo
if [[ -x /usr/share/gdm/generate-config ]]; then
    /usr/share/gdm/generate-config || true
fi
install -d -m 0711 -o gdm -g gdm /var/lib/gdm3
dconf compile /var/lib/gdm3/greeter-dconf-defaults /usr/share/gdm/dconf
chown gdm:gdm /var/lib/gdm3/greeter-dconf-defaults

cat > /etc/labkita-release <<'EOF'
NAME="LabKita Linux"
VERSION="{VERSION}"
BASE="Ubuntu 24.04 LTS"
PURPOSE="Praktikum pemrograman dasar offline"
EOF
cat > /etc/motd <<'EOF'
LabKita Linux {VERSION} | Praktikum pemrograman offline (Bahasa Indonesia)
Panduan: Jalankan 'labkita-guide' atau buka menu 'Panduan LabKita'
Uji kesiapan: labkita-check
Ruang sementara: /run/labkita (RAM disk sementara)
EOF

if [[ -f /usr/lib/os-release ]]; then
    sed -i 's/^PRETTY_NAME=.*/PRETTY_NAME="LabKita Linux {VERSION} ({CODENAME})"/' /usr/lib/os-release
fi
if [[ -f /etc/lsb-release ]]; then
    sed -i 's/^DISTRIB_DESCRIPTION=.*/DISTRIB_DESCRIPTION="LabKita Linux {VERSION}"/' /etc/lsb-release
fi

install -d -m 0755 /etc/dconf/profile
if [[ ! -f /etc/dconf/profile/user ]]; then
    printf 'user-db:user\\nsystem-db:local\\n' > /etc/dconf/profile/user
elif ! grep -qxF 'system-db:local' /etc/dconf/profile/user; then
    printf '\\nsystem-db:local\\n' >> /etc/dconf/profile/user
fi
dconf update
test -f /etc/dconf/db/local
test -f /etc/dconf/db/gdm

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
dpkg-query -W -f='${{binary:Package}}\\t${{Version}}\\n' > /usr/share/labkita/build/packages.tsv
cat > /usr/share/labkita/build/LICENSES.txt <<'EOF'
Lisensi setiap paket tersedia di /usr/share/doc/<nama-paket>/copyright.
Skrip dan aset LabKita berada pada repositori proyek kelompok.
Sertakan sumber dan lisensi upstream dalam laporan dan repositori.
EOF

if ls /boot/initrd.img-* >/dev/null 2>&1; then
    update-initramfs -u -k all
fi
"""
    script_path = min_dir / "tmp/v06_step2.sh"
    script_path.write_text(chroot_step2, encoding="utf-8")
    os.chmod(script_path, 0o755)
    print("Running chroot branding, GDM logo, icon cache, whitelabel, and Plymouth setup...", flush=True)
    subprocess.run(["chroot", str(min_dir), "/tmp/v06_step2.sh"], check=True)
    script_path.unlink(missing_ok=True)


def hash_password(plain: str) -> str:
    return subprocess.check_output(["openssl", "passwd", "-6", plain], text=True).strip()


def write_nocloud_autoinstall(disk_dir: Path):
    """Create nocloud/user-data and meta-data for zero-touch install with dual accounts."""
    admin_pass = os.environ.get("LABKITA_ADMIN_PASS", "labkita")
    student_pass = os.environ.get("LABKITA_PRAKTIKAN_PASS", "praktikan")
    admin_hash = hash_password(admin_pass)
    student_hash = hash_password(student_pass)

    nocloud_dir = disk_dir / "nocloud"
    nocloud_dir.mkdir(parents=True, exist_ok=True)
    (nocloud_dir / "meta-data").write_text(
        "instance-id: labkita-v06\nlocal-hostname: labkita-pc\n",
        encoding="utf-8",
    )

    cfg = {
        "autoinstall": {
            "version": 1,
            "source": {"id": "ubuntu-desktop-minimal"},
            "locale": "id_ID.UTF-8",
            "keyboard": {"layout": "us", "variant": ""},
            "timezone": "Asia/Jakarta",
            "refresh-installer": {"update": False},
            "apt": {"fallback": "offline-install"},
            "drivers": {"install": False},
            "codecs": {"install": False},
            "storage": {"layout": {"name": "direct"}},
            "identity": {
                "realname": "LabKita Admin",
                "username": "labkita",
                "hostname": "labkita-pc",
                "password": admin_hash,
            },
            "shutdown": "reboot",
            "late-commands": [
                ["curtin", "in-target", "--target=/target", "--", "mkdir", "-p", "/home/labkita/.config"],
                ["curtin", "in-target", "--target=/target", "--", "cp", "/etc/skel/.config/gnome-initial-setup-done", "/home/labkita/.config/gnome-initial-setup-done"],
                ["curtin", "in-target", "--target=/target", "--", "chown", "-R", "labkita:labkita", "/home/labkita/.config"],
                ["curtin", "in-target", "--target=/target", "--", "sh", "-c", "getent group labkita-praktikum >/dev/null || groupadd --system labkita-praktikum"],
                ["curtin", "in-target", "--target=/target", "--", "useradd", "--create-home", "--user-group", "--shell", "/bin/bash", "--groups", "labkita-praktikum", "praktikan"],
                ["curtin", "in-target", "--target=/target", "--", "usermod", "--password", student_hash, "praktikan"],
                ["curtin", "in-target", "--target=/target", "--", "chmod", "0700", "/home/praktikan"],
                ["curtin", "in-target", "--target=/target", "--", "mkdir", "-p", "/home/praktikan/Praktikum", "/home/praktikan/Dokumen/Panduan-LabKita", "/home/praktikan/.config"],
                ["curtin", "in-target", "--target=/target", "--", "sh", "-c", "cp -a /usr/share/labkita/examples/. /home/praktikan/Praktikum/ && cp -a /usr/share/labkita/guide/. /home/praktikan/Dokumen/Panduan-LabKita/"],
                ["curtin", "in-target", "--target=/target", "--", "cp", "/etc/skel/.config/gnome-initial-setup-done", "/home/praktikan/.config/gnome-initial-setup-done"],
                ["curtin", "in-target", "--target=/target", "--", "chown", "-R", "praktikan:praktikan", "/home/praktikan"],
                ["curtin", "in-target", "--target=/target", "--", "chmod", "0755", "/home/praktikan/Dokumen", "/home/praktikan/Dokumen/Panduan-LabKita"],
            ],
        }
    }

    user_data_text = "#cloud-config\n" + yaml.safe_dump(cfg, sort_keys=False, default_flow_style=False)
    user_data_path = nocloud_dir / "user-data"
    user_data_path.write_text(user_data_text, encoding="utf-8")

    # Sanity validate against snap autoinstall-schema.json if jsonschema is installed in host Python
    try:
        parsed = yaml.safe_load(user_data_text)
        assert parsed["autoinstall"]["version"] == 1
        assert len(parsed["autoinstall"]["late-commands"]) == 12
    except Exception as exc:
        raise RuntimeError(f"Generated nocloud/user-data failed YAML check: {exc}") from exc
    print(f"Wrote NoCloud autoinstall seed at {user_data_path} (dual accounts: labkita + praktikan).", flush=True)


def patch_live_initrd_plymouth(disk_dir: Path, repo_root: Path):
    """Replace only the 3 Plymouth assets in the final zstd cpio segment of casper/initrd."""
    initrd_path = disk_dir / "casper/initrd"
    raw_parts = subprocess.check_output(["3cpio", "-e", "--raw", str(initrd_path)], text=True).strip().splitlines()
    last_idx = len(raw_parts)
    last_start = int(raw_parts[-1].split()[0])

    with tempfile.TemporaryDirectory(prefix="lk_initrd_") as tmp:
        tmp_path = Path(tmp)
        p4_dir = tmp_path / "part4"
        p4_dir.mkdir()
        subprocess.run(["3cpio", "-x", "-P", str(last_idx), "-C", str(p4_dir), str(initrd_path)], check=True)

        targets = [
            "usr/share/plymouth/themes/spinner/watermark.png",
            "usr/share/plymouth/themes/spinner/bgrt-fallback.png",
            "usr/share/plymouth/themes/bgrt/bgrt.plymouth",
        ]
        for rel in targets:
            src = repo_root / "payload" / rel
            dst = p4_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            dst.chmod(0o644)

        prefix = initrd_path.read_bytes()[:last_start]
        new_p4 = subprocess.check_output(
            ["bash", "-c", "find . -mindepth 1 -print0 | LC_ALL=C sort -z | cpio --null -o -H newc --quiet | zstd -q -19"],
            cwd=p4_dir,
        )
        initrd_path.write_bytes(prefix + new_p4)

        verify_dir = tmp_path / "verify"
        verify_dir.mkdir()
        subprocess.run(["unmkinitramfs", str(initrd_path), str(verify_dir)], check=True)
        for rel in targets:
            h_src = hashlib.sha256((repo_root / "payload" / rel).read_bytes()).hexdigest()
            h_ext = hashlib.sha256((verify_dir / rel).read_bytes()).hexdigest()
            if h_src != h_ext:
                raise RuntimeError(f"Live initrd Plymouth verification failed for {rel}")
    print("Patched casper/initrd with LabKita Plymouth splash assets (verified via unmkinitramfs).", flush=True)


def main():
    if os.geteuid() != 0:
        raise SystemExit("Error: build_v06.py must be run as root inside Linux/WSL.")

    args = parse_args()
    source_iso = Path(args.source_iso).resolve()
    output_iso = Path(args.output_iso).resolve()
    work_dir = Path(args.work_dir).resolve()
    repo_root = Path(args.repo_root).resolve()

    if not source_iso.is_file():
        raise SystemExit(f"Source ISO not found: {source_iso}")

    pkgs = load_list_file(repo_root / "config/packages.txt", required=True)
    remove_pkgs = load_list_file(repo_root / "config/remove-packages.txt", required=False)

    disk_dir = work_dir / "disk"
    min_dir = work_dir / "min"

    if work_dir.exists():
        shutil.rmtree(work_dir)
    disk_dir.mkdir(parents=True)
    min_dir.mkdir(parents=True)

    print(f"Extracting source ISO {source_iso} -> {disk_dir}...", flush=True)
    subprocess.run(["xorriso", "-osirrox", "on", "-indev", str(source_iso), "-extract", "/", str(disk_dir)], check=True)
    subprocess.run(["chmod", "-R", "u+w", str(disk_dir)], check=True)

    print("Unsquashing minimal.squashfs ONLY (excluding minimal.standard.squashfs bloat)...", flush=True)
    subprocess.run(["unsquashfs", "-d", str(min_dir), str(disk_dir / "casper/minimal.squashfs")], check=True)
    (disk_dir / "casper/minimal.squashfs").unlink()
    std_sqfs = disk_dir / "casper/minimal.standard.squashfs"
    if std_sqfs.exists() or std_sqfs.is_symlink():
        std_sqfs.unlink()

    setup_base_packages_and_locale(min_dir, pkgs, remove_pkgs)
    setup_payload_and_branding(min_dir, repo_root)

    print("Updating casper/minimal.size and casper/minimal.manifest...", flush=True)
    du_out = subprocess.check_output(["du", "-sx", "--block-size=1", str(min_dir)], text=True).split()[0]
    (disk_dir / "casper/minimal.size").write_text(du_out + "\n", encoding="utf-8")
    manifest = subprocess.check_output(
        ["chroot", str(min_dir), "dpkg-query", "-W", "-f=${Package}\\t${Version}\\n"], text=True
    )
    (disk_dir / "casper/minimal.manifest").write_text(manifest, encoding="utf-8")
    (disk_dir / "casper/minimal.standard.manifest").write_text(manifest, encoding="utf-8")

    print("Packing minimal.squashfs (zstd level 3)...", flush=True)
    subprocess.run(
        ["mksquashfs", str(min_dir), str(disk_dir / "casper/minimal.squashfs"), "-noappend", "-comp", "zstd", "-Xcompression-level", "3"],
        check=True,
    )
    shutil.rmtree(min_dir)

    os.symlink("minimal.squashfs", disk_dir / "casper/minimal.standard.squashfs")

    patch_live_initrd_plymouth(disk_dir, repo_root)
    write_nocloud_autoinstall(disk_dir)

    (disk_dir / ".disk/info").write_text(
        f'Ubuntu 24.04 LabKita {VERSION} "{CODENAME}" - Release amd64 ({args.date})\n',
        encoding="utf-8",
    )

    (disk_dir / "casper/install-sources.yaml").write_text(
        f"""-   default: true
    description:
        en: {CODENAME}
    id: ubuntu-desktop-minimal
    locale_support: none
    name:
        en: LabKita Linux {VERSION}
    path: minimal.squashfs
    size: {du_out}
    type: fsimage-layered
    variant: desktop
""",
        encoding="utf-8",
    )

    (disk_dir / "boot/grub/grub.cfg").write_text(
        f"""set default=0
set timeout=5

loadfont unicode

set menu_color_normal=white/black
set menu_color_highlight=black/light-gray

menuentry "Pasang Otomatis LabKita Linux {VERSION} (Admin + Praktikan)" {{
\tset gfxpayload=keep
\tlinux\t/casper/vmlinuz autoinstall ds=nocloud\\;s=/cdrom/nocloud/ locale=id_ID.UTF-8 keyboard-configuration/layoutcode=us console-setup/layoutcode=us --- quiet splash
\tinitrd\t/casper/initrd
}}

menuentry "Coba atau Pasang Manual LabKita Linux {VERSION} (Bahasa Indonesia)" {{
\tset gfxpayload=keep
\tlinux\t/casper/vmlinuz locale=id_ID.UTF-8 keyboard-configuration/layoutcode=us console-setup/layoutcode=us --- quiet splash
\tinitrd\t/casper/initrd
}}

menuentry "LabKita Linux {VERSION} (Safe Graphics)" {{
\tset gfxpayload=keep
\tlinux\t/casper/vmlinuz nomodeset locale=id_ID.UTF-8 keyboard-configuration/layoutcode=us console-setup/layoutcode=us --- quiet splash
\tinitrd\t/casper/initrd
}}
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
            f"LabKita Linux {VERSION} amd64",
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
            "-isohybrid-gpt-basdat",
            "-o",
            str(output_iso),
            str(disk_dir),
        ],
        check=True,
    )

    if not args.keep_work:
        shutil.rmtree(work_dir)
    print(f"\nBUILD_V06_DONE: {output_iso}", flush=True)


if __name__ == "__main__":
    main()
