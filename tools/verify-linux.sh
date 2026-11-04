#!/usr/bin/env bash
# Validasi kode tanpa apt, tanpa root, dan tanpa menyalin payload ke sistem.
set -Eeuo pipefail
project=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$project"
bash -n scripts/customize.sh payload/usr/local/sbin/labkita-postinstall
python3 payload/usr/share/labkita/examples/hello.py
python3 payload/usr/share/labkita/examples/processes.py

# /mnt/d dapat memperlihatkan semua berkas sebagai executable/world-writable.
# Verifikasi unit dari salinan Linux dengan permission yang akan dipasang kit.
temporary=$(mktemp -d)
trap 'rm -f -- "$temporary/labkita-runtime.service" "$temporary/guard.log"; rmdir -- "$temporary"' EXIT
install -m 0644 payload/etc/systemd/system/labkita-runtime.service "$temporary/labkita-runtime.service"
systemd-analyze verify "$temporary/labkita-runtime.service"

if bash scripts/customize.sh >"$temporary/guard.log" 2>&1; then
    printf 'GAGAL: skrip menerima pemanggilan tanpa --cubic.\n' >&2
    exit 1
else
    code=$?
    test "$code" -eq 2
fi
# Host ini harus terdeteksi bukan chroot sebelum menguji penolakan.
if systemd-detect-virt --quiet --chroot; then
    printf 'Lewati uji penolakan host: pemeriksaan dijalankan dalam chroot.\n'
else
    if bash scripts/customize.sh --cubic >"$temporary/guard.log" 2>&1; then
        printf 'GAGAL: skrip menerima lingkungan host.\n' >&2
        exit 1
    fi
fi
printf 'LULUS: sintaks Bash, contoh Python/proses, unit systemd, dan penolakan host.\n'
