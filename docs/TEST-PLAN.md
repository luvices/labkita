# Rencana dan Hasil Pengujian LabKita Linux 0.2

Dokumen ini mencatat hasil audit dan verifikasi nyata pada **LabKita Linux 0.2** yang diinstal bersih ke disk virtual kosong (VMware Workstation `labkita-test.vmx`, 2 vCPU, RAM 4 GB / `3911 MiB` usable, disk virtual 40 GB SCSI). Semua tangkapan layar pada `docs/evidence/` adalah hasil capture langsung layar VM, termasuk pengujian yang gagal atau hanya lolos dengan catatan.

## 1. Daftar Pengujian Fungsional

| Pengujian | Target | Hasil Nyata di VM | Status | Bukti Screenshot |
| :--- | :--- | :--- | :--- | :--- |
| **Boot Menu GRUB Bahasa Indonesia** | Menu boot tampil dalam Bahasa Indonesia | Tampil *"Coba atau Pasang LabKita Linux (Bahasa Indonesia)"* di GRUB 2.12 | **LULUS** | `docs/evidence/01-grub-boot-menu-id.png` |
| **Autologin Live Session (`labkita`)** | Langsung masuk desktop sesi live tanpa wizard setup | Sesi live gagal autologin ke `labkita` dan selalu membuka `gnome-initial-setup` ("Selamat Datang") lebih dulu (terjadi di 0.1 & 0.2) | **GAGAL** | *(diamati saat live boot)* |
| **Installer GUI (`ubuntu-desktop-bootstrap`)** | Instalasi ke disk kosong lewat wizard grafis berjalan tuntas | Gagal di awal dengan dialog *"Ada yang salah"* (`casper-md5check` mismatch + kegagalan info snap pada log installer) | **GAGAL** | `docs/evidence/02-gui-installer-error.png` |
| **Instalasi ke Disk via `subiquity.cmd.tui`** | Instalasi penuh ke `/dev/sda` pada disk kosong 40 GB | Berhasil menyelesaikan partisi LVM + instalasi hingga *"Installation complete!"* dan reboot ke sistem terinstal | **LULUS (Fallback TUI)** | `docs/evidence/03-subiquity-tui-install-complete.png` |
| **Konsistensi Branding Rilis 0.2** | Seluruh dialog dan metadata menampilkan LabKita 0.2 | Dialog sambutan & sumber instalasi masih menyisakan label lama *"LabKita Linux 0.1 (Cubic 2026-11-03 23:29)"* (`/etc/labkita-release` sudah `0.2`) | **GAGAL (Minor/Sisa Metadata)** | `docs/evidence/03-subiquity-tui-install-complete.png` |
| **Desktop WhiteSur, Dock & Bahasa Indonesia** | Tema GTK/Ikon WhiteSur, tombol kiri, dock bawah tengah, wallpaper gradien, UI Indonesia | Tema WhiteSur, tombol jendela di kiri, dock terpusat, wallpaper LabKita, top bar `Sen 16 Nov`, dan `Berkas` tampil dalam Bahasa Indonesia | **LULUS** | `docs/evidence/04-installed-desktop-whitesur-id.png` |
| **`labkita-check` di Sistem Terinstal** | 21 pemeriksaan skrip berjalan pada OS terinstal | 21 dari 21 item `[LULUS]` (0 gagal oleh skrip; catatan: skrip hanya mengecek keberadaan file panduan, bukan eksekusi browser) | **LULUS** | `docs/evidence/05-installed-labkita-check.png` |
| **`sudo labkita-postinstall praktikan` (ISO 0.2)** | Membuat user `praktikan` non-sudo, `0700`, dan mencetak ringkasan tanpa error | User `praktikan` dan sandinya berhasil dibuat (`[SUKSES]`), tetapi baris 45 di skrip ISO 0.2 error `printf: - : pilihan tidak valid` (sudah diperbaiki di source repo `payload/`, belum di-rebuild ke ISO) | **GAGAL PARSIAL** | `docs/evidence/06-installed-labkita-postinstall.png` |
| **Isolasi Hak Akses & Izin `/home/praktikan`** | `praktikan` tidak masuk grup `sudo`/`adm`, folder `0700` privat | `id praktikan` (`1001`, grup `praktikan,labkita`), `stat` menunjukkan `700`, `ls /home/praktikan` dari `labkitaadmin` ditolak (`Ijin ditolak`), `sudo`/`adm` hanya berisi `labkitaadmin` | **LULUS** | `docs/evidence/07-installed-praktikan-isolation.png` |
| **Kompilasi & Eksekusi C/Python Tanpa Internet** | Toolchain offline bekerja dengan `nmcli networking off` | `nmcli networking` status `disabled`; `gcc hello.c` + `./hello_test`, `hello.py`, dan `processes.py` (multiprocessing) sukses dieksekusi | **LULUS** | `docs/evidence/08-installed-offline-c-python.png` |
| **Peluncur Panduan `labkita-guide` via Firefox Snap** | Membuka panduan HTML offline di browser tanpa error sandbox | Meski `labkita-guide` menyalin HTML ke `~/.local/share/labkita/guide/`, Firefox Snap masih memblokir akses dotfolder (`Akses terhadap berkas ditolak`) | **GAGAL** | `docs/evidence/09-installed-guide-firefox-snap-error.png` |

## 2. Perbandingan Kinerja 0.1 vs 0.2 Setelah Instalasi (Kondisi VM Identik)

Kedua versi diinstal ke disk virtual terpisah pada **VM yang sama** (`labkita-test.vmx`: 2 vCPU, RAM 4096 MB / `3911 MiB` terbaca Linux, disk 40 GB SCSI) lalu diukur **3 kali reboot bersih masing-masing**. Setiap pengukuran dilakukan di terminal 20 detik setelah desktop selesai login.

### A. Konsumsi Memori RAM (`free -m`)

| Versi | Run 1 Used / Avail | Run 2 Used / Avail | Run 3 Used / Avail | Rata-rata Used | Rata-rata Available |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **LabKita 0.1 (Terinstal, GNOME Yaru, Kernel `7.0.0-31-generic`)** | 1025 / 2886 MiB | 1030 / 2880 MiB | 1040 / 2870 MiB | **1031.7 MiB** | **2878.7 MiB** |
| **LabKita 0.2 (Terinstal, WhiteSur + Dock + ID, Kernel `7.0.0-43-generic`)** | 1063 / 2848 MiB | 1053 / 2857 MiB | 1064 / 2847 MiB | **1060.0 MiB** | **2850.7 MiB** |
| **Selisih (0.2 vs 0.1)** | +38 MiB | +23 MiB | +24 MiB | **+28.3 MiB (+2.7%)** | **-28.0 MiB** |

### B. Waktu Booting (`systemd-analyze time`)

| Versi | Run 1 (Kernel + User = Total) | Run 2 (Kernel + User = Total) | Run 3 (Kernel + User = Total) | Rata-rata Total | `graphical.target` (Rata-rata) |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **LabKita 0.1 (Terinstal)** | `3.504s + 6.933s = 10.437s` | `3.442s + 6.047s = 9.490s` | `3.406s + 6.345s = 9.752s` | **9.893s** | **6.398s** |
| **LabKita 0.2 (Terinstal)** | `3.425s + 6.152s = 9.578s` | `4.306s + 9.355s = 13.662s` | `3.496s + 7.625s = 11.121s` | **11.454s** | **7.636s** |
| **Selisih (0.2 vs 0.1)** | -0.859s | +4.172s | +1.369s | **+1.561s (+15.8%)** | **+1.238s** |

Bukti tangkapan layar 3x benchmark `0.1`: `docs/evidence/10-v01-installed-bench-r1.png`, `11-v01-installed-bench-r2.png`, `12-v01-installed-bench-r3.png`.
Bukti tangkapan layar 3x benchmark `0.2`: `docs/evidence/13-v02-installed-bench-r1.png`, `14-v02-installed-bench-r2.png`, `15-v02-installed-bench-r3.png`.

### Catatan Analisis Jujur

1. **Tidak lebih cepat & RAM sedikit naik:** Setelah diuji ulang pada sistem terinstal dalam kondisi identik, LabKita 0.2 menggunakan RAM rata-rata **28.3 MiB lebih tinggi** (`1060.0 MiB` vs `1031.7 MiB`) dan rata-rata waktu boot **1.561 detik lebih lambat serta lebih fluktuatif** (`9.578s–13.662s` dengan rata-rata `11.454s`, dibanding `9.490s–10.437s` dengan rata-rata `9.893s` pada 0.1). Oleh karena itu, klaim "lebih ringan" atau "lebih cepat" tidak berlaku; penambahan tema/ekstensi Dash-to-Dock WhiteSur dan pembaruan layanan boot memberi overhead wajar namun tetap menyisakan ~2.85 GiB RAM untuk IDE/compiler praktikum.
2. **Komponen terlama saat boot (`systemd-analyze blame`):** Di kedua versi, layanan teratas berasal dari `plymouth-quit-wait.service` (`2.644s–4.340s`), `snapd.seeded.service` (`1.083s–1.721s`), dan `snapd.service` (`0.913s–1.660s`).
3. **Akar masalah kegagalan yang ditemukan selama audit:**
   - **GUI installer gagal:** Konflik autologin `casper.conf` + ketidakcocokan checksum squashfs setelah remastering Cubic membuat `ubuntu-desktop-bootstrap` berhenti di `"Ada yang salah"`; fallback `subiquity.cmd.tui` tetap berhasil menyelesaikan instalasi disk.
   - **Panduan offline via Firefox Snap masih terblokir:** Firefox Snap menolak URI di dalam dotfolder `~/.local/share/labkita/guide/` (`Akses terhadap berkas ditolak`) karena kebijakan sandbox `home` Snap memblokir direktori tersembunyi berawalan titik. Rilis selanjutnya perlu menyalin panduan ke folder non-tersembunyi (misal `~/Panduan-LabKita`) atau memakai server HTTP lokal / HTML viewer non-Snap.
   - **`labkita-postinstall` ISO 0.2 bug baris 45:** Flag `-` di awal argumen `printf` terbaca sebagai opsi tidak valid oleh `printf`; sudah diperbaiki menjadi `printf --` pada source repo, namun ISO 0.2 terlanjur memaketkan versi sebelum perbaikan.
