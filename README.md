# LabKita Linux

Distribusi sistem operasi berbasis Ubuntu 24.04 LTS (Noble Numbat) yang dikustomisasi khusus untuk kebutuhan **praktikum pemrograman dasar dan sistem operasi secara luring (*offline*)** di laboratorium komputer kampus tanpa ketergantungan koneksi internet.

Proyek ini dikembangkan sebagai luaran **Final Project Mata Kuliah Sistem Operasi**, Semester Ganjil 2026/2027.  
**Dosen Pengampu:** Muhammad Sidik Asyaky, S.T., M.T.

---

## 1. Identitas Rilis & Checksum ISO

| Atribut | Detail |
| --- | --- |
| **Nama Distro** | LabKita Linux |
| **Versi Rilis** | 0.1 |
| **Basis Sistem** | Ubuntu 24.04.5 LTS Desktop (amd64) |
| **Arsitektur** | x86_64 / amd64 |
| **Nama Berkas ISO** | `labkita-linux-0.1-amd64.iso` |
| **Ukuran Berkas** | 6.493.779.968 bytes (~6.05 GiB) |
| **SHA256 Checksum** | `f80e42c9e8d4db820121f02fca79588760f1549a6cc6634929e3b0e071b810c5` |
| **MD5 Checksum** | `b457376899f24cbd1ee570e0c6edfd25` |
| **Metode Build** | Cubic (*Custom Ubuntu ISO Creator*) pada chroot lingkungan Noble |
| **Status Verifikasi** | Teruji & Lolos Uji VM 100% (14/14 Pengujian) |

### Verifikasi Integritas Berkas
Sebelum mengimpor atau membakar ISO ke media instalasi, lakukan verifikasi integritas berkas:

- **PowerShell (Windows):**
  ```powershell
  Get-FileHash -Algorithm SHA256 .\labkita-linux-0.1-amd64.iso
  # Hash: F80E42C9E8D4DB820121F02FCA79588760F1549A6CC6634929E3B0E071B810C5
  ```

- **Linux / macOS (Bash):**
  ```bash
  sha256sum labkita-linux-0.1-amd64.iso
  # f80e42c9e8d4db820121f02fca79588760f1549a6cc6634929e3b0e071b810c5  labkita-linux-0.1-amd64.iso
  ```

---

## 2. Latar Belakang & Fitur Utama

Laboratorium komputer kampus sering menghadapi masalah koneksi internet yang lambat atau tidak stabil saat praktikum berlangsung. LabKita Linux dirancang agar mahasiswa dan asisten lab dapat menjalankan sesi praktikum secara mandiri tanpa membutuhkan akses repository online.

### Fitur yang Diterapkan:
1. **Toolchain Pemrograman Lengkap (Offline Ready):**
   - **C/C++:** GCC 13.3.0, G++ 13.3.0, GNU Make 4.3, GDB, dan paket `build-essential`.
   - **Python:** Python 3.12.3, modul venv, dan dokumentasi lokal.
   - **Editor & IDE:** Geany 2.0 (terkonfigurasi build command C dan Python), GNU Nano, dan Git 2.43.
   - **Dokumentasi Manual:** `man-db`, `manpages-dev`, serta panduan praktikum lokal di `/usr/share/labkita/guide/index.html`.

2. **Isolasi Keamanan & Manajemen User Praktikan:**
   - Utilitas `/usr/local/sbin/labkita-postinstall` untuk konfigurasi instan akun mahasiswa (`praktikan`).
   - Direktori `/home/praktikan` dilindungi izin akses ketat `0700` (`drwx------`), mencegah akses tidak sah antarpengguna.
   - Akun mahasiswa **tidak memiliki hak `sudo`**, sehingga konfigurasi sistem dan berkas lab aman dari perubahan yang tidak disengaja.

3. **Workspace Temporer Cepat (RAM Disk tmpfs):**
   - Layanan systemd `labkita-runtime.service` otomatis membuat `/run/labkita` berbasis memori RAM (*tmpfs*) dengan sticky bit `1777` (`drwxrwxrwt`).
   - Berkas kompilasi sementara di folder ini akan otomatis terhapus saat reboot, menjaga media penyimpanan lab tetap bersih.

4. **Kustomisasi Tampilan & Identitas Lab:**
   - Wallpaper SVG resmi LabKita terpasang via konfigurasi profil `dconf`.
   - Pintasan panduan dan materi latihan langsung tersedia di desktop dan application launcher.

5. **Suite Diagnostik Mandiri (`labkita-check`):**
   - Perintah terminal `labkita-check` untuk mengecek kesiapan 14 komponen sistem (kompiler, pustaka, perizinan, dan layanan) sebelum praktikum dimulai.

---

## 3. Hasil Pengujian & Tolok Ukur VM

Pengujian dilakukan pada lingkungan mesin virtual VMware Workstation (spesifikasi uji: 2 vCPU, RAM 4096 MB, Disk 40 GB NVMe):

| Pengujian | Perintah / Tolok Ukur | Hasil Pengujian | Status |
| --- | --- | --- | :---: |
| **Self-Diagnostic Suite** | `labkita-check` | 14 dari 14 item uji lulus (0 error) | **LULUS** |
| **Penggunaan Memori (RAM)** | `free -m` | 1.342 MB terpakai / 2.568 MB bebas (Total 3.911 MB) | **TERUKUR** |
| **Waktu Booting Sistem** | `systemd-analyze` | Total 59.98 detik (Kernel 5.31s, Userspace 54.67s) | **TERUKUR** |
| **Isolasi Izin Sudo** | `sudo -l` (user `praktikan`) | Ditolak: user `praktikan` tidak diizinkan menjalankan sudo | **LULUS** |
| **Perizinan Folder Mahasiswa** | `stat /home/praktikan` | Mode `0700` (`drwx------`), hanya pemilik yang dapat mengakses | **LULUS** |
| **Kompilasi & Eksekusi C** | `gcc -O2 hello.c -o hello && ./hello` | Berjalan sukses: *"Halo dari LabKita Linux!"* | **LULUS** |
| **Eksekusi Python Multiprocess** | `python3 processes.py` | Berjalan sukses: fork PID anak berjalan mandiri | **LULUS** |
| **Uji Offline Total** | `nmcli networking off` | Status `connectivity: none`. GCC, Python, man pages tetap 100% normal | **LULUS** |
| **Ruang Kerja Tmpfs** | `ls -ld /run/labkita` | Mode `1777` (`drwxrwxrwt`), reset otomatis setelah reboot | **LULUS** |

*Dokumentasi lengkap dan tangkapan layar pengujian tersedia di folder [`docs/evidence/`](docs/evidence/) dan [`docs/TEST-PLAN.md`](docs/TEST-PLAN.md).*

---

## 4. Panduan Menjalankan ISO di Mesin Virtual

### A. Rekomendasi Spesifikasi VM (VMware / VirtualBox)
- **Tipe Sistem:** Linux → Ubuntu (64-bit)
- **CPU:** Minimal 2 vCPU
- **RAM:** Minimal 4096 MB (4 GB)
- **Penyimpanan:** Minimal 25 GB
- **Display:** Akselerasi 3D aktif, resolusi disarankan minimal 1280×800

### B. Menjalankan Live Session
1. Buat VM baru dan pasang file `labkita-linux-0.1-amd64.iso` pada drive CD/DVD virtual.
2. Nyalakan mesin virtual. Pada bootloader GRUB, pilih **"Try or Install Ubuntu / LabKita"**.
3. Sistem akan memuat desktop LabKita dengan latar belakang kustom dan dock perkakas praktikum.
4. Buka terminal (`Ctrl + Alt + T`) lalu jalankan verifikasi:
   ```bash
   labkita-check
   ```
5. Buka editor Geany dari panel untuk mulai mengerjakan kode C atau skrip Python.

### C. Menyiapkan Akun Praktikan (Opsional untuk Instalasi Fisik)
Jika sistem dipasang permanen pada PC laboratorium, siapkan akun mahasiswa dengan:
```bash
sudo labkita-postinstall praktikan
```
Skrip akan membuat user `praktikan`, mengatur perizinan folder privat, dan mengisi direktori `~/Praktikum` dengan contoh kode awal (`hello.c`, `hello.py`, `processes.py`).

---

## 5. Anggota Tim & Pembagian Tugas

| No | Nama | NPM | Peran | Tugas & Kontribusi |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Dafa Zahran** | **257006111188** | Ketua Kelompok & Integrasi Build | Koordinasi proyek, pipeline mastering ISO via Cubic, manajemen repositori GitHub, dan integrasi rilis akhir. |
| 2 | **Rafly Fauzi Pratama** | **257006111152** | Pengembang Inti & Toolchain | Penyusunan skrip kustomisasi Cubic (`customize.sh`), konfigurasi compiler GCC/G++, Python, Geany IDE, serta pembuatan suite `labkita-check`. |
| 3 | **Muhammad Ilham Rizky** | **257006111154** | Sistem, Keamanan & QA | Implementasi unit systemd tmpfs (`labkita-runtime.service`), skrip isolasi non-sudo (`labkita-postinstall`), serta eksekusi benchmark performa VM. |
| 4 | **Vadien Athallah Lukman** | **257006111160** | UI/UX, Dokumentasi & Media | Desain wallpaper SVG dan branding desktop, penyusunan materi latihan praktikum, laporan akhir proyek (PDF), slide presentasi (PPTX), dan naskah demo. |

---

## 6. Struktur Direktori Repositori

```text
labkita-linux/
├── config/
│   └── packages.txt             # Daftar paket esensial tambahan
├── dist/
│   ├── labkita-kit.tar.gz       # Arsip payload untuk injeksi Cubic
│   ├── labkita-linux-0.1-amd64.iso.md5      # Checksum MD5 berkas ISO
│   └── labkita-linux-0.1-amd64.iso.sha256   # Checksum SHA256 berkas ISO
├── docs/
│   ├── BUILD-CUBIC.md           # Prosedur pembuatan ISO dengan Cubic
│   ├── DEMO-SCRIPT.md           # Naskah video demonstrasi
│   ├── LAPORAN-PROYEK-LABKITA.pdf # Laporan lengkap proyek akhir (PDF)
│   ├── TEST-PLAN.md             # Matriks pengujian & hasil tolok ukur
│   ├── VM-BUILD.md              # Konfigurasi VM lingkungan build
│   ├── evidence/                # Tangkapan layar bukti pengujian di VM
│   └── presentation/            # Slide presentasi proyek akhir (PPTX)
├── payload/                     # Berkas kustomisasi sistem
│   ├── etc/
│   │   ├── dconf/db/local.d/    # Konfigurasi wallpaper dan desktop
│   │   └── systemd/system/      # Unit layanan labkita-runtime.service
│   └── usr/
│       ├── local/bin/           # Skrip pengujian `labkita-check`
│       ├── local/sbin/          # Skrip pembuatan user `labkita-postinstall`
│       └── share/labkita/       # Panduan HTML offline dan contoh kode
├── scripts/
│   └── customize.sh             # Skrip kustomisasi utama di chroot
├── tools/
│   ├── create-build-media.sh    # Generator media autoinstall VM build
│   ├── generate_report_pdf.py   # Generator laporan proyek PDF
│   ├── generate_slides.py       # Generator slide presentasi PPTX
│   ├── pack.py                  # Skrip pembuat arsip kit
│   ├── prepare-build-vm.py      # Otomasi provisioning VM build
│   ├── test_runner.py           # Otomasi pengujian VM via VNC
│   └── vmctl.py                 # Utilitas kontrol VMware
└── README.md
```

---

## 7. Lisensi

- Kustomisasi dan skrip konfigurasi LabKita dirilis di bawah [MIT License](LICENSE).
- Komponen upstream Ubuntu, kernel Linux, GCC, Python, Geany, dan pustaka pendukung tetap tunduk pada lisensi aslinya masing-masing (GPL, LGPL, PSF, dll.).
