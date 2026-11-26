# Rencana dan Hasil Pengujian LabKita Linux 0.6

Dokumen ini mencatat verifikasi resmi dan hasil pengujian nyata **LabKita Linux 0.6** (`labkita-linux-0.6-amd64.iso`, dibangun di WSL lewat [`tools/build_v06.py`](../tools/build_v06.py) dari basis resmi Ubuntu 24.04.5 LTS Desktop). Seluruh tangkapan layar pada [`docs/evidence/`](evidence/) berasal dari pengujian nyata di VMware Workstation.

## 1. Integritas Berkas & Validasi Kode Lokal

- **Berkas ISO Final:** `labkita-linux-0.6-amd64.iso` berukuran `6.083.305.472 bytes` (~5,67 GiB).
- **SHA256:** `78a58f0f757b63b97b46e21a520a2c2ea7a205458119192c8f4ed10d2fe9bde1` ([`dist/labkita-linux-0.6-amd64.iso.sha256`](../dist/labkita-linux-0.6-amd64.iso.sha256))
- **MD5:** `7db00f4c1bfbdf06df62c77bfd0e14c7` ([`dist/labkita-linux-0.6-amd64.iso.md5`](../dist/labkita-linux-0.6-amd64.iso.md5))
- **Verifikasi Loop-Mount ISO (`md5sum.txt`):** `MD5SUM_ALL_OK` (mengecualikan `boot.catalog` dan `./boot/grub/i386-pc/eltorito.img` yang diperbarui oleh `xorriso --grub2-boot-info`).
- **Validasi Skrip & Payload (`bash tools/verify-linux.sh`):** **LULUS** (pemeriksaan sintaks Bash/Python, contoh kode praktikum `hello.py`/`processes.py`/`thread_demo.py`, dan validasi `systemd-analyze verify` pada `labkita-runtime.service`).

## 2. Pengujian Nyata di VMware Workstation (Rilis 0.6)

Lingkungan uji: VMware Workstation, disk virtual kosong 40 GB, RAM 6144 MB (`5921 MiB` terbaca kernel Linux `7.0.0-44-generic`), 2 vCPU, adaptor jaringan NAT aktif.

| Skenario Uji | Hasil Aktual pada VM 0.6 | Status | Bukti |
| :--- | :--- | :---: | :--- |
| **GRUB & Autoinstall Nol-Langkah (`nocloud`)** | Menu GRUB default (`Pasang Otomatis LabKita Linux 0.6 (Admin + Praktikan)`) menyelesaikan instalasi ke disk tanpa input manual dalam ~4 menit, melewati bug render wizard | **LULUS** | [`0.6-01-grub-autoinstall.png`](evidence/0.6-01-grub-autoinstall.png), [`0.6-02-autoinstall-progress.png`](evidence/0.6-02-autoinstall-progress.png) |
| **Splash Boot Plymouth & Layar Login GDM** | Splash boot Plymouth dan layar login GDM menampilkan logo **Keystone LK** LabKita; daftar akun langsung memuat **LabKita Admin** (`labkita`) dan **praktikan** | **LULUS** | [`0.6-03-plymouth-logo.png`](evidence/0.6-03-plymouth-logo.png), [`0.6-04-gdm-dual-accounts.png`](evidence/0.6-04-gdm-dual-accounts.png) |
| **Desktop Admin & Kelengkapan Ikon WhiteSur** | Login `labkita` masuk ke desktop wallpaper **Cobalt Architectural Slate** tanpa popup GNOME Initial Setup atau upgrade; App Grid dan Settings menampilkan seluruh ikon utuh tanpa symlink rusak | **LULUS** | [`0.6-05-desktop-labkita.png`](evidence/0.6-05-desktop-labkita.png), [`0.6-06-app-grid-icons.png`](evidence/0.6-06-app-grid-icons.png), [`0.6-07-settings-icons.png`](evidence/0.6-07-settings-icons.png) |
| **Diagnostik `labkita-check` (25 Pemeriksaan)** | Seluruh 25 pemeriksaan mencetak `[LULUS]` dan `SEMUA PEMERIKSAAN LULUS`, mencakup toolchain, `tmpfs` `/run/labkita` (`1777`), `labkita-runtime.service`, logo GDM, dan akses Firefox Snap (`AppArmor OK`) | **LULUS** | [`0.6-11-labkita-check-pass.png`](evidence/0.6-11-labkita-check-pass.png) |
| **Buku Kerja 7 Modul (`labkita-guide`)** | Terbuka di Firefox Snap via `file:///.../Dokumen/Panduan-LabKita/index.html` tanpa blokir AppArmor; audit Edge/Selenium mengonfirmasi `no_overflow=True` di `1280x800` dan `390x844` CDP, `0` error konsol, tombol salin & progres `localStorage` aktif, serta kontras >= `4,62:1` | **LULUS** | [`0.6-08-guide-workbook-firefox.png`](evidence/0.6-08-guide-workbook-firefox.png) |
| **Isolasi & Toolchain Akun `praktikan`** | `stat /home/praktikan` = `700`, `uid=1001` pada grup `labkita-praktikum`, `sudo -n true` ditolak, dan kompilasi `gcc ~/Praktikum/hello.c` serta `python3 ~/Praktikum/thread_demo.py` berjalan sukses luring | **LULUS** | [`0.6-09-praktikan-isolation.png`](evidence/0.6-09-praktikan-isolation.png), [`0.6-10-praktikan-offline-compile.png`](evidence/0.6-10-praktikan-offline-compile.png) |

## 3. Observasi Sumber Daya & Catatan VMware Workstation

- **Observasi Pasca-Autoinstall (1x pada VM 6 GB RAM):** Perintah `free -m` mencatat penggunaan `1.076 MiB` (`4.844 MiB` tersedia dari total `5.921 MiB`), `systemd-analyze` mencatat `22,207s` (`3,610s` kernel + `18,597s` userspace), dan pemakaian disk root `/` tercatat `11 GB / 40 GB`. Angka ini adalah observasi tunggal pada konfigurasi 6 GB RAM dan tidak digunakan sebagai klaim perbandingan kecepatan/efisiensi terhadap rilis dasar sebelumnya.
- **Konfigurasi VMware Workstation GUI:**
  - Saat membuat mesin virtual baru, pilih **"I will install the operating system later."** agar fitur *Easy Install* VMware tidak menimpa seed `autoinstall` `nocloud` LabKita.
  - Setelah autoinstall selesai dan reboot ke disk, nonaktifkan centang **Connect at power on** pada CD/DVD dan aktifkan **Display -> Accelerate 3D graphics**. Jika layar hitam masih terjadi pada sesi Wayland di host tertentu, pilih **Ubuntu on Xorg** pada ikon gerigi kanan bawah di layar login GDM.
