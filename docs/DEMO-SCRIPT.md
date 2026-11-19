# Naskah & Panduan Video Demo LabKita Linux 0.3
**Durasi Target:** 3 – 5 Menit  
**Platform Unggah:** YouTube (Unlisted) atau Google Drive  
**Mata Kuliah:** Sistem Operasi (Ganjil 2026/2027)  
**Dosen Pengampu:** Muhammad Sidik Asyaky, S.T., M.T.  

---

## 1. Ikhtisar Alur Video (Storyline)

| Segmen | Waktu (Durasi) | Fokus Visual | Poin Penjelasan / Voiceover |
| :---: | :---: | :--- | :--- |
| **1. Pembuka & Booting** | 00:00 – 00:45 (45s) | Slide Judul, Menu Boot GRUB 0.3 ID, Info Installer GUI vs TUI | Pengenalan LabKita Linux 0.3, perbaikan manifest `md5sum.txt` (`casper-md5check` pass), serta transparansi kegagalan installer GUI normal & fallback via `subiquity.cmd.tui`. |
| **2. Antarmuka macOS & Metadata 0.3** | 00:45 – 01:30 (45s) | Desktop 0.3, WhiteSur, Dock Tengah, Settings *Tentang* | Demonstrasi antarmuka bergaya macOS bebas aset proprietary Apple, tombol kiri, `Berkas` Bahasa Indonesia, serta verifikasi metadata konsisten `LabKita Linux 0.3`. |
| **3. Uji Mandiri & Uji Baca Snap (`labkita-check`)** | 01:30 – 02:15 (45s) | Terminal eksekusi `labkita-check` & `labkita-guide` Firefox Snap | Pembuktian `labkita-check` menguji lokasi non-dotfolder `~/Dokumen/Panduan-LabKita` dan pembacaan nyata `snap run --shell firefox`, lalu membuka panduan langsung di GUI Firefox Snap. |
| **4. Uji Offline Total & Eksekusi Program** | 02:15 – 03:00 (45s) | `nmcli networking off`, kompilasi C & Python | Mematikan jaringan VM secara total, membuktikan kompilasi GCC (`~/Praktikum`) dan Python multiproses (`processes.py`) berjalan 100% luring, serta tmpfs `/run/labkita`. |
| **5. Keamanan & Fix `labkita-postinstall`** | 03:00 – 03:50 (50s) | `sudo labkita-postinstall praktikan`, `id`, `stat`, `ls` | Pembuatan akun praktikan mulus tanpa error `printf --`, pembuktian izin privat `0700` dan isolasi non-sudo. |
| **6. Benchmark 5x (0.1 vs 0.2 vs 0.3) & Penutup** | 03:50 – 04:30 (40s) | `uname -r`, `free -m`, `systemd-analyze time`, Slide Penutup | Menunjukkan rata-rata & rentang 5x pengukuran RAM (`1.038,2` / `1.068,2` / `1.058,2 MiB`) dan boot (`8,460s` / `9,317s` / `8,808s`), perbedaan kernel (`7.0.0-31` vs `7.0.0-43`), dan kesimpulan jujur. |

---

## 2. Naskah Terperinci Langkah Demi Langkah (Voiceover Script)

### Menit 00:00 – 00:45 | Segmen 1: Pembukaan, Booting & Catatan Installer
- **Visual:**
  - Tampilkan judul video: *"LabKita Linux 0.3 - Distro Praktikum Pemrograman Offline Berbahasa Indonesia"*.
  - Tampilkan VMware Workstation menyala, memilih *"Coba atau Pasang LabKita Linux 0.3 (Bahasa Indonesia)"* di GRUB.
- **Voiceover:**
  > *"Halo semuanya! Di video demonstrasi Final Project Sistem Operasi kali ini, kelompok kami mempresentasikan **LabKita Linux versi 0.3**, distribusi berbasis Ubuntu 24.04.5 LTS untuk praktikum pemrograman dasar tanpa koneksi internet.*  
  > *Pada rilis 0.3 ini, seluruh label rilis telah diperbarui menjadi 0.3 dan manifest `md5sum.txt` telah diregenerasi sehingga `casper-md5check` lolos 100%. Secara jujur kami juga melaporkan bahwa di VM uji, sesi live masih membuka `gnome-initial-setup` dan installer GUI `ubuntu-desktop-bootstrap` tetap berhenti di dialog 'Ada yang salah', sehingga instalasi ke disk dijalankan melalui jalur fallback `subiquity.cmd.tui`."*

---

### Menit 00:45 – 01:30 | Segmen 2: Antarmuka WhiteSur, Bahasa Indonesia & Metadata 0.3
- **Visual:**
  - Tampilkan desktop terinstal 0.3 dengan wallpaper gradien LabKita, dock terpusat, tombol kiri, jendela *Berkas* (`Rumah / Dokumen / Panduan-LabKita`), dan *Pengaturan → Sistem → Tentang* (`LabKita Linux 0.3 (Noble Numbat)`).
- **Voiceover:**
  > *"Di sistem terinstal 0.3, layar sambutan, Pengaturan Tentang, dan `os-release` seluruhnya kini konsisten menampilkan LabKita Linux 0.3.*  
  > *Antarmuka memakai tema sumber terbuka WhiteSur GTK dan ikon dengan tombol jendela di kiri, dock bawah terpusat, dan antarmuka penuh Bahasa Indonesia tanpa aset proprietary Apple."*

---

### Menit 01:30 – 02:15 | Segmen 3: Uji Diagnostik `labkita-check` & Panduan Firefox Snap
- **Visual:**
  - Buka terminal (`Ctrl + Alt + T`) dan jalankan:
    ```bash
    labkita-check
    ```
  - Tunjukkan baris `[LULUS] Lokasi panduan non-dotfolder (~/Dokumen)` dan `[LULUS] Pembacaan panduan oleh sandbox Firefox Snap (AppArmor OK)`.
  - Jalankan `labkita-guide &` dan tampilkan Firefox Snap merender `file:///home/labkitaadmin/Dokumen/Panduan-LabKita/index.html`.
- **Voiceover:**
  > *"Pada LabKita 0.3, panduan offline telah dipindahkan dari dotfolder `.local` ke folder non-tersembunyi `~/Dokumen/Panduan-LabKita`.*  
  > *Perintah `labkita-check` kini tidak sekadar mengecek keberadaan file, melainkan benar-benar menguji pembacaan HTML dari dalam sandbox Firefox Snap. Saat kita jalankan `labkita-guide`, Firefox Snap terbuka normal tanpa blokir AppArmor lagi."*

---

### Menit 02:15 – 03:00 | Segmen 4: Uji Offline Total & Eksekusi Program
- **Visual:**
  - Di terminal, matikan jaringan dan uji kompilasi/eksekusi di `~/Praktikum`:
    ```bash
    nmcli networking off
    nmcli general status
    mkdir -p ~/Praktikum && cp /usr/share/labkita/examples/* ~/Praktikum/
    gcc ~/Praktikum/hello.c -o ~/Praktikum/hello_c && ~/Praktikum/hello_c
    python3 ~/Praktikum/hello.py
    python3 ~/Praktikum/processes.py
    systemctl is-active labkita-runtime.service && ls -ld /run/labkita
    ```
- **Voiceover:**
  > *"Dengan kondisi jaringan dimatikan total (`CONNECTIVITY: tidak ada`), mahasiswa tetap dapat mengompilasi program C di `~/Praktikum` serta mengeksekusi skrip Python dan `processes.py` multiproses secara instan.*  
  > *Layanan `labkita-runtime.service` juga memastikan `/run/labkita` berbasis tmpfs aktif dengan izin sticky bit `1777` sebagai ruang scratch sementara."*

---

### Menit 03:00 – 03:50 | Segmen 5: Keamanan Akun & Fix `labkita-postinstall`
- **Visual:**
  - Jalankan perintah pascainstalasi:
    ```bash
    sudo labkita-postinstall praktikan
    ```
    *(Ringkasan `[SUKSES]` tampil mulus tanpa error `printf`.)*
  - Verifikasi isolasi akun dan keberadaan panduan di akun `praktikan`:
    ```bash
    id praktikan
    sudo stat -c '%a %U:%G %n' /home/praktikan /home/praktikan/Dokumen/Panduan-LabKita/index.html
    ls /home/praktikan
    ```
- **Voiceover:**
  > *"Untuk akun mahasiswa, bug `printf` yang sempat muncul di ISO 0.2 sudah tuntas diperbaiki dengan `printf --` di 0.3.*  
  > *Akun `praktikan` dibuat tanpa hak sudo, direktori `/home/praktikan` terkunci izin `0700` sehingga pengguna lain langsung mendapat pesan `Ijin ditolak`, dan panduan belajar otomatis tersedia di `/home/praktikan/Dokumen/Panduan-LabKita`."*

---

### Menit 03:50 – 04:30 | Segmen 6: Tolok Ukur 5x (0.1 vs 0.2 vs 0.3) & Penutup
- **Visual:**
  - Jalankan di terminal:
    ```bash
    uname -r && free -m && systemd-analyze time
    ```
  - Tampilkan slide perbandingan 5x run per versi (`0.1`, `0.2`, `0.3`) dan slide identitas tim (Dafa Zahran, Rafly Fauzi Pratama, Muhammad Ilham Rizky, Vadien Athallah Lukman) beserta tautan repositori `https://github.com/luvices/labkita`.
- **Voiceover:**
  > *"Terakhir, dari 5 kali pengukuran ulang di VM yang sama setelah instalasi penuh: RAM rata-rata 0.3 tercatat 1.058,2 MiB (rentang 1.046–1.067 MiB), dibanding 0.1 (1.038,2 MiB; 1.016–1.056 MiB) dan 0.2 (1.068,2 MiB; 1.058–1.080 MiB). Waktu boot total 0.3 rata-rata 8,808 detik (8,460–9,014s), dibanding 0.1 (8,460s; 8,359–8,676s) dan 0.2 (9,317s; 9,072–9,458s).*  
  > *Perlu dicatat bahwa 0.3 menggunakan kernel `7.0.0-43-generic` sedangkan 0.1 dan 0.2 memakai `7.0.0-31-generic`, sehingga tidak ada klaim 'lebih cepat' atau 'lebih ringan'. Dengan sisa RAM ~2,85 GiB, LabKita Linux 0.3 siap dipakai praktikum offline. Terima kasih!"*

---

## 3. Checklist Perekaman Video
- [ ] Resolusi rekaman minimal 1080p (1920x1080) atau 720p (1280x720) dengan framerate 30/60 fps.
- [ ] Font terminal disetel ukuran 14–16 pt agar terbaca jelas pada layar monitor dan ponsel.
- [ ] Suara rekaman jernih tanpa derau latar belakang.
- [ ] Format video: MP4 (H.264 / AAC).
- [ ] Tautan diunggah ke YouTube sebagai *Unlisted* atau simpan di Google Drive dengan akses publik.
