# Naskah & Panduan Rekam Video Demonstrasi LabKita Linux 0.6

- **Durasi Target:** ~5,5 sampai 6 menit
- **Format Rekam:** Rekaman layar VMware Workstation (`1280x800` atau `1920x1080`) + mikrofon jernih
- **Pembagian Narator (4 Anggota):**
  1. **Dafa Zahran** (Ketua & Build/Integrasi): Segmen 1 & 2
  2. **Rafly Fauzi Pratama** (Toolchain & Diagnostik): Segmen 5
  3. **Muhammad Ilham Rizky** (Sistem, Keamanan & QA): Segmen 6 & 7
  4. **Vadien Athallah Lukman** (UI/UX, Brand & Dokumentasi): Segmen 3 & 4

> **Checklist Persiapan Sebelum Klik Record:**
> - Pastikan VM baru memakai opsi *"I will install the operating system later"* (tanpa Easy Install VMware) dan ISO `labkita-linux-0.6-amd64.iso` sudah terpasang di CD/DVD.
> - Siapkan satu VM bersih yang masih di tahap booting ISO (untuk Segmen 2), atau gunakan satu VM sudah terinstal (dengan `Accelerate 3D graphics` aktif & CD/DVD `Connect at power on` mati) lalu sambungkan klip proses Autoinstall di editor video.

---

## Segmen 1: Pembukaan, Latar Belakang, & Setup VMware (00:00 - 00:45)
- **Narator:** Dafa Zahran
- **Visual:** Tampilkan judul/cover `LabKita Linux 0.6` atau jendela VMware Workstation saat memilih **"I will install the operating system later"** lalu memasang `labkita-linux-0.6-amd64.iso` di `CD/DVD (SATA)`.
- **Narasi:**
  > "Assalamualaikum warahmatullahi wabarakatuh. Kami dari Kelompok LabKita Linux Program Studi Informatika Universitas Siliwangi. Pada video ini kami mendemonstrasikan rilis LabKita Linux 0.6, yaitu sistem operasi praktikum berbasis Ubuntu 24.04.5 LTS yang dirancang siap pakai secara offline tanpa bergantung koneksi internet kampus.
  > Pada rilis 0.6 ini kami memperbaiki alur instalasi agar asisten lab tidak perlu melewati wizard panjang maupun bug tampilan OpenGL VMware. Saat membuat VM baru di VMware, kita cukup memilih 'I will install the operating system later' dan memasang ISO secara manual agar fitur Easy Install VMware tidak menimpa skrip autoinstall bawaan LabKita."

---

## Segmen 2: GRUB Autoinstall Nol-Langkah & Splash Plymouth (00:45 - 01:30)
- **Narator:** Dafa Zahran
- **Visual:** Power on VM -> tunjukkan menu GRUB default `Pasang Otomatis LabKita Linux 0.6 (Admin + Praktikan)` -> proses installer berjalan otomatis (`Menyalin berkas...`) -> percepat (timelapse) hingga splash Plymouth berlogo LabKita muncul.
- **Narasi:**
  > "Saat VM dinyalakan, menu GRUB otomatis memilih mode Pasang Otomatis LabKita Linux 0.6 dalam beberapa detik. Berkat konfigurasi autoinstall NoCloud, installer langsung mempartisi disk, menyetel bahasa Indonesia serta zona waktu Asia/Jakarta, menyingkirkan paket bloat yang tidak relevan, dan membentuk dua akun secara otomatis. Proses ini berjalan sekitar empat menit lalu sistem melakukan reboot mandiri dengan splash screen bermerek resmi LabKita Linux."

---

## Segmen 3: Layar Login GDM Resmi & Dua Akun Bawaan (01:30 - 02:05)
- **Narator:** Vadien Athallah Lukman
- **Visual:** Tahan tampilan di layar login GDM. Arahkan kursor perlahan ke dua nama akun (**LabKita Admin** dan **praktikan**) serta logo **LabKita Linux / Praktikum Mandiri Offline** di bagian bawah layar. Lalu klik **LabKita Admin** dan masukkan password `labkita`.
- **Narasi:**
  > "Setelah reboot, sistem langsung tiba di layar login GDM. Terlihat di bagian bawah sudah terpasang logo resmi LabKita Linux melalui konfigurasi dconf greeter, dan sudah tersedia dua akun bawaan: akun LabKita Admin untuk asisten laboratorium, serta akun praktikan yang terisolasi untuk mahasiswa. Sekarang kita coba masuk terlebih dahulu ke akun LabKita Admin."

---

## Segmen 4: Desktop Bersih & Kelengkapan Ikon WhiteSur (02:05 - 02:50)
- **Narator:** Vadien Athallah Lukman
- **Visual:** Desktop terbuka langsung tanpa popup GNOME Initial Setup. Arahkan kursor ke Dock bawah -> klik **Tampilkan Aplikasi (App Grid)** untuk menunjukkan seluruh ikon terender utuh -> buka **Pengaturan (Settings)** sebentar untuk menunjukkan ikon sidebar lengkap -> tutup Settings.
- **Narasi:**
  > "Begitu login, desktop langsung bersih dengan tema WhiteSur, tombol jendela di sisi kiri, dock bawah, serta wallpaper orisinal LabKita tanpa gangguan popup sambutan awal atau notifikasi upgrade. Pada rilis 0.6 ini kami juga memperbaiki integritas symlink ikon WhiteSur serta cache ikonnya, sehingga saat App Grid dan menu Pengaturan dibuka, seluruh ikon tampil utuh tanpa ada ikon yang kosong."

---

## Segmen 5: Diagnostik `labkita-check` & Panduan Kerja 7 Modul di Firefox Snap (02:50 - 04:05)
- **Narator:** Rafly Fauzi Pratama
- **Visual:** Tekan `Ctrl + Alt + T` (Terminal) -> maksimalkan jendela -> ketik perintah berikut, tunggu selesai, lalu buka panduan:
  ```bash
  labkita-check
  labkita-guide
  ```
  Di Firefox Snap: tunjukkan URL `file:///home/labkita/Dokumen/Panduan-LabKita/index.html`, gulir modul 1-7, klik satu tombol `Salin`, dan centang checkbox `Selesai` di Modul 01 (progres berubah ke `1 / 7 modul`). Tutup Firefox.
- **Narasi:**
  > "Sekarang kita buka Terminal dan jalankan perintah `labkita-check` untuk memvalidasi kesiapan sistem secara otomatis. Seluruh komponen penting seperti GCC, G++, Make, GDB, Python 3, Geany, dokumentasi Python offline, lokasi panduan non-dotfolder, logo login GDM, hingga pembacaan panduan di dalam sandbox Firefox Snap berstatus LULUS semua.
  > Berikutnya kita jalankan `labkita-guide`. Berkas panduan diletakkan di folder Dokumen pengguna agar lolos kebijakan AppArmor Firefox Snap tanpa melemahkan keamanan sistem. Di dalamnya sudah tersedia tujuh modul praktikum terstruktur lengkap dengan tombol Salin dan pelacak progres lokal yang tersimpan di peramban."

---

## Segmen 6: Uji Isolasi Akun `praktikan`, `tmpfs`, & Kompilasi Offline (04:05 - 05:25)
- **Narator:** Muhammad Ilham Rizky
- **Visual:** Logout dari `labkita` (menu kanan atas -> Power -> Log Out), lalu di GDM pilih akun **praktikan** dan login dengan password `praktikan`.
  Buka Terminal (`Ctrl + Alt + T`) dan jalankan perintah verifikasi satu per satu dengan jeda 1-2 detik agar output terbaca jelas:
  ```bash
  whoami && id
  sudo -n true
  ls -ld /home/praktikan /run/labkita
  systemctl is-active labkita-runtime.service
  ls -la ~/Praktikum
  gcc -Wall ~/Praktikum/hello.c -o ~/Praktikum/hello && ~/Praktikum/hello
  python3 ~/Praktikum/thread_demo.py
  ```
- **Narasi:**
  > "Selanjutnya kita keluar dan masuk ke akun praktikan. Akun ini tidak masuk ke grup sudo, hanya berada di grup labkita-praktikum dengan izin direktori home 0700 sehingga berkas antar-mahasiswa terisolasi dan aman dari perubahan sistem oleh praktikan. Saat diuji perintah `sudo`, sistem langsung menolak.
  > Kami juga menyiapkan ruang kerja sementara berbasis RAM di `/run/labkita` dengan sticky bit 1777 lewat layanan `labkita-runtime.service`. Karena `/run` di Ubuntu modern bersifat noexec, kompilasi biner program C tetap dijalankan langsung dari folder pribadi `~/Praktikum`. Seperti terlihat, kompilasi program C dengan GCC maupun eksekusi skrip Python multithreading berjalan lancar sepenuhnya tanpa koneksi internet."

---

## Segmen 7: Ringkasan & Penutup (05:25 - 05:50)
- **Narator:** Muhammad Ilham Rizky
- **Visual:** Biarkan terminal `praktikan` bersama desktop bersih di layar (atau tampilkan slide penutup dengan tautan GitHub `https://github.com/luvices/labkita`).
- **Narasi:**
  > "Dengan demikian seluruh fitur LabKita Linux 0.6 mulai dari autoinstall nol-langkah, dual akun terisolasi, pemulihan ikon dan branding resmi, hingga buku kerja tujuh modul offline telah terverifikasi langsung di VMware Workstation. Terima kasih atas perhatiannya, wassalamualaikum warahmatullahi wabarakatuh."
