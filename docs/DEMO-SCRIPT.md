# Naskah & Panduan Video Demo LabKita Linux 0.2
**Durasi Target:** 3 – 5 Menit  
**Platform Unggah:** YouTube (Unlisted) atau Google Drive  
**Mata Kuliah:** Sistem Operasi (Ganjil 2026/2027)  
**Dosen Pengampu:** Muhammad Sidik Asyaky, S.T., M.T.  

---

## 1. Ikhtisar Alur Video (Storyline)

| Segmen | Waktu (Durasi) | Fokus Visual | Poin Penjelasan / Voiceover |
| :---: | :---: | :--- | :--- |
| **1. Pembuka & Booting** | 00:00 – 00:45 (45s) | Slide Judul, Identitas Tim, Menu Boot GRUB Bahasa Indonesia | Pengenalan proyek LabKita Linux 0.2, latar belakang praktikum offline, dan bootloader GRUB berbahasa Indonesia. |
| **2. Antarmuka macOS & Bahasa Indonesia** | 00:45 – 01:30 (45s) | Desktop LabKita, Tema WhiteSur, Dock Bawah, Top Bar Bersih | Demonstrasi antarmuka modern bernuansa macOS (bebas aset proprietary Apple), tombol jendela di kiri, dock bawah terpusat, dan menu berbahasa Indonesia. |
| **3. Uji Mandiri (`labkita-check`)** | 01:30 – 02:15 (45s) | Terminal eksekusi `labkita-check` | Pembuktian kelulusan 21 pemeriksaan otomatis kesiapan sistem (GCC, Python, Geany, locale id_ID, timezone Jakarta, tema GTK, ikon, tmpfs). |
| **4. Uji Offline Total & Eksekusi Program** | 02:15 – 03:00 (45s) | `nmcli networking off`, kompilasi C & Python | Mematikan adapter jaringan VM secara total, membuktikan kompilasi program C (`hello.c`), Python multiproses (`processes.py`), dan panduan lokal berjalan 100% luring. |
| **5. Keamanan & Akun Praktikan** | 03:00 – 03:50 (50s) | `sudo labkita-postinstall praktikan`, `su - praktikan`, `sudo -l` | Pembuatan akun praktikan, demonstrasi pembatasan permission `0700`, dan pembuktian penolakan hak akses sudo. |
| **6. Analisis Kinerja Empiris & Penutup** | 03:50 – 04:30 (40s) | `free -m`, `systemd-analyze time`, Slide Anggota Tim | Menunjukkan penggunaan RAM riil (~1.41 GB, +76 MB karena tema visual WhiteSur), waktu boot startup (31.8 detik), kesimpulan, dan penutup. |

---

## 2. Naskah Terperinci Langkah Demi Langkah (Voiceover Script)

### Menit 00:00 – 00:45 | Segmen 1: Pembukaan & Booting
- **Visual:**
  - Tampilkan judul video: *"LabKita Linux 0.2 - Distro Praktikum Pemrograman Offline Berbahasa Indonesia"*.
  - Tampilkan VMware Workstation menyala, memilih *"Coba atau Pasang LabKita Linux (Bahasa Indonesia)"* di GRUB.
- **Voiceover:**
  > *"Halo semuanya! Selamat datang di video demonstrasi Final Project Sistem Operasi kelompok kami. Di sini kami mempersembahkan **LabKita Linux versi 0.2**, distribusi Linux turunan Ubuntu 24.04 LTS yang dirancang khusus untuk praktikum pemrograman dasar di laboratorium komputer kampus tanpa ketergantungan internet.*  
  > *Pada versi 0.2 ini, kami telah menuntaskan lokalisasi penuh ke dalam Bahasa Indonesia sejak tahap menu bootloader GRUB dan wizard instalasi, mengeliminasi glitch bahasa asing yang sebelumnya muncul."*

---

### Menit 00:45 – 01:30 | Segmen 2: Tampilan Desktop Bergaya macOS & Bahasa Indonesia
- **Visual:**
  - Sesi desktop memuat antarmuka bertema modern: dock terpusat di bawah dengan efek autohide, wallpaper gradien orisinal LabKita, tombol jendela di sebelah kiri, dan tipografi Inter.
  - Klik menu status di pojok kanan atas: tampil menu Bahasa Indonesia (*Mode Daya, Seimbang, Cahaya Malam, Gaya Gelap*).
- **Voiceover:**
  > *"Masuk ke antarmuka desktop, LabKita Linux 0.2 mengadopsi estetika modern bergaya macOS menggunakan tema open source WhiteSur GTK dan Icon theme, tanpa menggunakan aset hak cipta milik Apple sama sekali.*  
  > *Tombol jendela ditempatkan rapi di sisi kiri, dock aplikasi terpusat di bagian bawah layar, dan seluruh menu sistem menggunakan Bahasa Indonesia baku.*  
  > *Aplikasi praktikum esensial seperti Geany IDE dan materi praktikum telah kami sematkan langsung di dock utama."*

---

### Menit 01:30 – 02:15 | Segmen 3: Pengujian Otomatis (`labkita-check`)
- **Visual:**
  - Buka terminal (`Ctrl + Alt + T`).
  - Ketik dan jalankan perintah:
    ```bash
    labkita-check
    ```
  - Tampilkan output hijau: 21 pemeriksaan berturut-turut *"LULUS"* dan *"SEMUA PEMERIKSAAN LULUS"*.
- **Voiceover:**
  > *"Sebelum praktikum dimulai, asisten laboratorium cukup menjalankan perintah `labkita-check`.*  
  > *Skrip diagnostik ini memverifikasi 21 komponen penting secara otomatis: mulai dari compiler GCC, G++, Python 3, Geany IDE, Git, lokalisasi Bahasa Indonesia id_ID, zona waktu Asia/Jakarta, hingga integritas tema WhiteSur dan memori temporer tmpfs. Seluruh pengujian tercatat 100% lulus."*

---

### Menit 02:15 – 03:00 | Segmen 4: Uji Offline Total & Eksekusi Program
- **Visual:**
  - Di terminal, matikan jaringan:
    ```bash
    nmcli networking off
    nmcli networking connectivity check
    ```
    *(Output menampilkan: `none`)*
  - Jalankan program contoh di folder latihan:
    ```bash
    cd ~/Praktikum
    python3 hello.py
    python3 processes.py
    gcc -O2 hello.c -o hello && ./hello
    ```
  - Buka materi panduan via peluncur: `labkita-guide`.
- **Voiceover:**
  > *"Sekarang kita buktikan kapabilitas utama distro ini dalam kondisi jaringan terputus total.*  
  > *Dengan jaringan dinonaktifkan, mahasiswa tetap dapat mengompilasi program C, menjalankan skrip Python multiproses untuk mempelajari fork dan konkurensi, serta membuka dokumentasi dan panduan praktikum lokal secara instan tanpa internet."*

---

### Menit 03:00 – 03:50 | Segmen 5: Keamanan Sistem & Akun Mahasiswa
- **Visual:**
  - Jalankan skrip pembuatan akun mahasiswa:
    ```bash
    sudo labkita-postinstall praktikan
    ```
  - Tampilkan permission:
    ```bash
    stat /home/praktikan
    id praktikan
    ```
  - Masuk sebagai user `praktikan` dan uji akses sudo:
    ```bash
    su - praktikan
    sudo -l
    ```
    *(Tampilkan pesan penolakan sudo)*.
- **Voiceover:**
  > *"Untuk aspek tata kelola laboratorium, skrip `labkita-postinstall` secara otomatis menyiapkan akun mahasiswa tanpa izin sudo.*  
  > *Folder kerja mahasiswa diproteksi dengan izin ketat 0700 sehingga tidak bisa dibaca oleh mahasiswa lain.*  
  > *Ketika user praktikan mencoba perintah `sudo -l`, sistem secara tegas menolak akses, menjaga konfigurasi laboratorium tetap aman dari instalasi ilegal atau perusakan sistem."*

---

### Menit 03:50 – 04:30 | Segmen 6: Analisis Kinerja Empiris & Penutup
- **Visual:**
  - Jalankan perintah tolok ukur:
    ```bash
    free -m
    systemd-analyze
    ```
  - Tampilkan slide penutup yang berisi identitas anggota tim (Dafa Zahran, Rafly Fauzi Pratama, Muhammad Ilham Rizky, Vadien Athallah Lukman) dan tautan repositori GitHub (https://github.com/luvices/labkita).
- **Voiceover:**
  > *"Dari segi performa, penggunaan memori RAM LabKita 0.2 tercatat sebesar 1.41 GB. Kami laporkan secara transparan adanya sedikit penambahan memori sekitar 76 MB dibandingkan versi polos karena pemuatan tema visual WhiteSur yang lebih kaya.*  
  > *Meski demikian, sisa RAM tersedia masih sangat besar, yaitu 2.49 GB, dan waktu booting sistem meningkat drastis menjadi hanya 31.8 detik.*  
  > *Demikian demonstrasi LabKita Linux 0.2 dari kelompok kami. Terima kasih atas perhatiannya!"*

---

## 3. Checklist Perekaman Video
- [ ] Resolusi rekaman minimal 1080p (1920x1080) atau 720p (1280x720) dengan framerate 30/60 fps.
- [ ] Font terminal disetel ukuran 14–16 pt agar terbaca jelas pada layar monitor dan ponsel.
- [ ] Suara rekaman jernih tanpa derau latar belakang.
- [ ] Format video: MP4 (H.264 / AAC).
- [ ] Tautan diunggah ke YouTube sebagai *Unlisted* atau simpan di Google Drive dengan akses publik.
