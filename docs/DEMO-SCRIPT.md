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
| **4. Uji Offline Total & Eksekusi Program** | 02:15 – 03:00 (45s) | `nmcli networking off`, kompilasi C & Python | Mematikan adapter jaringan VM secara total, membuktikan kompilasi program C (`hello.c`) dan Python multiproses (`processes.py`) berjalan 100% luring, serta menjelaskan kendala nyata `labkita-guide` dengan Firefox Snap. |
| **5. Keamanan & Akun Praktikan** | 03:00 – 03:50 (50s) | `sudo labkita-postinstall praktikan`, `id`, `stat`, `ls` | Pembuatan akun praktikan, pembuktian pembatasan izin `0700` dan non-sudo, serta pelaporan jujur error baris 45 pada skrip ISO 0.2. |
| **6. Analisis Kinerja Empiris & Penutup** | 03:50 – 04:30 (40s) | `free -m`, `systemd-analyze time`, Slide Anggota Tim | Menunjukkan rata-rata RAM riil terinstal (1.060,0 MiB pada 0.2 vs 1.031,7 MiB pada 0.1), waktu boot rata-rata (11,454s pada 0.2 vs 9,893s pada 0.1), kesimpulan, dan penutup. |

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
    nmcli networking
    ```
    *(Output menampilkan: `disabled`)*
  - Kompilasi dan jalankan contoh program di sistem terinstal:
    ```bash
    gcc /usr/share/labkita/examples/hello.c -o /tmp/hello_test && /tmp/hello_test
    python3 /usr/share/labkita/examples/hello.py
    python3 /usr/share/labkita/examples/processes.py
    ```
  - Uji peluncur `labkita-guide` dan jelaskan secara terbuka kendala sandbox Firefox Snap pada dotfolder `~/.local/share/labkita/guide/`.
- **Voiceover:**
  > *"Sekarang kita buktikan kapabilitas utama distro ini dalam kondisi jaringan terputus total.*  
  > *Dengan jaringan dimatikan, mahasiswa tetap dapat mengompilasi program C dan menjalankan skrip Python multiproses untuk mempelajari fork dan konkurensi secara instan tanpa internet.*  
  > *Secara transparan, kami juga mencatat bahwa utilitas `labkita-guide` di rilis 0.2 ini masih terblokir AppArmor Firefox Snap karena file disalin ke dotfolder `.local`, sehingga menjadi agenda perbaikan utama ke folder non-tersembunyi pada rilis 0.3."*

---

### Menit 03:00 – 03:50 | Segmen 5: Keamanan Sistem & Akun Mahasiswa
- **Visual:**
  - Jalankan skrip pembuatan akun mahasiswa:
    ```bash
    sudo labkita-postinstall praktikan
    ```
  - Tampilkan permission dan isolasi akun:
    ```bash
    stat -c '%a %U:%G %n' /home/praktikan
    id praktikan
    ls /home/praktikan
    grep -E '^(sudo|adm):' /etc/group
    ```
- **Voiceover:**
  > *"Untuk aspek tata kelola laboratorium, skrip `labkita-postinstall` menyiapkan akun mahasiswa `praktikan` tanpa izin sudo.*  
  > *Folder kerja `/home/praktikan` diproteksi izin ketat `0700` sehingga user lain langsung ditolak (`Ijin ditolak`), dan `praktikan` tidak masuk grup `sudo` maupun `adm`.*  
  > *Catatan audit kami juga melaporkan bahwa pada ISO 0.2 baris 45 skrip ini memunculkan error `printf: - : pilihan tidak valid` meski akun sudah berhasil terbuat — dan perbaikan `printf --` sudah dimasukkan ke source repo."*

---

### Menit 03:50 – 04:30 | Segmen 6: Analisis Kinerja Empiris & Penutup
- **Visual:**
  - Jalankan perintah tolok ukur pada sistem terinstal:
    ```bash
    free -m
    systemd-analyze time
    ```
  - Tampilkan slide penutup yang berisi identitas anggota tim (Dafa Zahran, Rafly Fauzi Pratama, Muhammad Ilham Rizky, Vadien Athallah Lukman) dan tautan repositori GitHub (https://github.com/luvices/labkita).
- **Voiceover:**
  > *"Dari pengujian 3 kali reboot setelah instalasi pada VM 4 GB dengan kondisi identik, konsumsi RAM LabKita 0.2 rata-rata tercatat 1.060,0 MiB — naik wajar sekitar 28,3 MiB (+2,7%) dibanding versi 0.1 (1.031,7 MiB) akibat tema WhiteSur dan Dash-to-Dock.*  
  > *Sementara rata-rata waktu boot 0.2 berada di 11,454 detik dibanding 9,893 detik pada 0.1, sehingga tidak kami klaim lebih cepat; sisa RAM ~2,85 GiB tetap sangat memadai untuk kebutuhan praktikum.*  
  > *Demikian demonstrasi jujur LabKita Linux 0.2 dari kelompok kami. Terima kasih atas perhatiannya!"*

---

## 3. Checklist Perekaman Video
- [ ] Resolusi rekaman minimal 1080p (1920x1080) atau 720p (1280x720) dengan framerate 30/60 fps.
- [ ] Font terminal disetel ukuran 14–16 pt agar terbaca jelas pada layar monitor dan ponsel.
- [ ] Suara rekaman jernih tanpa derau latar belakang.
- [ ] Format video: MP4 (H.264 / AAC).
- [ ] Tautan diunggah ke YouTube sebagai *Unlisted* atau simpan di Google Drive dengan akses publik.
