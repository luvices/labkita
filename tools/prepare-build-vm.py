"""Siapkan konfigurasi khusus VM baru; tidak menyentuh VM/disk fisik lain."""
import json
from pathlib import Path
import secrets
import subprocess

root = Path(__file__).resolve().parents[1]
build = root / "build"
vm = build / "vm"
seed = build / "seed"
vm.mkdir(parents=True, exist_ok=True)
seed.mkdir(exist_ok=True)
credentials = build / "builder.credentials.json"
if credentials.exists() or (vm / "labkita-build.vmx").exists():
    raise SystemExit("Konfigurasi/credential VM sudah ada; tidak ditimpa.")

password = secrets.token_urlsafe(24)
hashed = subprocess.run(
    ["wsl.exe", "-d", "Ubuntu", "--", "openssl", "passwd", "-6", "-stdin"],
    input=(password + "\n").encode("ascii"), capture_output=True, check=True,
).stdout.decode("ascii").strip()
if not hashed.startswith("$6$"):
    raise SystemExit("Hash password SHA512 tidak berhasil dibuat.")
credentials.write_text(json.dumps({"username": "builder", "password": password}, indent=2), encoding="utf-8")

config = {"autoinstall": {
    "version": 1,
    "refresh-installer": {"update": False},
    "locale": "en_US.UTF-8",
    "keyboard": {"layout": "us"},
    "timezone": "Asia/Jakarta",
    "source": {"id": "ubuntu-desktop-minimal", "search_drivers": False},
    "identity": {"hostname": "labkita-build", "username": "builder", "realname": "LabKita Builder", "password": hashed},
    "storage": {"layout": {"name": "direct", "match": {"model": "VMware*"}}},
    "apt": {"geoip": False, "primary": [{"arches": ["amd64"], "uri": "http://archive.ubuntu.com/ubuntu"}]},
    "packages": ["open-vm-tools-desktop", "software-properties-common", "xorriso", "squashfs-tools", "xdotool"],
    "codecs": {"install": False},
    "drivers": {"install": False},
    "updates": "security",
    "late-commands": [
        ["curtin", "in-target", "--target=/target", "--", "sh", "-c", "printf 'builder ALL=(ALL) NOPASSWD: ALL\\n' > /etc/sudoers.d/90-labkita-builder && chmod 0440 /etc/sudoers.d/90-labkita-builder"],
        ["curtin", "in-target", "--target=/target", "--", "sh", "-c", "sed -i '/^\\[daemon\\]/a AutomaticLoginEnable=true\\nAutomaticLogin=builder' /etc/gdm3/custom.conf"],
        ["curtin", "in-target", "--target=/target", "--", "touch", "/var/lib/labkita-build-vm-ready"],
    ],
    "shutdown": "reboot",
}}
# YAML 1.2 menerima struktur JSON. File ini hanya dipakai VM build baru.
(seed / "autoinstall.yaml").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
(seed / "grub.cfg").write_text('''set timeout=3
set default=0
loadfont unicode
menuentry "Install Ubuntu - dedicated LabKita BUILD VM only" {
    set gfxpayload=keep
    linux /casper/vmlinuz autoinstall subiquity.autoinstallpath=/cdrom/autoinstall.yaml --- quiet splash
    initrd /casper/initrd
}
''', encoding="utf-8")

iso = build / "ubuntu-build-vm-AUTOINSTALL.iso"
settings = {
    ".encoding": "UTF-8", "config.version": "8", "virtualHW.version": "21",
    "displayName": "LabKita Ubuntu Build", "guestOS": "ubuntu-64",
    "memsize": "6144", "numvcpus": "2", "cpuid.coresPerSocket": "2",
    "firmware": "bios", "bios.bootOrder": "hdd,cdrom",
    "pciBridge0.present": "TRUE", "pciBridge0.pciSlotNumber": "17",
    "pciBridge4.present": "TRUE", "pciBridge4.virtualDev": "pcieRootPort", "pciBridge4.functions": "8",
    "pciBridge5.present": "TRUE", "pciBridge5.virtualDev": "pcieRootPort", "pciBridge5.functions": "8",
    "pciBridge6.present": "TRUE", "pciBridge6.virtualDev": "pcieRootPort", "pciBridge6.functions": "8",
    "pciBridge7.present": "TRUE", "pciBridge7.virtualDev": "pcieRootPort", "pciBridge7.functions": "8",
    "pciBridge4.pciSlotNumber": "21", "pciBridge5.pciSlotNumber": "22",
    "pciBridge6.pciSlotNumber": "23", "pciBridge7.pciSlotNumber": "24",
    "scsi0.pciSlotNumber": "16", "usb.pciSlotNumber": "32",
    "ethernet0.pciSlotNumber": "160", "ehci.pciSlotNumber": "34", "sata0.pciSlotNumber": "35",
    "scsi0.present": "TRUE", "scsi0.virtualDev": "lsilogic",
    "scsi0:0.present": "TRUE", "scsi0:0.fileName": "labkita-build.vmdk",
    "sata0.present": "TRUE", "sata0:0.present": "TRUE",
    "sata0:0.deviceType": "cdrom-image", "sata0:0.fileName": str(iso),
    "sata0:0.startConnected": "TRUE",
    "ethernet0.present": "TRUE", "ethernet0.connectionType": "nat",
    "ethernet0.virtualDev": "e1000e", "ethernet0.addressType": "generated",
    "usb.present": "TRUE", "ehci.present": "TRUE",
    "sound.present": "FALSE", "floppy0.present": "FALSE",
    "mks.enable3d": "FALSE", "svga.autodetect": "TRUE",
    "tools.syncTime": "TRUE", "tools.upgrade.policy": "manual",
    "vmci0.present": "TRUE", "isolation.tools.hgfs.disable": "TRUE",
}
(vm / "labkita-build.vmx").write_text("\n".join(f'{key} = "{value}"' for key, value in settings.items()) + "\n", encoding="utf-8")
(build / "README.txt").write_text(
    "VM build khusus proyek LabKita. Disk virtual baru 80 GB dinamis, RAM 6 GB.\n"
    "Media AUTOINSTALL hanya untuk disk virtual baru VM ini.\n"
    "Untuk INPUT CUBIC, gunakan ISO Ubuntu ASLI dari Downloads, bukan media AUTOINSTALL.\n"
    "Credential lokal ada di builder.credentials.json; jangan unggah folder build ke repositori.\n",
    encoding="utf-8",
)
print("Konfigurasi VM dan hash password siap. Credential tidak dicetak.")
print(vm / "labkita-build.vmx")
