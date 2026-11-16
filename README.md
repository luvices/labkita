# LabKita Linux

Distribusi sistem operasi berbasis Ubuntu 24.04 LTS (Noble Numbat) yang dikustomisasi khusus untuk kebutuhan **praktikum pemrograman dasar dan sistem operasi secara luring (*offline*)** di laboratorium komputer kampus tanpa ketergantungan koneksi internet.

Proyek ini dikembangkan sebagai luaran **Final Project Mata Kuliah Sistem Operasi**, Semester Ganjil 2026/2027.  
**Dosen Pengampu:** Muhammad Sidik Asyaky, S.T., M.T.

---

## 1. Identitas Rilis & Checksum ISO

| Atribut | Detail |
| --- | --- |
| **Nama Distro** | LabKita Linux |
| **Versi Rilis** | 0.2 |
| **Basis Sistem** | Ubuntu 24.04.5 LTS Desktop (amd64) |
| **Arsitektur** | x86_64 / amd64 |
| **Nama Berkas ISO** | `labkita-linux-0.2-amd64.iso` |
| **Ukuran Berkas** | 6.519.777.280 bytes (~6.07 GiB / 6.52 GB) |
| **SHA256 Checksum** | `ae6391a26d3497cb9d9aed4d9e967352e46adfd630202ac47c58b149d8000d19` |
| **MD5 Checksum** | `e0f73c691ffd65f1c0108f60834d15f4` |
| **Metode Build** | Cubic (*Custom Ubuntu ISO Creator*) `2026.09.110-release~202609120048~ubuntu24.04.1` |
| **Status Verifikasi** | Teruji pascainstalasi di VM (`21/21` cek `labkita-check` lulus; ada kegagalan GUI installer, `labkita-postinstall` baris 45 di ISO, & `labkita-guide` Firefox Snap — lihat [`docs/TEST-PLAN.md`](docs/TEST-PLAN.md)) |

### Verifikasi Integritas Berkas
Sebelum mengimpor atau membakar ISO ke media instalasi, lakukan verifikasi integritas berkas:

- **PowerShell (Windows):**
  ```powershell
  Get-FileHash -Algorithm SHA256 .\labkita-linux-0.2-amd64.iso
  # Hash: AE6391A26D3497CB9D9AED4D9E967352E46ADFD630202AC47C58B149D8000D19
  ```

- **Linux / macOS (Bash):**
  ```bash
  sha256sum labkita-linux-0.2-amd64.iso
  # ae6391a26d3497cb9d9aed4d9e967352e46adfd630202ac47c58b149d8000d19  labkita-linux-0.2-amd64.iso
  ```

---

## 2. Latar Belakang & Fitur Utama

Laboratorium komputer kampus sering menghadapi masalah koneksi internet yang lambat atau tidak stabil saat praktikum berlangsung. LabKita Linux dirancang agar mahasiswa dan asisten lab dapat menjalankan sesi praktikum secara mandiri tanpa membutuhkan akses repository online.

### Fitur yang Diterapkan di Versi 0.2:
1. **Lokalisasi Penuh Bahasa Indonesia (dengan Catatan Sisa Metadata):**
   - Integrasi paket bahasa lengkap: `language-pack-id`, `language-pack-gnome-id`, `hunspell-id`, dan `firefox-locale-id`.
   - Konfigurasi default sistem: Locale `id_ID.UTF-8`, zona waktu `Asia/Jakarta` (WIB), dan tata letak papan tik `us` (QWERTY standar laboratorium).
   - Bootloader GRUB terkonfigurasi dengan parameter `locale=id_ID.UTF-8`, dan desktop/terminal terinstal tampil dalam Bahasa Indonesia penuh. *(Catatan audit: layar sambutan pertama & daftar sumber Subiquity masih menyisakan label lama `"LabKita Linux 0.1"`, dan sesi live tetap memunculkan wizard `gnome-initial-setup` karena autologin `labkita` tidak aktif.)*
   - Penerjemahan seluruh teks utilitas mandiri: `labkita-check`, `labkita-postinstall`, dan launcher panduan.

2. **Antarmuka Modern Bergaya macOS (100% Bebas Aset Proprietary Apple):**
   - Menggunakan tema sumber terbuka berlisensi resmi: **WhiteSur GTK Theme** (Light & Dark) dan **WhiteSur Icon Theme** karya vinceliuice (lisensi GPL-3.0 / CC-BY-SA-4.0).
   - Tema kursor bergaya macOS halus (**WhiteSur Cursors**) dan tipografi **Inter Font** (`fonts-inter`) yang nyaman dibaca untuk coding.
   - Tata letak desktop: Dock terpusat di bagian bawah layar (*centered bottom dock*), tombol kontrol jendela di sebelah kiri (`close,minimize,maximize:`), sudut jendela membulat, dan *top bar* bersih.
   - Wallpaper orisinal LabKita gradien minimalis (format SVG & PNG 4K). Seluruh atribusi lisensi didokumentasikan di [`docs/CREDITS.md`](docs/CREDITS.md).

3. **Toolchain Pemrograman Lengkap (Offline Ready):**
   - **C/C++:** GCC 13.3.0, G++ 13.3.0, GNU Make 4.3, GDB, dan paket `build-essential`.
   - **Python:** Python 3.12.3, modul venv, dan dokumentasi pustaka offline.
   - **Editor & IDE:** Geany 2.0 (terkonfigurasi build shortcut C dan Python), GNU Nano, dan Git 2.43.
   - **Dokumentasi Manual:** `man-db`, `manpages-dev`, serta panduan praktikum lokal offline di `/usr/share/labkita/guide/`.
   - **Kendala Browser Snap pada `labkita-guide` (Terbuka):** Skrip `labkita-guide` menyalin panduan ke `~/.local/share/labkita/guide/`, namun pada uji sistem terinstal 0.2 Firefox Snap masih memblokir akses dotfolder tersebut (*"Akses terhadap berkas ditolak"*). Di rilis berikutnya perlu dipindah ke folder non-tersembunyi (misal `~/Panduan`) atau disajikan lewat server HTTP lokal.

4. **Isolasi Keamanan & Manajemen User Praktikan:**
   - Utilitas `/usr/local/sbin/labkita-postinstall` untuk konfigurasi instan akun mahasiswa (`praktikan`). *(Catatan audit ISO 0.2: user & password berhasil dibuat, tetapi baris 45 gagal mencetak ringkasan dengan error `printf: - : pilihan tidak valid`; perbaikan `printf --` sudah masuk source repo untuk rebuild ISO berikutnya.)*
   - Direktori `/home/praktikan` dilindungi izin akses ketat `0700` (`drwx------`), mencegah akses tidak sah antarmahasiswa.
   - Akun mahasiswa **tidak memiliki hak `sudo`**, sehingga konfigurasi sistem dan berkas lab aman dari perusakan yang tidak disengaja.

5. **Workspace Temporer Cepat (RAM Disk tmpfs):**
   - Layanan systemd `labkita-runtime.service` otomatis membuat `/run/labkita` berbasis memori RAM (*tmpfs*) dengan sticky bit `1777` (`drwxrwxrwt`).
   - Berkas kompilasi sementara di folder ini akan otomatis terhapus saat reboot, menjaga media penyimpanan lab tetap bersih.

6. **Suite Diagnostik Mandiri Diperluas (`labkita-check`):**
   - Memeriksa 21 komponen kesiapan sistem (kompiler, pustaka, locale, timezone, tema GTK, ikon, kursor, wallpaper, tmpfs, dan layanan runtime) — **21/21 `[LULUS]`** pada sistem terinstal *(catatan: skrip mengecek keberadaan file panduan, belum memvalidasi pembukaan via Firefox Snap)*.

---

## 3. Hasil Pengujian & Tolok Ukur Empiris

Pengujian empiris dilakukan ulang **setelah instalasi penuh ke disk kosong** pada VMware Workstation dalam **kondisi identik** (VM `labkita-test.vmx`: 2 vCPU, RAM 4096 MB / `3911 MiB` usable, Disk 40 GB SCSI, **3 kali reboot bersih per versi**, pengukuran 20 detik setelah desktop siap):

| Pengujian | Perintah / Tolok Ukur | Hasil LabKita 0.1 (Terinstal) | Hasil LabKita 0.2 (Terinstal) | Status |
| --- | --- | :---: | :---: | :---: |
| **Boot Menu GRUB** | Layar GRUB 2.12 | Bahasa Indonesia | Bahasa Indonesia | **LULUS** |
| **Autologin Live Session** | Live boot tanpa wizard | Jatuh ke `gnome-initial-setup` | Jatuh ke `gnome-initial-setup` | **GAGAL** |
| **Installer GUI** | `ubuntu-desktop-bootstrap` | Gagal (*Something went wrong*) | Gagal (*Ada yang salah* / md5check) | **GAGAL** |
| **Instalasi ke Disk** | `subiquity.cmd.tui` | Sukses hingga reboot | **Sukses hingga reboot** *(sisa label 0.1)* | **LULUS (Fallback)** |
| **Self-Diagnostic Suite** | `labkita-check` | 14/14 Lulus | **21/21 Lulus** *(cek berbasis file)* | **LULUS** |
| **Penggunaan Memori (RAM)** | `free -m` (rata-rata 3x) | **1.031,7 MiB** (`1025/1030/1040`) | **1.060,0 MiB** (`1063/1053/1064`) *(+28,3 MiB / +2,7%)* | **TERUKUR** |
| **Waktu Booting Sistem** | `systemd-analyze time` (rata-rata 3x) | **9,893 detik** (`10.44s/9.49s/9.75s`) | **11,454 detik** (`9.58s/13.66s/11.12s`) *(+1,561s / +15,8% lebih lambat)* | **TERUKUR** |
| **Bahasa Antarmuka Desktop** | Desktop & utilitas pasca-install | Campuran Inggris/Prancis di GUI | **Bahasa Indonesia** (`Berkas`, panel, terminal) | **LULUS** |
| **Tampilan Tema WhiteSur** | Desktop & `Berkas` | Default Yaru | **WhiteSur GTK, Ikon WhiteSur, Dock Tengah, Left Buttons** | **LULUS** |
| **Pembuatan Akun Praktikan** | `sudo labkita-postinstall praktikan` | Lulus | **Akun terbuat, tetapi error `printf` baris 45 di ISO 0.2** | **GAGAL PARSIAL** |
| **Isolasi Akun & Izin 0700** | `id`, `stat`, `ls /home/praktikan`, `grep sudo` | Ditolak / `0700` | **`0700`, `Ijin ditolak`, `praktikan` non-`sudo`** | **LULUS** |
| **Akses Panduan Firefox Snap** | `labkita-guide` | Terblokir `/usr/share` | **Masih terblokir di `~/.local` (*Akses terhadap berkas ditolak*)** | **GAGAL** |
| **Kompilasi & Eksekusi Offline** | `nmcli networking off`, `gcc`, `python3` | Lulus | **Lulus: C, Python, & `processes.py` berjalan offline** | **LULUS** |
| **Ruang Kerja Tmpfs** | `/run/labkita` (`1777`) | Mode `1777` | **Mode `1777` aktif** | **LULUS** |

> **Catatan Analisis Kinerja Empiris (Tanpa Klaim Lebih Ringan/Cepat):**  
> Pada pengujian ulang yang adil setelah instalasi ke disk (3x pengukuran per versi di VM identik), **LabKita 0.2 tidak lebih cepat maupun lebih ringan daripada 0.1**: konsumsi RAM rata-rata naik **+28,3 MiB (+2,7%)** dari `1.031,7 MiB` ke `1.060,0 MiB`, sedangkan waktu boot total rata-rata lebih lambat dan lebih fluktuatif (`11,454 detik` vs `9,893 detik` pada 0.1, +15,8%). Penambahan tema WhiteSur GTK, set ikon, dan ekstensi Dash-to-Dock wajar memberi sedikit overhead, sementara sisa RAM tersedia rata-rata **2.850,7 MiB** tetap sangat memadai untuk kompilasi dan IDE praktikum.

*Dokumentasi lengkap hasil audit, kegagalan nyata, dan 15 tangkapan layar VM asli tersedia di [`docs/evidence/`](docs/evidence/) dan [`docs/TEST-PLAN.md`](docs/TEST-PLAN.md).*

---

## 4. Panduan Menjalankan ISO di Mesin Virtual

### A. Rekomendasi Spesifikasi VM (VMware / VirtualBox)
- **Tipe Sistem:** Linux → Ubuntu (64-bit)
- **CPU:** Minimal 2 vCPU
- **RAM:** Minimal 4096 MB (4 GB)
- **Penyimpanan:** Minimal 25 GB
- **Display:** Akselerasi 3D aktif, resolusi disarankan minimal 1280×800

### B. Menjalankan Live Session
1. Buat VM baru dan pasang file `labkita-linux-0.2-amd64.iso` pada drive CD/DVD virtual.
2. Nyalakan mesin virtual. Pada bootloader GRUB, pilih **"Coba atau Pasang LabKita Linux (Bahasa Indonesia)"**.
3. Sistem akan memuat desktop LabKita dengan bahasa Indonesia, dock terpusat, dan perkakas praktikum siap pakai.
4. Buka terminal (`Ctrl + Alt + T`) lalu jalankan verifikasi:
   ```bash
   labkita-check
   ```
5. Buka editor Geany dari dock untuk mulai mengerjakan program C atau Python.

### C. Menyiapkan Akun Praktikan (Instalasi Fisik Lab)
Jika sistem dipasang permanen pada PC laboratorium, siapkan akun mahasiswa dengan:
```bash
sudo labkita-postinstall praktikan
```
Skrip akan membuat user `praktikan`, mengunci hak sudo, mengatur izin folder privat `0700`, dan mengisi direktori `~/Praktikum` dengan modul latihan serta menyinkronkan panduan offline.

---

## 5. Anggota Tim & Pembagian Tugas

| No | Nama | NPM | Peran | Tugas & Kontribusi |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Dafa Zahran** | **257006111188** | Ketua Kelompok & Integrasi Build | Koordinasi proyek, pipeline mastering ISO via Cubic, manajemen repositori GitHub, integrasi rilis v0.2, dan orkestrasi pengujian VM. |
| 2 | **Rafly Fauzi Pratama** | **257006111152** | Pengembang Inti & Toolchain | Pembuatan skrip kustomisasi Cubic (`customize.sh`), perbaikan lokalisasi Bahasa Indonesia (`id_ID.UTF-8`), konfigurasi compiler GCC/G++, Python, Geany IDE, serta pengembangan suite `labkita-check`. |
| 3 | **Muhammad Ilham Rizky** | **257006111154** | Sistem, Keamanan & QA | Implementasi unit systemd tmpfs (`labkita-runtime.service`), skrip isolasi non-sudo (`labkita-postinstall`), perbaikan launcher Firefox Snap, serta eksekusi benchmark empiris RAM & boot time VM. |
| 4 | **Vadien Athallah Lukman** | **257006111160** | UI/UX, Dokumentasi & Media | Integrasi tema WhiteSur GTK & ikon, tipografi Inter font, desain wallpaper orisinal gradien LabKita, penyusunan laporan akhir proyek (PDF), slide presentasi (PPTX), dan naskah demo. |

Panduan alur kerja tim, konvensi commit, dan pembagian tugas GitHub Issue tersedia di [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) dan [`docs/issues/`](docs/issues/).

---

## 6. Struktur Direktori Repositori

```text
labkita-linux/
├── config/
│   └── packages.txt             # Daftar paket esensial tambahan
├── dist/
│   ├── labkita-kit.tar.gz       # Arsip payload untuk injeksi Cubic
│   ├── labkita-linux-0.2-amd64.iso.md5      # Checksum MD5 berkas ISO
│   └── labkita-linux-0.2-amd64.iso.sha256   # Checksum SHA256 berkas ISO
├── docs/
│   ├── BUILD-CUBIC.md           # Prosedur pembuatan ISO dengan Cubic
│   ├── CONTRIBUTING.md          # Panduan kolaborasi & konvensi commit git
│   ├── CREDITS.md               # Atribusi lisensi tema, ikon, font, wallpaper
│   ├── DEMO-SCRIPT.md           # Naskah video demonstrasi
│   ├── LAPORAN-PROYEK-LABKITA.pdf # Laporan lengkap proyek akhir (PDF)
│   ├── TEST-PLAN.md             # Matriks pengujian & hasil tolok ukur empiris
│   ├── VM-BUILD.md              # Konfigurasi VM lingkungan build
│   ├── evidence/                # Tangkapan layar bukti pengujian di VM
│   ├── issues/                  # Template pembagian tugas GitHub Issue
│   └── presentation/            # Slide presentasi proyek akhir (PPTX)
├── payload/                     # Berkas kustomisasi sistem
│   ├── etc/
│   │   ├── dconf/db/local.d/    # Konfigurasi dconf (dock, tema, buttons)
│   │   ├── default/             # Konfigurasi default locale & keyboard
│   │   └── systemd/system/      # Unit layanan labkita-runtime.service
│   └── usr/
│       ├── local/bin/           # Skrip `labkita-check` & `labkita-guide`
│       ├── local/sbin/          # Skrip pembuatan user `labkita-postinstall`
│       └── share/labkita/       # Panduan HTML offline dan contoh kode
├── scripts/
│   └── customize.sh             # Skrip kustomisasi utama di chroot
├── tools/
│   ├── generate_report_pdf.py   # Generator laporan proyek PDF
│   ├── generate_slides.py       # Generator slide presentasi PPTX
│   ├── pack.py                  # Skrip pembuat arsip kit
│   ├── test_runner.py           # Otomasi pengujian VM via VNC
│   └── vmctl.py                 # Utilitas kontrol VMware
└── README.md
```

---

## 7. Lisensi

- Kustomisasi dan skrip konfigurasi LabKita dirilis di bawah [MIT License](LICENSE).
- Komponen tema visual WhiteSur, ikon, dan kursor tunduk pada lisensi aslinya masing-masing (GPL-3.0 / CC-BY-SA-4.0).
- Komponen upstream Ubuntu, kernel Linux, GCC, Python, Geany, dan pustaka pendukung tetap tunduk pada lisensi aslinya masing-masing (GPL, LGPL, PSF, dll.). Atribusi lengkap tercantum pada [`docs/CREDITS.md`](docs/CREDITS.md).
