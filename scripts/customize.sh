#!/usr/bin/env bash
# Jalankan hanya di terminal virtual Cubic, bukan terminal host build.
set -Eeuo pipefail
trap 'printf "Build terhenti pada baris %s. Baca error sebelum mengulangi.\n" "$LINENO" >&2' ERR

if [[ ${1:-} != --cubic ]]; then
    printf 'Pemakaian di terminal virtual Cubic: bash scripts/customize.sh --cubic\n' >&2
    exit 2
fi
if [[ $EUID -ne 0 ]]; then
    printf 'Terminal Cubic harus berjalan sebagai root.\n' >&2
    exit 1
fi
if ! command -v systemd-detect-virt >/dev/null || (! systemd-detect-virt --quiet --chroot && [[ $(systemd-detect-virt) != "systemd-nspawn" ]]); then
    printf 'Ditolak: lingkungan chroot/container Cubic tidak terdeteksi. Jangan jalankan di host.\n' >&2
    exit 1
fi
. /etc/os-release
if [[ $ID != ubuntu || $VERSION_ID != 24.04 ]]; then
    printf 'Kit awal ini menargetkan ISO Ubuntu 24.04 LTS; terdeteksi %s.\n' "$PRETTY_NAME" >&2
    exit 1
fi

kit_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends software-properties-common
add-apt-repository -y universe
apt-get update
mapfile -t packages < <(sed 's/#.*//; /^[[:space:]]*$/d' "$kit_dir/config/packages.txt")
apt-get install -y --no-install-recommends "${packages[@]}"

# Konfigurasi Locale Bahasa Indonesia
locale-gen id_ID.UTF-8
update-locale LANG=id_ID.UTF-8 LANGUAGE=id_ID:id LC_ALL=id_ID.UTF-8

cat > /etc/default/locale <<'EOF'
LANG="id_ID.UTF-8"
LANGUAGE="id_ID:id"
LC_ALL="id_ID.UTF-8"
EOF

# Konfigurasi Zona Waktu Asia/Jakarta
ln -sf /usr/share/zoneinfo/Asia/Jakarta /etc/localtime
echo "Asia/Jakarta" > /etc/timezone

# Konfigurasi Layout Keyboard US
cat > /etc/default/keyboard <<'EOF'
XKBMODEL="pc105"
XKBLAYOUT="us"
XKBVARIANT=""
XKBOPTIONS=""
BACKSPACE="guess"
EOF

# Salin seluruh payload (tema, ikon, kursor, background, skrip) ke sistem root
cp -a "$kit_dir/payload/." /

# Hak akses utilitas dan pustaka
chmod 0755 /usr/local/bin/labkita-check /usr/local/bin/labkita-guide /usr/local/sbin/labkita-postinstall
find /usr/share/labkita -type d -exec chmod 0755 {} +
find /usr/share/labkita -type f -exec chmod 0644 {} +
chmod 0644 /etc/systemd/system/labkita-runtime.service
chmod 0644 /usr/share/applications/labkita-guide.desktop

# Pastikan perizinan tema dan ikon terbuka untuk seluruh pengguna
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
VERSION="0.2"
BASE="Ubuntu 24.04 LTS"
PURPOSE="Praktikum pemrograman dasar offline"
EOF
cat > /etc/motd <<'EOF'
LabKita Linux 0.2 | Praktikum pemrograman offline (Bahasa Indonesia)
Panduan: Jalankan 'labkita-guide' atau buka menu 'Panduan LabKita'
Uji kesiapan: labkita-check
Ruang sementara: /run/labkita (RAM disk sementara)
EOF

# Pertahankan /etc/os-release Ubuntu agar installer dan deteksi paket konsisten.
install -d -m 0755 /etc/dconf/profile
if [[ ! -f /etc/dconf/profile/user ]]; then
    printf 'user-db:user\nsystem-db:local\n' > /etc/dconf/profile/user
elif ! grep -qxF 'system-db:local' /etc/dconf/profile/user; then
    printf '\nsystem-db:local\n' >> /etc/dconf/profile/user
fi
dconf update
getent group labkita >/dev/null || groupadd --system labkita

# Siapkan skel untuk user baru (termasuk praktikan)
install -d -m 0755 /etc/skel/Praktikum
cp -a /usr/share/labkita/examples/. /etc/skel/Praktikum/
install -d -m 0755 /etc/skel/.local/share/labkita/guide
cp -a /usr/share/labkita/guide/. /etc/skel/.local/share/labkita/guide/

# Enable tanpa start: systemd tidak berjalan dalam chroot Cubic.
install -d -m 0755 /etc/systemd/system/multi-user.target.wants
ln -sfn /etc/systemd/system/labkita-runtime.service \
    /etc/systemd/system/multi-user.target.wants/labkita-runtime.service

install -d -m 0755 /usr/share/labkita/build
date -u '+%Y-%m-%dT%H:%M:%SZ' > /usr/share/labkita/build/build-time.txt
cp /etc/os-release /usr/share/labkita/build/base-os-release
dpkg-query -W -f='${binary:Package}\t${Version}\n' > /usr/share/labkita/build/packages.tsv
cat > /usr/share/labkita/build/LICENSES.txt <<'EOF'
Lisensi setiap paket tersedia di /usr/share/doc/<nama-paket>/copyright.
Skrip dan aset LabKita berada pada repositori proyek kelompok.
Sertakan sumber dan lisensi upstream dalam laporan dan repositori.
EOF
apt-get clean
printf '\nKustomisasi selesai. Lanjutkan generate ISO di Cubic.\n'
printf 'Jalankan labkita-check setelah boot dan setelah instalasi ke VM bersih.\n'
