#!/usr/bin/env bash
set -Eeuo pipefail
if [[ $EUID -ne 0 || ! -f /var/lib/labkita-build-vm-ready ]]; then
    printf 'Hanya untuk VM build LabKita yang telah disiapkan proyek.\n' >&2
    exit 1
fi
exec > >(tee /var/log/labkita-cubic-setup.log) 2>&1
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y software-properties-common
add-apt-repository -y universe
add-apt-repository -y ppa:cubic-wizard/release
apt-get update
apt-get install -y --no-install-recommends cubic
install -d -o builder -g builder -m 0755 /home/builder/cubic /home/builder/labkita-input
touch /var/lib/labkita-cubic-ready
printf '\nCubic siap. Pilih ISO ASLI pada /home/builder/labkita-input/.\n'
