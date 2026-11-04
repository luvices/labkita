# VM build proyek

Lokasi konfigurasi: `build/vm/labkita-build.vmx`.
Nama di VMware: **LabKita Ubuntu Build**.
Alokasi: RAM 6 GB, 2 CPU, disk virtual dinamis 80 GB di drive D.
Jaringan NAT. VM lain tetap memakai konfigurasi masing-masing.

Media `build/ubuntu-build-vm-AUTOINSTALL.iso` hanya dibuat untuk menyiapkan
VM build dengan disk virtual baru. Jangan gunakan sebagai produk final atau
sebagai input Cubic. Input Cubic adalah ISO Ubuntu asli dari Downloads.

Akun `builder` adalah akun pengelola lingkungan build. Password acak ada di
`build/builder.credentials.json`. Akun ini mendapat sudo tanpa password
khusus dalam VM build agar pekerjaan build dapat diotomatisasi. Folder `build/`
diabaikan Git. Akun/credential ini tidak disalin oleh kit ke ISO final.

Helper lokal dari folder proyek:

```powershell
python tools/vmctl.py status
python tools/vmctl.py ip
```

Perintah guest baru bekerja setelah Ubuntu terinstal dan VMware Tools aktif.
`unknown` selama sesi installer belum berarti instalasi gagal.

Skrip `tools/guest-setup-build.sh` hanya berjalan sebagai root di VM build
dengan marker `/var/lib/labkita-build-vm-ready`. Skrip memasang Cubic dan
menyimpan log di `/var/log/labkita-cubic-setup.log`.

ISO asli sudah diperiksa terhadap:
https://releases.ubuntu.com/24.04.5/SHA256SUMS

SHA256:
`4da4a0c9035da8e68a59a838674f403f0a54472c78a83b4fb7f78d03588f85a7`.

Keberhasilan menyiapkan VM build bukan bukti bahwa ISO LabKita final sudah
berhasil dibuat atau diinstal. Status dan hasil pengujian harus dicatat
berdasarkan hasil nyata.
