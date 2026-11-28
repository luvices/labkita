# Checklist QA & Evaluasi Keamanan LabKita Linux 0.6

Dokumen ini berisi prosedur verifikasi terstruktur dan perintah uji yang dapat langsung dijalankan oleh penguji atau asisten lab pada mesin virtual VMware Workstation. Semua langkah mengacu pada berkas dan konfigurasi aktual di repositori `luvices/labkita` versi 0.6.

**Penyusun:** Muhammad Ilham Rizky (QA & Evaluasi Keamanan)

---

## 1. Pemeriksaan Integritas ISO 0.6

Pastikan berkas ISO yang diunduh dari Google Drive cocok dengan hash resmi di `dist/`.

### 1.1 Verifikasi SHA256

**Nilai acuan** (dari `dist/labkita-linux-0.6-amd64.iso.sha256`):

```
78a58f0f757b63b97b46e21a520a2c2ea7a205458119192c8f4ed10d2fe9bde1  labkita-linux-0.6-amd64.iso
```

**Perintah uji di Linux/macOS:**

```bash
sha256sum labkita-linux-0.6-amd64.iso
# Bandingkan keluaran dengan nilai acuan di atas.
# Atau verifikasi otomatis:
sha256sum -c dist/labkita-linux-0.6-amd64.iso.sha256
```

**Perintah uji di Windows (PowerShell):**

```powershell
Get-FileHash -Algorithm SHA256 .\labkita-linux-0.6-amd64.iso
# Harus cocok: 78A58F0F757B63B97B46E21A520A2C2EA7A205458119192C8F4ED10D2FE9BDE1
```

| # | Butir Pemeriksaan | Perintah/Aksi | Hasil Diharapkan | Lulus? |
|---|---|---|---|---|
| 1.1 | Hash SHA256 cocok | `sha256sum labkita-linux-0.6-amd64.iso` | `78a58f0f...e9bde1` | [ ] |

### 1.2 Verifikasi MD5

**Nilai acuan** (dari `dist/labkita-linux-0.6-amd64.iso.md5`):

```
7db00f4c1bfbdf06df62c77bfd0e14c7  labkita-linux-0.6-amd64.iso
```

**Perintah uji di Linux/macOS:**

```bash
md5sum labkita-linux-0.6-amd64.iso
# Bandingkan keluaran dengan nilai acuan di atas.
```

| # | Butir Pemeriksaan | Perintah/Aksi | Hasil Diharapkan | Lulus? |
|---|---|---|---|---|
| 1.2 | Hash MD5 cocok | `md5sum labkita-linux-0.6-amd64.iso` | `7db00f4c...0e14c7` | [ ] |

### 1.3 Ukuran Berkas

| # | Butir Pemeriksaan | Perintah/Aksi | Hasil Diharapkan | Lulus? |
|---|---|---|---|---|
| 1.3 | Ukuran ISO sesuai | `ls -l labkita-linux-0.6-amd64.iso` | `6083305472 bytes` (~5,67 GiB) | [ ] |

---

## 2. Daftar Cek Isolasi Akun `praktikan`

Verifikasi bahwa akun `praktikan` yang dibuat oleh `labkita-postinstall` telah terisolasi dengan benar sesuai desain keamanan LabKita Linux.

> Jalankan semua perintah berikut setelah login sebagai akun `praktikan` (sandi default: `praktikan`) di dalam VM yang sudah terinstal.

### 2.1 Identitas dan Keanggotaan Grup

```bash
id
```

| # | Butir Pemeriksaan | Perintah/Aksi | Hasil Diharapkan | Lulus? |
|---|---|---|---|---|
| 2.1a | UID `praktikan` terdaftar | `id` | `uid=1001(praktikan)` | [ ] |
| 2.1b | Anggota grup `labkita-praktikum` | `id` | Keluaran mengandung `labkita-praktikum` | [ ] |
| 2.1c | Bukan anggota grup `sudo` | `id` | Keluaran TIDAK mengandung `sudo` | [ ] |

### 2.2 Hak Akses Sudo Ditolak

```bash
sudo -n true 2>&1
```

| # | Butir Pemeriksaan | Perintah/Aksi | Hasil Diharapkan | Lulus? |
|---|---|---|---|---|
| 2.2 | Sudo ditolak tanpa kata sandi | `sudo -n true 2>&1` | Pesan kesalahan: `a password is required` atau sejenisnya | [ ] |

### 2.3 Izin Direktori Home Privat

```bash
stat -c '%a %U %G' /home/praktikan
```

| # | Butir Pemeriksaan | Perintah/Aksi | Hasil Diharapkan | Lulus? |
|---|---|---|---|---|
| 2.3 | Mode direktori `/home/praktikan` = `0700` | `stat -c '%a' /home/praktikan` | `700` | [ ] |

### 2.4 Direktori Kerja Tersedia

```bash
ls ~/Praktikum/
ls ~/Dokumen/Panduan-LabKita/
```

| # | Butir Pemeriksaan | Perintah/Aksi | Hasil Diharapkan | Lulus? |
|---|---|---|---|---|
| 2.4a | Folder `~/Praktikum/` berisi contoh kode | `ls ~/Praktikum/` | Memuat `hello.c`, `hello.py`, `processes.py`, `thread_demo.py` | [ ] |
| 2.4b | Folder `~/Dokumen/Panduan-LabKita/` tersedia | `ls ~/Dokumen/Panduan-LabKita/` | Memuat `index.html` | [ ] |

---

## 3. Daftar Cek Layanan Memori Sementara `labkita-runtime.service`

Verifikasi konfigurasi dan status layanan systemd yang menyediakan ruang kerja sementara berbasis `tmpfs`.

> Jalankan semua perintah berikut dari akun `labkita` (admin) atau sebagai `root` di dalam VM.

### 3.1 Status Layanan Aktif

```bash
systemctl is-active labkita-runtime.service
systemctl status labkita-runtime.service
```

| # | Butir Pemeriksaan | Perintah/Aksi | Hasil Diharapkan | Lulus? |
|---|---|---|---|---|
| 3.1 | Layanan aktif | `systemctl is-active labkita-runtime.service` | `active` | [ ] |

### 3.2 Direktori `/run/labkita` dengan Sticky Bit

```bash
stat -c '%a %U' /run/labkita
```

| # | Butir Pemeriksaan | Perintah/Aksi | Hasil Diharapkan | Lulus? |
|---|---|---|---|---|
| 3.2a | Direktori `/run/labkita` ada | `test -d /run/labkita && echo OK` | `OK` | [ ] |
| 3.2b | Mode `1777` (sticky bit) | `stat -c '%a' /run/labkita` | `1777` | [ ] |

### 3.3 Sifat `tmpfs` pada `/run`

```bash
findmnt -n -o FSTYPE,OPTIONS /run
```

| # | Butir Pemeriksaan | Perintah/Aksi | Hasil Diharapkan | Lulus? |
|---|---|---|---|---|
| 3.3a | Tipe sistem berkas `/run` = `tmpfs` | `findmnt -n -o FSTYPE /run` | `tmpfs` | [ ] |
| 3.3b | Opsi `noexec` pada `/run` (jika berlaku) | `findmnt -n -o OPTIONS /run` | Periksa keberadaan `noexec` pada opsi mount | [ ] |

> **Catatan:** Opsi `noexec` pada `/run` bergantung pada konfigurasi distribusi dasar Ubuntu 24.04. Layanan unit `labkita-runtime.service` sendiri sudah menerapkan `ProtectSystem=strict`, `ProtectHome=yes`, `PrivateTmp=yes`, dan `NoNewPrivileges=yes` sebagai lapisan keamanan tambahan.

### 3.4 Pemisahan Kompilasi di `~/Praktikum`

Verifikasi bahwa akun `praktikan` dapat mengompilasi dan menjalankan program C di direktori kerja `~/Praktikum` (bukan di `/run/labkita`).

```bash
# Login sebagai praktikan
cd ~/Praktikum
gcc -Wall -Wextra hello.c -o hello && ./hello
python3 hello.py
```

| # | Butir Pemeriksaan | Perintah/Aksi | Hasil Diharapkan | Lulus? |
|---|---|---|---|---|
| 3.4a | Kompilasi C berhasil di `~/Praktikum` | `gcc -Wall -Wextra hello.c -o hello && ./hello` | Keluaran: `Halo dari LabKita Linux!` | [ ] |
| 3.4b | Eksekusi Python berhasil di `~/Praktikum` | `python3 hello.py` | Keluaran: `Halo dari LabKita Linux!` | [ ] |

---

## 4. Daftar Cek Pasca-Instalasi VMware Workstation

Verifikasi konfigurasi VMware dan fungsionalitas sistem setelah instalasi otomatis selesai dan VM sudah reboot ke disk.

### 4.1 Konfigurasi VMware Workstation

| # | Butir Pemeriksaan | Aksi Manual di VMware | Hasil Diharapkan | Lulus? |
|---|---|---|---|---|
| 4.1a | CD/DVD tidak terhubung saat boot | Buka VM Settings > CD/DVD (SATA) > **hapus centang** "Connect at power on" | CD/DVD tidak lagi dimuat otomatis saat VM dinyalakan | [ ] |
| 4.1b | Akselerasi 3D grafis diaktifkan | Buka VM Settings > Display > **centang** "Accelerate 3D graphics" | 3D graphics aktif untuk mendukung desktop GNOME | [ ] |
| 4.1c | Fallback Ubuntu on Xorg (jika perlu) | Pada layar login GDM, klik ikon gerigi kanan bawah > pilih "Ubuntu on Xorg" | Sesi Xorg berhasil dimuat tanpa layar hitam | [ ] |

### 4.2 Diagnostik `labkita-check` (25/25 Lulus)

Jalankan skrip diagnostik mandiri yang memeriksa 25 poin kesiapan sistem:

```bash
labkita-check
# Atau jika perlu hak root untuk sebagian pemeriksaan:
sudo labkita-check
```

**Daftar 25 pemeriksaan yang dijalankan oleh `labkita-check`:**

1. Program `python3`
2. Program `gcc`
3. Program `g++`
4. Program `make`
5. Program `geany`
6. Program `git`
7. Program `man`
8. Berkas panduan lokal (`/usr/share/labkita/guide/index.html`)
9. Skrip peluncur panduan (`/usr/local/bin/labkita-guide`)
10. Lokasi panduan non-dotfolder (`~/Dokumen/Panduan-LabKita`)
11. Asosiasi penampil HTML (`xdg-mime`)
12. Pembacaan panduan oleh sandbox Firefox Snap (AppArmor OK)
13. Dokumentasi Python offline (`/usr/share/doc/python3/html/index.html`)
14. Dukungan Bahasa Indonesia (`id_ID.UTF-8`)
15. Zona waktu `Asia/Jakarta`
16. Tema GTK WhiteSur
17. Set Ikon WhiteSur
18. Integritas symlink ikon WhiteSur
19. Tema Kursor WhiteSur
20. Wallpaper Orisinal LabKita
21. Aset Splash Boot LabKita (Plymouth)
22. Logo Login GDM LabKita
23. Eksekusi contoh Python (`hello.py`)
24. Eksekusi proses anak / fork / multiprocess (`processes.py`)
25. Kompilasi dan eksekusi C (`hello.c`)

Setelah pemeriksaan 1-25, `labkita-check` juga memverifikasi:
- Ruang kerja sementara tmpfs `/run/labkita` dengan sticky bit `1777`
- Status aktif layanan `labkita-runtime.service`

| # | Butir Pemeriksaan | Perintah/Aksi | Hasil Diharapkan | Lulus? |
|---|---|---|---|---|
| 4.2a | Semua 25 pemeriksaan lulus | `labkita-check` | `SEMUA PEMERIKSAAN LULUS` | [ ] |
| 4.2b | Tidak ada pemeriksaan `[GAGAL]` | Periksa keluaran di atas | Nol baris `[GAGAL]` | [ ] |

### 4.3 Panduan LabKita (`labkita-guide`) dan AppArmor

```bash
labkita-guide
# Verifikasi panduan terbuka di Firefox Snap tanpa blokir AppArmor
```

| # | Butir Pemeriksaan | Perintah/Aksi | Hasil Diharapkan | Lulus? |
|---|---|---|---|---|
| 4.3a | Perintah `labkita-guide` berhasil | `labkita-guide` | Panduan tersalin ke `~/Dokumen/Panduan-LabKita/` dan terbuka di peramban | [ ] |
| 4.3b | Firefox Snap membaca tanpa blokir AppArmor | Periksa keluaran `labkita-check` butir 12 | `AppArmor OK` | [ ] |

---

## 5. Ringkasan Eksekusi Checklist

| Kategori | Jumlah Butir | Lulus | Gagal |
|---|---|---|---|
| 1. Integritas ISO | 3 | | |
| 2. Isolasi akun `praktikan` | 7 | | |
| 3. Layanan `labkita-runtime.service` | 7 | | |
| 4. Pasca-instalasi VMware | 7 | | |
| **Total** | **24** | | |

**Tanggal pengujian:** ____________________

**Penguji:** ____________________

**Catatan tambahan:**

---

> Dokumen ini adalah bagian dari dokumentasi QA repositori [luvices/labkita](https://github.com/luvices/labkita). Lihat juga [Rencana dan Hasil Pengujian 0.6](TEST-PLAN.md) untuk hasil verifikasi resmi.
