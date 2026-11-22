# Naskah & Panduan Video Demo LabKita Linux 0.4
**Durasi Target:** 3 – 5 Menit  
**Platform Unggah:** YouTube (Unlisted) atau Google Drive  
**Mata Kuliah:** Sistem Operasi (Ganjil 2026/2027)  
**Dosen Pengampu:** Muhammad Sidik Asyaky, S.T., M.T.  

---

## 1. Ikhtisar Alur Video (Storyline)

| Segmen | Waktu (Durasi) | Fokus Visual | Poin Penjelasan / Voiceover |
| :---: | :---: | :--- | :--- |
| **1. Pembuka & Booting** | 00:00 – 00:45 (45s) | Slide Judul, GRUB 0.4 ID, Autologin Live `labkita`, Info GUI vs TUI | Pengenalan LabKita Linux 0.4, pemulihan **autologin live session** (fix bentrok grup `labkita` -> `labkita-praktikum`), serta transparansi keterbatasan GUI installer pada ISO build Cubic & prosedur resmi via `subiquity.cmd.tui`. |
| **2. Antarmuka macOS & Metadata 0.4** | 00:45 – 01:30 (45s) | Desktop 0.4, WhiteSur, Dock Tengah, Sambutan 0.4 & `os-release` | Demonstrasi antarmuka bergaya macOS bebas aset proprietary Apple, tombol kiri, `Berkas` Bahasa Indonesia, serta verifikasi metadata konsisten `LabKita Linux 0.4`. |
| **3. Uji Mandiri & Uji Baca Snap (`labkita-check`)** | 01:30 – 02:15 (45s) | Terminal `labkita-check` (`23/23`) & `labkita-guide` Firefox Snap | Pembuktian `labkita-check` menguji lokasi non-dotfolder `~/Dokumen/Panduan-LabKita` dan pembacaan nyata `snap run firefox`, lalu membuka panduan `0.4` langsung di GUI Firefox Snap. |
| **4. Uji Offline Total & Eksekusi Program** | 02:15 – 03:00 (45s) | `nmcli networking off`, kompilasi C & Python | Mematikan jaringan VM secara total, membuktikan kompilasi GCC (`~/Praktikum`) dan Python multiproses (`processes.py`) berjalan 100% luring, serta tmpfs `/run/labkita`. |
| **5. Keamanan & Grup `labkita-praktikum`** | 03:00 – 03:50 (50s) | `sudo labkita-postinstall praktikan`, `id`, `stat`, `getent group` | Pembuatan akun praktikan mulus (`0` error `printf`), isolasi non-`sudo`, izin privat `0700`, dan grup sistem `labkita-praktikum` (grup `labkita` tidak ada lagi). |
| **6. Benchmark 5x (0.1–0.4) & Penutup** | 03:50 – 04:30 (40s) | `uname -r`, `free -m`, `systemd-analyze time`, Slide Penutup | Menunjukkan rata-rata & rentang 5x pengukuran RAM (`1.038,2` / `1.068,2` / `1.058,2` / `1.062,6 MiB`) dan boot (`8,460s` / `9,317s` / `8,808s` / `9,185s`), perbedaan kernel (`7.0.0-31` vs `7.0.0-43`), dan kesimpulan: tidak ada perbedaan yang dapat dibuktikan. |

---

## 2. Naskah Terperinci Langkah Demi Langkah (Voiceover Script)

### Menit 00:00 – 00:45 | Segmen 1: Pembukaan, Booting & Catatan Installer
- **Visual:**
  - Tampilkan judul video: *"LabKita Linux 0.4 - Distro Praktikum Pemrograman Offline Berbahasa Indonesia"*.
  - Tampilkan VMware Workstation menyala, memilih *"Coba atau Pasang LabKita Linux 0.4 (Bahasa Indonesia)"* di GRUB, lalu langsung masuk ke desktop live `labkita` tanpa `gnome-initial-setup`.
- **Voiceover:**
  > *"Halo semuanya! Di video demonstrasi Final Project Sistem Operasi kali ini, kelompok kami mempresentasikan **LabKita Linux versi 0.4**, distribusi berbasis Ubuntu 24.04.5 LTS untuk praktikum pemrograman dasar tanpa koneksi internet.*  
  > *Dari eksperimen kontrol (Ubuntu asli lulus di VM identik) dan 4 tahap bisect manual di WSL, kami membuktikan bahwa bentrok `.disk/info` `'LabKita...'` dengan `groupadd --system labkita` menyebabkan `casper` gagal membuat user live (`The group 'labkita' already exists`), memicu `gnome-initial-setup` dan error installer. Di versi **0.4** ini, grup sistem diganti menjadi `labkita-praktikum`: **autologin sesi live kini pulih dan langsung masuk desktop `labkita`**. Namun, pada ISO 0.4 hasil build Cubic, installer GUI `ubuntu-desktop-bootstrap` masih terhenti di 'Ada yang salah' setelah `Inhibiting Gnome session`, sehingga karena perbedaan lingkungan build WSL vs Cubic, **prosedur instalasi resmi ke disk tetap menggunakan `subiquity.cmd.tui`**."*

---

### Menit 00:45 – 01:30 | Segmen 2: Antarmuka WhiteSur, Bahasa Indonesia & Metadata 0.4
- **Visual:**
  - Tampilkan desktop terinstal 0.4 dengan dialog sambutan `LabKita Linux 0.4`, wallpaper gradien LabKita, dock terpusat, tombol kiri, jendela *Berkas*, dan terminal `cat /etc/os-release /etc/labkita-release`.
- **Voiceover:**
  > *"Di sistem terinstal 0.4, layar sambutan, `/etc/labkita-release`, dan `/etc/os-release` seluruhnya konsisten menampilkan LabKita Linux 0.4.*  
  > *Antarmuka memakai tema sumber terbuka WhiteSur GTK dan ikon dengan tombol jendela di kiri, dock bawah terpusat, dan antarmuka penuh Bahasa Indonesia tanpa aset proprietary Apple."*

---

### Menit 01:30 – 02:15 | Segmen 3: Uji Diagnostik `labkita-check` & Panduan Firefox Snap
- **Visual:**
  - Buka terminal (`Ctrl + Alt + T`) dan jalankan:
    ```bash
    labkita-check
    ```
  - Tunjukkan hasil **`23/23 [LULUS]`** termasuk `[LULUS] Lokasi panduan non-dotfolder (~/Dokumen)` dan `[LULUS] Pembacaan panduan oleh sandbox Firefox Snap (AppArmor OK)`.
  - Jalankan `labkita-guide &` dan tampilkan Firefox Snap merender `file:///home/labkitavm/Dokumen/Panduan-LabKita/index.html` dengan lencana `LabKita Linux 0.4`.
- **Voiceover:**
  > *"Perintah `labkita-check` menjalankan 23 pemeriksaan otomatis yang seluruhnya lulus—termasuk menguji langsung pembacaan file HTML di `~/Dokumen/Panduan-LabKita` dari dalam sandbox Firefox Snap. Saat `labkita-guide` dijalankan, panduan versi 0.4 terbuka normal di Firefox Snap tanpa blokir AppArmor."*

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

### Menit 03:00 – 03:50 | Segmen 5: Keamanan Akun & Grup `labkita-praktikum`
- **Visual:**
  - Jalankan perintah pascainstalasi:
    ```bash
    sudo labkita-postinstall praktikan
    ```
    *(Ringkasan `[SUKSES]` tampil mulus tanpa error `printf`.)*
  - Verifikasi grup `labkita-praktikum`, tidak adanya grup `labkita`, dan isolasi akun:
    ```bash
    getent group labkita || echo "NO_LABKITA_GROUP"
    getent group labkita-praktikum
    id praktikan
    sudo stat -c '%a %U:%G %n' /home/praktikan /home/praktikan/Dokumen/Panduan-LabKita/index.html
    ls /home/praktikan
    ```
- **Voiceover:**
  > *"Untuk akun mahasiswa, skrip `labkita-postinstall` berjalan mulus dan mendaftarkan akun `praktikan` ke grup sistem `labkita-praktikum` (grup `labkita` sudah tidak digunakan agar tidak membentrok `casper`).*  
  > *Akun `praktikan` dibuat tanpa hak `sudo`, dan direktori `/home/praktikan` terkunci izin `0700` sehingga pengguna lain langsung mendapat pesan `Permission denied`."*

---

### Menit 03:50 – 04:30 | Segmen 6: Tolok Ukur 5x (0.1 vs 0.2 vs 0.3 vs 0.4) & Penutup
- **Visual:**
  - Jalankan di terminal:
    ```bash
    uname -r && free -m && systemd-analyze time
    ```
  - Tampilkan slide perbandingan 5x run per versi (`0.1`, `0.2`, `0.3`, `0.4`) dan slide identitas tim (Dafa Zahran, Rafly Fauzi Pratama, Muhammad Ilham Rizky, Vadien Athallah Lukman) beserta tautan repositori `https://github.com/luvices/labkita`.
- **Voiceover:**
  > *"Terakhir, dari 5 kali pengukuran ulang di VM yang sama setelah instalasi penuh: RAM rata-rata 0.4 tercatat 1.062,6 MiB (rentang 1.043–1.075 MiB), dibanding 0.1 (1.038,2 MiB; 1.016–1.056 MiB), 0.2 (1.068,2 MiB; 1.058–1.080 MiB), dan 0.3 (1.058,2 MiB; 1.046–1.067 MiB). Waktu boot total 0.4 rata-rata 9,185 detik (8,520–10,713s), dibanding 0.1 (8,460s), 0.2 (9,317s), dan 0.3 (8,808s).*  
  > *Karena rentang pengukuran saling tumpang tindih dan terdapat perbedaan versi kernel (`7.0.0-43-generic` pada `0.3`/`0.4` vs `7.0.0-31-generic` pada `0.1`/`0.2`), **tidak ada perbedaan yang dapat dibuktikan** dan tidak ada klaim 'lebih cepat' atau 'lebih ringan'. Dengan sisa RAM ~2,85 GiB dan autologin live yang telah pulih, LabKita Linux 0.4 siap dipakai praktikum offline. Terima kasih!"*

---

## 3. Checklist Perekaman Video
- [ ] Resolusi rekaman minimal 1080p (1920x1080) atau 720p (1280x720) dengan framerate 30/60 fps.
- [ ] Font terminal disetel ukuran 14–16 pt agar terbaca jelas pada layar monitor dan ponsel.
- [ ] Suara rekaman jernih tanpa derau latar belakang.
- [ ] Format video: MP4 (H.264 / AAC).
- [ ] Tautan diunggah ke YouTube sebagai *Unlisted* atau simpan di Google Drive dengan akses publik.
