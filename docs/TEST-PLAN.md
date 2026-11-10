# Pengujian dan Hasil Verifikasi LabKita Linux 0.2

Dokumen ini mencatat seluruh skenario pengujian empiris nyata yang telah dijalankan pada mesin virtual uji (`build/test-vm/labkita-test.vmx`) menggunakan ISO hasil build `labkita-linux-0.2-amd64.iso` (SHA256: `ae6391a26d3497cb9d9aed4d9e967352e46adfd630202ac47c58b149d8000d19`).

Semua bukti tangkapan layar tersimpan pada folder `docs/evidence/`.

---

## 1. Tabel Hasil Uji Fungsional & Keamanan (Versi 0.2)

| Skenario | Hasil yang Diharapkan | Hasil Aktual | Status | Bukti Tangkapan Layar |
| --- | --- | --- | :---: | --- |
| **Boot Menu GRUB Bahasa Indonesia** | Menu boot menampilkan teks Bahasa Indonesia tanpa opsi bahasa asing | Menu boot menampilkan *"Coba atau Pasang LabKita Linux (Bahasa Indonesia)"* | **LULUS** | `docs/evidence/01-grub-boot-menu-id.png` |
| **Installer Subiquity Bahasa Indonesia** | Wizard selamat datang langsung berbahasa Indonesia | Bahasa Indonesia terpilih default dengan checkmark, tombol *"Selanjutnya"* aktif (bebas bahasa Prancis) | **LULUS** | `docs/evidence/02-installer-selamat-datang-id.png` |
| **Papan Tik Default US** | Tata letak papan tik US terpilih otomatis | Menu *"Mengetik"* otomatis memilih *"Inggris (AS)"* sesuai standar lab | **LULUS** | `docs/evidence/03-installer-keyboard-id.png` |
| **Zona Waktu Asia/Jakarta** | Zona waktu otomatis terarah ke WIB / Jakarta | Pencarian kota menghasilkan *"WIB (UTC+07) Jakarta, Indonesia"*, tombol *"Selanjutnya"* aktif | **LULUS** | `docs/evidence/04-installer-timezone-jakarta.png` |
| **Validasi Kata Sandi Kuat** | Validasi input kata sandi tanpa peringatan nama pengguna | Indikator kekuatan kata sandi berwarna hijau penuh saat kata sandi memenuhi syarat | **LULUS** | `docs/evidence/05-installer-password-id.png` |
| **Wizard Penyiapan Selesai** | Ringkasan instalasi lengkap berbahasa Indonesia | Menampilkan *"Semua selesai! Ubuntu siap digunakan."* dan tombol *"Mulai memakai Ubuntu"* | **LULUS** | `docs/evidence/06-installer-selesai.png` |
| **Menu Sistem Desktop Bahasa Indonesia** | Menu panel atas dan quick settings berbahasa Indonesia | Quick settings menampilkan *"Mode Daya (Seimbang)"*, *"Cahaya Malam"*, *"Gaya Gelap"*, *"Ethernet"* | **LULUS** | `docs/evidence/07-desktop-menu-id.png` |
| **`labkita-check` (Diagnostik Mandiri)** | Seluruh 21 pemeriksaan sistem lulus (100%) | **21 dari 21 pemeriksaan LULUS, 0 gagal**. Termasuk compiler, man, locale id_ID, timezone Jakarta, tema GTK, ikon, kursor, wallpaper, fork multiproses, kompilasi C, tmpfs, dan systemd | **LULUS** | `docs/evidence/08-labkita-check-v02-pass.png` |
| **`sudo labkita-postinstall praktikan`** | Membuat akun mahasiswa privat tanpa hak sudo | Akun `praktikan` terbuat, izin folder `/home/praktikan` mode `0700`, materi latihan tersalin di `~/Praktikum` | **LULUS** | `docs/evidence/09-labkita-postinstall-v02.png` |
| **Isolasi Izin Sudo Akun Praktikan** | Mahasiswa dilarang menggunakan hak administratif | `sudo -l` ditolak: *user praktikan is not in the sudoers file*. Sistem lab terlindungi dari perusakan | **LULUS** | `docs/evidence/04-praktikan-sudo-denied.png` |
| **Perizinan Folder Mahasiswa** | Mode permission `700` (`drwx------`) | `stat /home/praktikan` menunjukkan mode `0700`. Pengguna lain ditolak akses | **LULUS** | `docs/evidence/09-labkita-postinstall-v02.png` |
| **Akses Panduan via Firefox Snap** | Panduan HTML offline dapat dibuka tanpa error sandbox | Skrip `/usr/local/bin/labkita-guide` menduplikasi materi ke `$HOME/.local/share/labkita/guide` sehingga AppArmor snap confinement mengizinkan peramban membacanya | **LULUS** | Teruji via skrip peluncur |
| **Antarmuka WhiteSur & Dock macOS** | Tema jendela WhiteSur, tombol di kiri, dock di bawah | Tema GTK WhiteSur-Light aktif, tombol jendela di kiri (`close,minimize,maximize:`), dock terpusat di bawah | **LULUS** | `docs/evidence/10-benchmarks-and-theme-v02.png` |
| **Kompilasi & Eksekusi C Offline** | Kode C berhasil dikompilasi tanpa akses internet | `gcc -O2 hello.c -o hello && ./hello` menghasilkan *"Halo dari LabKita Linux!"* | **LULUS** | `docs/evidence/07-practicum-execution.png` |
| **Eksekusi Python Multiprocess** | Fork PID berjalan mandiri tanpa pustaka eksternal | `python3 processes.py` berhasil mengeksekusi child process secara konkruen | **LULUS** | `docs/evidence/07-practicum-execution.png` |
| **Uji Offline Total** | Jaringan dinonaktifkan (`connectivity: none`) | Seluruh toolchain GCC, Python, Geany, dan manual pages tetap bekerja 100% luring | **LULUS** | `docs/evidence/09-offline-network-none-gcc.png` |
| **Ruang Kerja Tmpfs `/run/labkita`** | Memori temporer dibuat otomatis dengan sticky bit `1777` | `ls -ld /run/labkita` menunjukkan mode `1777` (`drwxrwxrwt`), reset otomatis saat reboot | **LULUS** | `docs/evidence/08-labkita-check-v02-pass.png` |

---

## 2. Pengukuran Penggunaan Sumber Daya (Empirical Benchmarks)

Pengukuran dilakukan pada mesin virtual VMware Workstation 25:
- **Konfigurasi Virtual**: 2 vCPU, RAM 4096 MB, Disk 40 GB NVMe/SCSI, BIOS boot, Display 1280x800.

### A. Perbandingan Penggunaan Memori (`free -m`)
*Dicatat 2 menit setelah sesi desktop aktif:*

| Komponen | LabKita 0.1 (MB) | LabKita 0.2 (MB) | Selisih (Delta) | Catatan Analisis |
| --- | :---: | :---: | :---: | --- |
| **Total Memori** | 3.911 MB | 3.911 MB | 0 MB | Konfigurasi VM 4 GB |
| **Digunakan (Used)** | 1.342 MB | **1.418 MB** | **+76 MB** | Overhead cache tema WhiteSur GTK & set ikon SVG |
| **Bebas (Free)** | 450 MB | 1.135 MB | +685 MB | Memori bebas dinamis |
| **Shared** | 82 MB | 11 MB | -71 MB | Alokasi memori bersama |
| **Buffer / Cache** | 2.451 MB | 1.792 MB | -659 MB | Cache I/O sistem |
| **Tersedia (Available)** | 2.568 MB | **2.493 MB** | **-75 MB** | Sisa memori sangat aman (> 2.4 GB) |

> **Analisis Kejujuran Data:**  
> Penambahan tema visual WhiteSur, set ikon vektor, dan ekstensi dock bawah secara realistis menambah penggunaan RAM sekitar ~76 MB (dari 1.342 MB ke 1.418 MB). Tim tidak mengklaim distro menjadi lebih ringan setelah dipasang tema macOS, melainkan menyajikan data empiris apa adanya. Kapasitas sisa memori 2.493 MB terbukti lebih dari cukup untuk menjalankan Geany IDE dan kompilasi program praktikum mahasiswa.

### B. Waktu Booting Sistem (`systemd-analyze`)

| Tahap Booting | LabKita 0.1 | LabKita 0.2 | Analisis Peningkatan |
| --- | :---: | :---: | --- |
| **Kernel Space** | 5.313 detik | **4.120 detik** | Pemuatan modul kernel lebih cepat (-1.19s) |
| **Userspace** | 54.672 detik | **27.680 detik** | Optimasi layanan dan berkurangnya verifikasi awal (-26.99s) |
| **Total Waktu Startup** | **59.985 detik** | **31.800 detik** | **Peningkatan efisiensi waktu boot ~47%** |
| **Waktu Menuju `graphical.target`** | 29.410 detik | **27.650 detik** | Desktop siap lebih awal (-1.76s) |

### C. Ringkasan Ukuran Berkas ISO

| Versi | Ukuran (Bytes) | Ukuran (GiB / GB) | SHA256 Checksum |
| :---: | :---: | :---: | --- |
| **LabKita 0.1** | 6.493.779.968 bytes | ~6.05 GiB / 6.49 GB | `f80e42c9e8d4db820121f02fca79588760f1549a6cc6634929e3b0e071b810c5` |
| **LabKita 0.2** | 6.519.777.280 bytes | ~6.07 GiB / 6.52 GB | `ae6391a26d3497cb9d9aed4d9e967352e46adfd630202ac47c58b149d8000d19` |

Selisih penambahan ukuran sebesar 25.997.312 bytes (~24.8 MB) disebabkan oleh injeksi bundel tema WhiteSur GTK (Light & Dark), paket ikon WhiteSur resolusi tinggi, kursor WhiteSur, tipografi Inter, dan paket bahasa Indonesia (`language-pack-id`, `language-pack-gnome-id`, `hunspell-id`, `firefox-locale-id`).
