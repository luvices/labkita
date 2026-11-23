# Naskah & Panduan Video Demo LabKita Linux 0.5
**Durasi Target:** 3 – 5 Menit  
**Platform Unggah:** YouTube (Unlisted) atau Google Drive  
**Mata Kuliah:** Sistem Operasi (Ganjil 2026/2027)  
**Dosen Pengampu:** Muhammad Sidik Asyaky, S.T., M.T.  

---

## 1. Ikhtisar Alur Video (Storyline)

| Segmen | Waktu (Durasi) | Fokus Visual | Poin Penjelasan / Voiceover |
| :---: | :---: | :--- | :--- |
| **1. Pembuka, Booting & GUI Installer 0.5** | 00:00 – 00:45 (45s) | Slide Judul, GRUB 0.5 ID, Autologin Live `ubuntu`, Installer GUI *"Instalasi selesai"* | Pengenalan LabKita Linux 0.5 (build WSL `v0.5-iso`), pemulihan penuh **installer GUI `ubuntu-desktop-bootstrap`** dibanding arsip Cubic `0.1`–`0.4` (TUI `subiquity.cmd.tui` sebagai cadangan). |
| **2. Antarmuka macOS & Metadata 0.5** | 00:45 – 01:30 (45s) | Desktop 0.5, WhiteSur, Dock Tengah, Sambutan 0.5 & `os-release` | Demonstrasi antarmuka bergaya macOS bebas aset proprietary Apple, tombol kiri, `Rumah` Bahasa Indonesia, serta verifikasi metadata konsisten `LabKita Linux 0.5`. |
| **3. Uji Mandiri & Uji Baca Snap (`labkita-check`)** | 01:30 – 02:15 (45s) | Terminal `labkita-check` (SEMUA LULUS) & `labkita-guide` Firefox Snap | Pembuktian `labkita-check` menguji lokasi non-dotfolder `~/Dokumen/Panduan-LabKita` dan pembacaan nyata `snap run firefox`, lalu membuka panduan `0.5` langsung di GUI Firefox Snap. |
| **4. Uji Offline Total & Eksekusi Program** | 02:15 – 03:00 (45s) | Kompilasi C, eksekusi Python multiproses & tmpfs `/run/labkita` `1777` | Mematikan jaringan atau bekerja tanpa internet, membuktikan kompilasi GCC dan Python multiproses berjalan 100% luring, serta tmpfs `/run/labkita`. |
| **5. Keamanan & Grup `labkita-praktikum`** | 03:00 – 03:50 (50s) | `sudo labkita-postinstall praktikan`, `id`, `stat` | Pembuatan akun praktikan mulus, isolasi non-`sudo`, izin privat `0700`, dan grup sistem `labkita-praktikum` (tanpa grup `'labkita'`). |
| **6. Benchmark 5x (0.1–0.5) & Penutup** | 03:50 – 04:30 (40s) | `uname -r`, `free -m`, `systemd-analyze time`, Slide Penutup | Menunjukkan rata-rata & rentang 5x pengukuran RAM (`1.042,8 MiB` pada 0.5) dan boot (`9,036s` pada 0.5) vs `0.1`–`0.4`, perbedaan kernel (`7.0.0-31` vs `7.0.0-43`), dan kesimpulan: tidak ada perbedaan yang dapat dibuktikan. |

---

## 2. Naskah Terperinci Langkah Demi Langkah (Voiceover Script)

### Menit 00:00 – 00:45 | Segmen 1: Pembukaan, Booting & Pemulihan Installer GUI 0.5
- **Visual:**
  - Tampilkan judul video: *"LabKita Linux 0.5 - Distro Praktikum Pemrograman Offline Berbahasa Indonesia"*.
  - Tampilkan VMware Workstation menyala, memilih *"Coba atau Pasang LabKita Linux 0.5 (Bahasa Indonesia)"* di GRUB, langsung masuk ke desktop live `ubuntu` dengan jendela **installer GUI `ubuntu-desktop-bootstrap`** menampilkan Bahasa Indonesia hingga *"Instalasi selesai"*.
- **Voiceover:**
  > *"Halo semuanya! Di video demonstrasi Final Project Sistem Operasi kali ini, kelompok kami mempresentasikan **LabKita Linux versi 0.5**, distribusi berbasis Ubuntu 24.04.5 LTS untuk praktikum pemrograman dasar tanpa koneksi internet.*  
  > *Pada arsip build Cubic 0.1–0.4 sebelumnya, installer GUI sempat gagal di dialog 'Ada yang salah' sehingga harus memakai TUI. Melalui eksperimen kontrol dan build reproducible WSL pada tag **`v0.5-iso`** (`tools/build_v05.py`), kami menemukan bahwa `.disk/info` tanpa tanda kutip memicu `RangeError` pada `ProductService` installer, dan dengan format `.disk/info` `Ubuntu 24.04 LabKita 0.5 "Noble Numbat"` + grup `labkita-praktikum`, **autologin live maupun installer GUI `ubuntu-desktop-bootstrap` kini berjalan penuh hingga Instalasi selesai**—dengan TUI `subiquity.cmd.tui` tetap siap sebagai cadangan."*

---

### Menit 00:45 – 01:30 | Segmen 2: Antarmuka WhiteSur, Bahasa Indonesia & Metadata 0.5
- **Visual:**
  - Tampilkan desktop terinstal 0.5 dengan dialog sambutan `Selamat datang di LabKita Linux 0.5 (Noble Numbat)!`, wallpaper gradien LabKita, dock terpusat, tombol kiri, ikon *Rumah* Bahasa Indonesia, dan terminal `cat /etc/os-release`.
- **Voiceover:**
  > *"Di sistem terinstal 0.5, layar sambutan, `/etc/labkita-release`, dan `/etc/os-release` seluruhnya konsisten menampilkan LabKita Linux 0.5.*  
  > *Antarmuka memakai tema sumber terbuka WhiteSur GTK dan ikon dengan tombol jendela di kiri, dock bawah terpusat, dan antarmuka penuh Bahasa Indonesia tanpa aset proprietary Apple."*

---

### Menit 01:30 – 02:15 | Segmen 3: Uji Diagnostik `labkita-check` & Panduan Firefox Snap
- **Visual:**
  - Buka terminal (`Ctrl + Alt + T`) dan jalankan:
    ```bash
    labkita-check
    ```
  - Tunjukkan hasil **`Hasil: SEMUA PEMERIKSAAN LULUS`** termasuk `[LULUS] Lokasi panduan non-dotfolder (~/Dokumen)` dan `[LULUS] Pembacaan panduan oleh sandbox Firefox Snap (AppArmor OK)`.
  - Jalankan `labkita-guide &` dan tampilkan Firefox Snap merender `file:///home/labadmin/Dokumen/Panduan-LabKita/index.html` dengan lencana `LabKita Linux 0.5`.
- **Voiceover:**
  > *"Perintah `labkita-check` menjalankan pemeriksaan otomatis yang seluruhnya lulus—termasuk menguji langsung pembacaan file HTML di `~/Dokumen/Panduan-LabKita` dari dalam sandbox Firefox Snap. Saat `labkita-guide` dijalankan, panduan versi 0.5 terbuka normal di Firefox Snap tanpa blokir AppArmor."*

---

### Menit 02:15 – 03:00 | Segmen 4: Uji Offline Total & Eksekusi Program
- **Visual:**
  - Di terminal, uji offline + kompilasi/eksekusi di `~/Praktikum`:
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
  > *"Dengan kondisi jaringan dimatikan total, mahasiswa tetap dapat mengompilasi program C di `~/Praktikum` serta mengeksekusi skrip Python dan `processes.py` multiproses secara instan.*  
  > *Layanan `labkita-runtime.service` juga memastikan `/run/labkita` berbasis tmpfs aktif dengan izin sticky bit `1777` sebagai ruang scratch sementara."*

---

### Menit 03:00 – 03:50 | Segmen 5: Keamanan Akun & Grup `labkita-praktikum`
- **Visual:**
  - Jalankan perintah pascainstalasi:
    ```bash
    sudo labkita-postinstall praktikan
    ```
  - Verifikasi grup `labkita-praktikum`, tidak adanya grup `labkita`, dan isolasi akun:
    ```bash
    getent group labkita || echo "NO_LABKITA_GROUP"
    getent group labkita-praktikum
    id praktikan
    sudo stat -c '%a %U:%G %n' /home/praktikan
    ```
- **Voiceover:**
  > *"Untuk akun mahasiswa, skrip `labkita-postinstall` berjalan mulus dan mendaftarkan akun `praktikan` ke grup sistem `labkita-praktikum` tanpa hak `sudo`.*  
  > *Direktori `/home/praktikan` terkunci izin `0700` sehingga akun lain tidak bisa mengintip berkas praktikum mahasiswa lain."*

---

### Menit 03:50 – 04:30 | Segmen 6: Tolok Ukur 5x (0.1–0.5) & Penutup
- **Visual:**
  - Jalankan `uname -r && free -m && systemd-analyze time`, tampilkan slide perbandingan 5x run `0.1`–`0.5` dan slide tim (Dafa Zahran, Rafly Fauzi Pratama, Muhammad Ilham Rizky, Vadien Athallah Lukman) beserta tautan repositori `https://github.com/luvices/labkita`.
- **Voiceover:**
  > *"Terakhir, dari 5 kali pengukuran ulang di VM yang sama setelah instalasi penuh: RAM rata-rata 0.5 tercatat 1.042,8 MiB (rentang 1.031–1.054 MiB) dibanding 0.1–0.4 (1.038,2–1.068,2 MiB), dan waktu boot total 0.5 rata-rata 9,036 detik (rentang 8,349–9,515s) dibanding 0.1–0.4 (8,460–9,317s).*  
  > *Karena rentang pengukuran saling tumpang tindih dan ada perbedaan kernel (`7.0.0-43-generic` pada `0.3`–`0.5` vs `7.0.0-31-generic` pada `0.1`/`0.2`), **tidak ada perbedaan yang dapat dibuktikan** dan tidak ada klaim 'lebih cepat' atau 'lebih ringan'. Dengan installer GUI yang sudah pulih penuh di 0.5 (`v0.5-iso`), LabKita Linux siap digunakan praktikum offline. Terima kasih!"*

---

## 3. Checklist Perekaman Video
- [ ] Resolusi rekaman minimal 1080p (1920x1080) atau 720p (1280x720) dengan framerate 30/60 fps.
- [ ] Font terminal disetel ukuran 14–16 pt agar terbaca jelas pada layar monitor dan ponsel.
- [ ] Suara rekaman jernih tanpa derau latar belakang.
- [ ] Format video: MP4 (H.264 / AAC).
- [ ] Tautan diunggah ke YouTube sebagai *Unlisted* atau simpan di Google Drive dengan akses publik.
