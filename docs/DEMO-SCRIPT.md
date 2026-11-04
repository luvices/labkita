# Naskah & Panduan Video Demo LabKita Linux 0.1
**Durasi Target:** 3 – 5 Menit  
**Platform Unggah:** YouTube (Unlisted) atau Google Drive  
**Mata Kuliah:** Sistem Operasi (Ganjil 2026/2027)  
**Dosen Pengampu:** Muhammad Sidik Asyaky, S.T., M.T.  

---

## 1. Ikhtisar Alur Video (Storyline)

| Segmen | Waktu (Durasi) | Fokus Visual | Poin Penjelasan / Voiceover |
| :---: | :---: | :--- | :--- |
| **1. Pembuka** | 00:00 – 00:40 (40s) | Slide Judul, Identitas Tim, Booting ISO di VM | Pengenalan proyek LabKita Linux, latar belakang kendala internet saat praktikum, dan spesifikasi VM uji. |
| **2. Tampilan & Branding** | 00:40 – 01:20 (40s) | Desktop LabKita, Wallpaper kustom, Panel Dock | Penjelasan identitas visual, launcher Geany, panduan praktikum, dan arsitektur basis Ubuntu 24.04 LTS. |
| **3. Uji Mandiri (`labkita-check`)** | 01:20 – 02:00 (40s) | Terminal eksekusi `labkita-check` | Pembuktian kelulusan 14 pengujian otomatis (GCC, Python, Geany, systemd, sticky bit, man pages). |
| **4. Uji Offline Total** | 02:00 – 02:50 (50s) | `nmcli networking off`, kompilasi C & Python | Mematikan adapter jaringan VM secara total, membuktikan bahwa kompilasi program C (`hello.c`) dan Python multiproses (`processes.py`) berjalan 100% tanpa internet. |
| **5. Keamanan & Akun Praktikan** | 02:50 – 03:45 (55s) | `sudo labkita-postinstall praktikan`, `su - praktikan`, `sudo -l` | Pembuatan akun praktikan, demonstrasi pembatasan permission `0700`, dan pembuktian penolakan hak akses sudo. |
| **6. Manajemen Memori & Penutup** | 03:45 – 04:30 (45s) | `free -m`, `systemd-analyze time`, Slide Anggota Tim | Menunjukkan penggunaan RAM riil (~1.34 GB), waktu boot startup (59.9 detik), kesimpulan, dan penutup. |

---

## 2. Naskah Terperinci Langkah Demi Langkah (Voiceover Script)

### Menit 00:00 – 00:40 | Segmen 1: Pembukaan & Booting
- **Visual:**
  - Tampilkan judul video: *"LabKita Linux 0.1 - Distro Praktikum Pemrograman Offline"*.
  - Tampilkan VMware Workstation menyala, memilih *"Try or Install Ubuntu / LabKita"* di GRUB.
- **Voiceover:**
  > *"Halo semuanya! Selamat datang di video demonstrasi Final Project Sistem Operasi kelompok kami. Di sini kami mempersembahkan **LabKita Linux versi 0.1**, sebuah distribusi Linux turunan Ubuntu 24.04 LTS yang dirancang khusus untuk lingkungan praktikum pemrograman dasar di laboratorium komputer tanpa ketergantungan internet.*  
  > *Seringkali saat praktikum, jaringan internet kampus bermasalah atau justru disalahgunakan praktikan untuk browsing di luar materi. LabKita Linux hadir sebagai solusi mandiri yang siap pakai sejak detik pertama booting."*

---

### Menit 00:40 – 01:20 | Segmen 2: Tampilan Desktop & Identitas LabKita
- **Visual:**
  - Sesi desktop GNOME termuat dengan wallpaper kustom LabKita (`Ruang belajar. Siap offline.`).
  - Kursor mengarahkan ke dock kiri: ikon Geany, terminal, panduan materi, dan pemutar berkas.
- **Voiceover:**
  > *"Seperti yang dapat dilihat, sistem langsung memuat antarmuka grafis dengan wallpaper kustom LabKita Linux. Di panel sebelah kiri, kami telah menata pintasan esensial: Geany IDE sebagai editor kode ringan terintegrasi, Terminal, berkas latihan mahasiswa, dan panduan praktikum lokal.*  
  > *Seluruh lingkungan ini dikemas menggunakan Cubic ke dalam satu berkas ISO mandiri berukuran 6.05 GiB."*

---

### Menit 01:20 – 02:00 | Segmen 3: Pengujian Otomatis (`labkita-check`)
- **Visual:**
  - Buka terminal (`Ctrl + Alt + T`).
  - Ketik dan jalankan perintah:
    ```bash
    labkita-check
    ```
  - Tampilkan output hijau: 14 pemeriksaan berturut-turut *"LULUS"* dan *"0 pemeriksaan gagal"*.
- **Voiceover:**
  > *"Untuk memastikan kesiapan sebelum praktikum dimulai, asisten laboratorium cukup mengetikkan perintah `labkita-check`.*  
  > *Skrip diagnostik ini memverifikasi secara menyeluruh 14 komponen sistem: mulai dari ketersediaan compiler GCC, G++, Python 3, tool Make, Git, manual offline, hingga layanan runtime systemd. Di sini terlihat seluruh pengujian lulus 100% tanpa ada kesalahan."*

---

### Menit 02:00 – 02:50 | Segmen 4: Uji Offline Total & Eksekusi Program
- **Visual:**
  - Di terminal, matikan jaringan:
    ```bash
    nmcli networking off
    nmcli networking connectivity check
    ```
    *(Output menampilkan: `none`)*
  - Pindah ke folder contoh dan jalankan program:
    ```bash
    cd /home/praktikan/Praktikum
    python3 hello.py
    python3 processes.py
    gcc -O2 hello.c -o hello && ./hello
    ```
- **Voiceover:**
  > *"Sekarang kita buktikan visi utama distro ini: kemampuan berjalan sepenuhnya tanpa internet.*  
  > *Kami matikan seluruh jaringan VM dengan `nmcli networking off`. Status konektivitas kini `none`.*  
  > *Kita jalankan program Python multiproses yang membuat proses anak fork PID independen, serta program C menggunakan GCC 13. Keduanya terkompilasi dan tereksekusi secara instan dan sempurna tanpa butuh koneksi internet sama sekali."*

---

### Menit 02:50 – 03:45 | Segmen 5: Keamanan Sistem & Akun Mahasiswa
- **Visual:**
  - Tampilkan perintah pembuatan akun praktikan:
    ```bash
    sudo labkita-postinstall praktikan
    ```
  - Masukkan password praktikan.
  - Tampilkan permission:
    ```bash
    stat /home/praktikan
    id praktikan
    ```
  - Masuk sebagai praktikan dan coba hak akses root:
    ```bash
    su - praktikan
    sudo -l
    ```
    *(Tampilkan pesan penolakan sudo)*.
- **Voiceover:**
  > *"Dari aspek keamanan sistem operasi, mahasiswa praktikan tidak boleh memiliki hak administratif. Skrip `labkita-postinstall` secara otomatis membuat akun mahasiswa tanpa grup `sudo`.*  
  > *Folder `/home/praktikan` diproteksi ketat dengan hak akses `0700`, sehingga user lain tidak bisa mengintip berkas latihan.*  
  > *Ketika user praktikan mencoba menjalankan `sudo -l`, sistem langsung menolak akses. Hal ini mencegah modifikasi berkas sistem atau instalasi software liar selama praktikum berlangsung."*

---

### Menit 03:45 – 04:30 | Segmen 6: Analisis Kinerja & Penutup
- **Visual:**
  - Jalankan perintah tolok ukur:
    ```bash
    free -m
    systemd-analyze time
    ```
  - Tampilkan slide penutup yang berisi identitas anggota tim (Dafa Zahran, Rafly Fauzi Pratama, Muhammad Ilham Rizky, Vadien Athallah Lukman) dan tautan repositori GitHub (https://github.com/luvices/labkita).
- **Voiceover:**
  > *"Terakhir, dari segi performa, penggunaan memori RAM LabKita 0.1 tercatat sekitar 1.34 GB dengan total boot time 59.9 detik pada konfigurasi 2 core vCPU dan RAM 4 GB.*  
  > *Demikian presentasi demonstrasi LabKita Linux 0.1 dari kelompok kami. Semoga distro ini dapat memberikan manfaat nyata bagi digitalisasi praktikum sistem operasi dan pemrograman dasar. Terima kasih!"*

---

## 3. Checklist Perekaman Video
- [ ] Resolusi rekaman minimal 1080p (1920x1080) atau 720p (1280x720) dengan framerate 30/60 fps.
- [ ] Font terminal disetel ukuran 14–16 pt agar terbaca jelas pada layar ponsel dosen.
- [ ] Suara mikrofon jernih tanpa noise berlebih.
- [ ] Format video: MP4 (H.264 / AAC).
- [ ] Tautan diunggah ke YouTube sebagai *Unlisted* atau simpan di Google Drive dengan akses *Anyone with link can view*.
