#!/usr/bin/env bash
# Validasi sintaks skrip, modul contoh, alat build, dan unit systemd 0.6 tanpa root/chroot.
set -Eeuo pipefail
project=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$project"

bash -n payload/usr/local/sbin/labkita-postinstall payload/usr/local/bin/labkita-guide
python3 -m py_compile payload/usr/local/bin/labkita-check tools/build_v06.py tools/generate_brand_assets.py tools/generate_wallpaper.py
python3 payload/usr/share/labkita/examples/hello.py >/dev/null
python3 payload/usr/share/labkita/examples/processes.py >/dev/null
python3 payload/usr/share/labkita/examples/thread_demo.py >/dev/null

temporary=$(mktemp -d)
trap 'rm -f -- "$temporary/labkita-runtime.service"; rmdir -- "$temporary"' EXIT
install -m 0644 payload/etc/systemd/system/labkita-runtime.service "$temporary/labkita-runtime.service"
systemd-analyze verify "$temporary/labkita-runtime.service"

printf 'LULUS: sintaks Bash/Python, contoh praktikum, dan unit systemd 0.6 valid.\n'
