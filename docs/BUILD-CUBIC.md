# Build ISO dengan Cubic

## 1. Lingkungan build

Siapkan Ubuntu Desktop pada VM terpisah. ISO asli yang sudah tersedia boleh
dipakai untuk menginstal VM build, kemudian dipakai lagi sebagai input Cubic.
Ini tidak memerlukan instalasi ulang Windows.

Saran awal: RAM 6 GB, CPU 2-4, disk VM dinamis 80 GB dengan sekitar 60 GB
ruang kosong di drive host. Tempatkan folder proyek Cubic di filesystem Linux
di dalam VM, misalnya `~/cubic/labkita`, bukan shared folder Windows.

Pemeriksaan ulang menemukan drive D (DATA) kosong sekitar 119,97 GB.
Simpan VM baru di folder `build/vm/` proyek ini pada drive D.

WSL dipakai untuk pemeriksaan kode dan persiapan media instalasi otomatis.
Jalur GUI, mount, dan build Cubic di WSL belum diverifikasi pada laptop ini.

## 2. Pasang Cubic di terminal Ubuntu build

```bash
sudo apt update
sudo apt install -y software-properties-common
sudo apt-add-repository universe
sudo apt-add-repository ppa:cubic-wizard/release
sudo apt update
sudo apt install --no-install-recommends cubic
```

Perintah tersebut mengikuti dokumentasi resmi Cubic:
https://github.com/PJ-Singh-001/Cubic/wiki/Install-Cubic

## 3. Buat arsip kit di Windows

Jalankan Python dari folder proyek:

```powershell
python tools/pack.py
```

Output: `dist/labkita-kit.tar.gz`. Salin arsip kecil ini dan ISO asli ke VM.
Folder `payload/` adalah isi yang akan ditempatkan di filesystem distro.

## 4. Pilih ISO dan salin kit

1. Buka Cubic dan pilih folder proyek Linux yang baru.
2. Pilih ISO Ubuntu Desktop 24.04 yang sudah ada.
3. Beri nama hasil `LabKita Linux 0.1`, misalnya `labkita-linux-0.1-amd64.iso`.
4. Tunggu ekstraksi, lalu masuk ke **terminal virtual Cubic**.
5. Ketik `cd /tmp`. Drag arsip `labkita-kit.tar.gz` ke terminal Cubic dan
   konfirmasi penyalinan berkas.
6. Di terminal virtual Cubic jalankan:

```bash
cd /tmp
tar -xzf labkita-kit.tar.gz
cd labkita-linux
bash scripts/customize.sh --cubic
```

Skrip menolak berjalan di luar chroot atau pada basis selain Ubuntu 24.04.
Jangan menjalankannya di terminal biasa VM atau WSL. Jika deteksi chroot
gagal, hentikan dan periksa lingkungan; jangan menonaktifkan pemeriksaannya.

## 5. Generate ISO

Lanjutkan wizard Cubic setelah skrip selesai. Pertahankan kernel, komponen
installer, dan pengaturan boot bawaan pada build pertama. Jangan menghapus
`snapd` atau Snap installer. Paket kit dipasang melalui apt, bukan Snap.

Pada halaman pemilihan paket, pastikan paket kit tidak ditandai untuk dihapus
oleh installer. Generate ISO dan catat checksum SHA256 serta versi Cubic.

Dokumentasi Cubic mencatat bahwa overlay installer Ubuntu baru dapat menutupi
sebagian kustomisasi pada sesi live. Karena itu cek **sesi live dan sistem
hasil instalasi**. Jangan menyatakan ISO selesai hanya karena generate berhasil.

Referensi: https://github.com/PJ-Singh-001/Cubic/wiki/Terminal-Page

## 6. Boot dan instalasi percobaan

Gunakan VM pengujian baru dengan disk kosong. Boot ISO, uji panduan dan paket,
lalu instal ke disk VM tersebut. Setelah boot dari disk hasil instalasi:

```bash
labkita-check
sudo labkita-postinstall praktikan
```

Perintah kedua meminta password baru dan membuat akun praktikan tanpa grup
sudo. Akun administrator yang dibuat installer tetap digunakan pengelola.
Login sebagai praktikan, putus koneksi jaringan VM, lalu ulangi latihan.

Installer pada beberapa kombinasi Ubuntu/Cubic dapat memerlukan internet;
catat hasil pengujian instalasi online dan offline secara terpisah. Visi
utama kit adalah **pemakaian praktikum offline setelah sistem terpasang**.

## 7. Bukti hasil

Ikuti `TEST-PLAN.md`. Simpan tangkapan layar dan hasil nyata di laporan.
Tautkan repositori, video, dan checksum ISO pada README sebelum pengumpulan.
