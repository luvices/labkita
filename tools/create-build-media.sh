#!/usr/bin/env bash
set -Eeuo pipefail
project=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
original="${1:-$HOME/Downloads/ubuntu-24.04.5.1-desktop-amd64.iso}"
output="$project/build/ubuntu-build-vm-AUTOINSTALL.iso"
if [[ -e $output ]]; then
    printf 'Media build sudah ada, tidak ditimpa: %s\n' "$output" >&2
    exit 2
fi
test -f "$project/build/seed/autoinstall.yaml"
xorriso -indev "$original" -outdev "$output" \
    -map "$project/build/seed/grub.cfg" /boot/grub/grub.cfg \
    -map "$project/build/seed/autoinstall.yaml" /autoinstall.yaml \
    -boot_image any replay -volid LABKITA_BUILD_VM \
    -padding included -compliance no_emul_toc
printf '\nMedia instalasi khusus VM build siap. ISO ini BUKAN produk final LabKita.\n'
