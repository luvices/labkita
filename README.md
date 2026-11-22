# LabKita Linux

Distribusi sistem operasi berbasis Ubuntu 24.04 LTS (Noble Numbat) yang dikustomisasi khusus untuk kebutuhan **praktikum pemrograman dasar dan sistem operasi secara luring (*offline*)** di laboratorium komputer kampus tanpa ketergantungan koneksi internet.

Proyek ini dikembangkan sebagai luaran **Final Project Mata Kuliah Sistem Operasi**, Semester Ganjil 2026/2027.  
**Dosen Pengampu:** Muhammad Sidik Asyaky, S.T., M.T.

---

## 1. Identitas Rilis & Checksum ISO

| Atribut | Detail |
| --- | --- |
| **Nama Distro** | LabKita Linux |
| **Versi Rilis** | 0.3 |
| **Basis Sistem** | Ubuntu 24.04.5 LTS Desktop (amd64) |
| **Arsitektur** | x86_64 / amd64 |
| **Nama Berkas ISO** | `labkita-linux-0.3-amd64.iso` |
| **Ukuran Berkas** | 6.520.272.896 bytes (~6.07 GiB / 6.52 GB) |
| **SHA256 Checksum** | `21f38dc158a010e6f80920274dd7b8cd8f3e0d7f5e91283a310e98e53f045387` |
| **MD5 Checksum** | `521f315f62a6c7cd08a31d40ad8c9fb5` |
| **Metode Build** | Cubic (*Custom Ubuntu ISO Creator*) `2026.09.110-release~202609120048~ubuntu24.04.1` |
| **Status Verifikasi** | Teruji pascainstalasi di VM (`md5sum` ISO `957/957` lulus, `casper-md5check` pass, `labkita-check` + uji baca sandbox Firefox Snap lulus, `labkita-postinstall` `printf --` lulus; installer GUI normal & autologin live masih gagal — lihat [`docs/TEST-PLAN.md`](docs/TEST-PLAN.md)) |

### Verifikasi Integritas Berkas
Sebelum mengimpor atau membakar ISO ke media instalasi, lakukan verifikasi integritas berkas:

- **PowerShell (Windows):**
  ```powershell
  Get-FileHash -Algorithm SHA256 .\labkita-linux-0.3-amd64.iso
  # Hash: 21F38DC158A010E6F80920274DD7B8CD8F3E0D7F5E91283A310E98E53F045387
  ```

- **Linux / macOS (Bash):**
  ```bash
  sha256sum labkita-linux-0.3-amd64.iso
  # 21f38dc158a010e6f80920274dd7b8cd8f3e0d7f5e91283a310e98e53f045387  labkita-linux-0.3-amd64.iso
  ```

---

## 2. Latar Belakang & Fitur Utama

Laboratorium komputer kampus sering menghadapi masalah koneksi internet yang lambat atau tidak stabil saat praktikum berlangsung. LabKita Linux dirancang agar mahasiswa dan asisten lab dapat menjalankan sesi praktikum secara mandiri tanpa membutuhkan akses repository online.

### Fitur & Perbaikan pada Versi 0.3:
1. **Lokalisasi Penuh Bahasa Indonesia & Konsistensi Branding 0.3:**
   - Integrasi paket bahasa lengkap: `language-pack-id`, `language-pack-gnome-id`, `hunspell-id`, dan `firefox-locale-id`.
   - Konfigurasi default sistem: Locale `id_ID.UTF-8`, zona waktu `Asia/Jakarta` (WIB), dan tata letak papan tik `us`.
   - Seluruh label rilis lama `0.1`/`0.2` diperbarui menjadi `0.3`: GRUB (`Coba atau Pasang LabKita Linux 0.3 (Bahasa Indonesia)`), `/usr/lib/os-release` & `/etc/lsb-release` (`LabKita Linux 0.3`), `/etc/labkita-release`, layar sambutan pertama, `casper/install-sources.yaml`, dan `labkita-guide`. *(Catatan jujur: sesi live masih masuk ke wizard `gnome-initial-setup` karena autologin `labkita` belum aktif.)*
   - Penerjemahan seluruh teks utilitas mandiri: `labkita-check`, `labkita-postinstall`, dan launcher panduan.

2. **Antarmuka Modern Bergaya macOS (100% Bebas Aset Proprietary Apple):**
   - Menggunakan tema sumber terbuka berlisensi resmi: **WhiteSur GTK Theme** (Light & Dark) dan **WhiteSur Icon Theme** karya vinceliuice (lisensi GPL-3.0 / CC-BY-SA-4.0).
   - Tema kursor bergaya macOS halus (**WhiteSur Cursors**) dan tipografi **Inter Font** (`fonts-inter`) yang nyaman dibaca untuk coding.
   - Tata letak desktop: Dock terpusat di bagian bawah layar (*centered bottom dock*), tombol kontrol jendela di sebelah kiri (`close,minimize,maximize:`), sudut jendela membulat, dan *top bar* bersih. *(Catatan minor: pada 0.3, slot ikon Terminal & Berkas di dock tampak redup saat tidak aktif.)*
   - Wallpaper orisinal LabKita gradien minimalis (format SVG & PNG 4K). Seluruh atribusi lisensi didokumentasikan di [`docs/CREDITS.md`](docs/CREDITS.md).

3. **Toolchain Pemrograman Lengkap & Panduan Lolos Sandbox Firefox Snap:**
   - **C/C++:** GCC 13.3.0, G++ 13.3.0, GNU Make 4.3, GDB, dan paket `build-essential`.
   - **Python:** Python 3.12.3, modul venv, dan dokumentasi pustaka offline.
   - **Editor & IDE:** Geany 2.0 (terkonfigurasi build shortcut C dan Python), GNU Nano, dan Git 2.43.
   - **Panduan Offline di `~/Dokumen/Panduan-LabKita`:** `labkita-guide` kini menyalin HTML panduan dari `/usr/share/labkita/guide/` ke direktori non-dotfolder `$HOME/Dokumen/Panduan-LabKita/` (menghormati `xdg-user-dir DOCUMENTS`, termasuk `/etc/skel/Dokumen/Panduan-LabKita/`) sehingga **terbuka & terender normal di Firefox Snap** tanpa blokir AppArmor.

4. **Isolasi Keamanan & Perbaikan `labkita-postinstall`:**
   - Utilitas `/usr/local/sbin/labkita-postinstall` terpaket rapi di ISO 0.3 dengan perbaikan **`printf --`** (mengatasi error `printf: - : pilihan tidak valid` pada ISO 0.2), sekaligus menyalin panduan ke `/home/<user>/Dokumen/Panduan-LabKita/`.
   - Direktori `/home/praktikan` dilindungi izin akses ketat `0700` (`drwx------`), mencegah akses tidak sah antarmahasiswa.
   - Akun mahasiswa **tidak memiliki hak `sudo`**, sehingga konfigurasi sistem dan berkas lab aman dari perusakan yang tidak disengaja.

5. **Workspace Temporer Cepat (RAM Disk tmpfs) & Regenerasi `md5sum.txt` ISO:**
   - Layanan systemd `labkita-runtime.service` otomatis membuat `/run/labkita` berbasis memori RAM (*tmpfs*) dengan sticky bit `1777` (`drwxrwxrwt`). *(Catatan: `/run` dipasang `noexec` oleh sistem, sehingga binary hasil kompilasi dijalankan dari `~/Praktikum`, sementara `/run/labkita` dipakai untuk berkas scratch sementara).*
   - Manifest `md5sum.txt` ISO 0.3 diregenerasi setelah seluruh berkas final terbentuk dan lolos verifikasi **`957/957 OK`** di ISO terpasang loop serta `casper-md5check: pass` saat live boot. *(Catatan: meskipun checksum lulus, installer GUI normal `ubuntu-desktop-bootstrap` masih gagal memunculkan dialog `"Ada yang salah"` di VM sehingga instalasi memakai fallback `subiquity.cmd.tui`.)*

6. **Suite Diagnostik Mandiri dengan Tes Baca Sandbox (`labkita-check`):**
   - Memverifikasi toolchain, locale, timezone, tema WhiteSur, wallpaper, tmpfs, layanan runtime, lokasi non-dotfolder `~/Dokumen/Panduan-LabKita`, asosiasi `xdg-mime`, sekaligus **menguji pembacaan nyata file HTML melalui `snap run --shell firefox -c 'cat "$1"'`** (`AppArmor OK`).

---

## 3. Hasil Pengujian & Tolok Ukur Empiris (0.1 vs 0.2 vs 0.3)

Pengujian empiris dilakukan ulang **setelah instalasi penuh ke disk kosong** pada VMware Workstation dalam **kondisi identik** (VM `labkita-test.vmx`: 2 vCPU, RAM 4096 MB / `3911 MiB` usable, Disk 40 GB SCSI, **5 kali reboot bersih per versi**, pengukuran 20 detik setelah desktop siap).  
*Catatan variabel:* `0.1` dan `0.2` berjalan pada kernel **`7.0.0-31-generic`**, sedangkan `0.3` berjalan pada kernel **`7.0.0-43-generic`**.

| Pengujian | Perintah / Tolok Ukur | LabKita 0.1 | LabKita 0.2 | LabKita 0.3 (Terinstal) | Status 0.3 |
| --- | --- | :---: | :---: | :---: | :---: |
| **Integritas ISO (`md5sum.txt`)** | `md5sum -c` & `casper-md5check` | — | Gagal mismatch | **957/957 OK; `casper-md5check` `pass`** | **LULUS** |
| **Boot Menu GRUB** | Layar GRUB 2.12 | Bahasa Inggris | Bahasa Indonesia | **LabKita Linux 0.3 (Bahasa Indonesia)** | **LULUS** |
| **Autologin Live Session** | Live boot tanpa wizard | Jatuh ke `gnome-initial-setup` | Jatuh ke `gnome-initial-setup` | **Masih jatuh ke `gnome-initial-setup`** | **GAGAL** |
| **Installer GUI** | `ubuntu-desktop-bootstrap` | Gagal | Gagal (*Ada yang salah*) | **Masih gagal (*Ada yang salah*) meski md5 pass** | **GAGAL** |
| **Instalasi ke Disk** | `subiquity.cmd.tui` | Sukses hingga reboot | Sukses hingga reboot | **Sukses (*LabKita Linux 0.3*) hingga reboot** | **LULUS (Fallback)** |
| **Self-Diagnostic Suite** | `labkita-check` | Lulus (cek dasar) | 21/21 (cek file) | **Semua Lulus + uji baca `snap run firefox` OK** | **LULUS** |
| **Konsumsi RAM (5x)** | `free -m` Used (rata-rata & rentang) | **1.038,2 MiB** *(1016–1056)* | **1.068,2 MiB** *(1058–1080)* | **1.058,2 MiB** *(1046–1067 MiB)* | **TERUKUR** |
| **Waktu Booting (5x)** | `systemd-analyze time` (rata-rata & rentang) | **8,460s** *(8,359–8,676s)* | **9,317s** *(9,072–9,458s)* | **8,808s** *(8,460–9,014s)* | **TERUKUR** |
| **Konsistensi Branding** | `os-release`, sambutan, Pengaturan | Label `0.1` | Sisa label `0.1` | **Seluruh label & Tentang tampil `0.3`** | **LULUS** |
| **Tampilan WhiteSur & ID** | Desktop, dock, `Berkas` | Default Yaru (EN) | WhiteSur + Dock (ID) | **WhiteSur + Dock + ID** *(catatan minor ikon dock)* | **LULUS** |
| **Pembuatan Akun Praktikan** | `sudo labkita-postinstall praktikan` | Lulus | Error `printf` baris 45 | **Lulus mulus (fix `printf --`, 0 error)** | **LULUS** |
| **Isolasi Akun & Izin 0700** | `id`, `stat`, `ls /home/praktikan` | `0700` / ditolak | `0700` / ditolak | **`0700`, `Ijin ditolak`, non-`sudo`** | **LULUS** |
| **Akses Panduan Firefox Snap** | `labkita-guide` GUI Firefox Snap | Terblokir `/usr/share` | Terblokir `~/.local` | **Terbuka & terender di `~/Dokumen/Panduan-LabKita`** | **LULUS** |
| **Kompilasi & Eksekusi Offline** | `nmcli networking off`, `gcc`, `python3` | Lulus | Lulus | **Lulus: C (`~/Praktikum`), Python, `processes.py`** | **LULUS** |
| **Ruang Kerja Tmpfs** | `/run/labkita` (`1777`) | Mode `1777` | Mode `1777` | **Mode `1777` aktif (`noexec` pada `/run`)** | **LULUS** |

> **Catatan Analisis Kinerja Empiris (Tanpa Klaim "Lebih Ringan/Cepat"):**  
> Pada 5 kali pengujian identik setelah instalasi per versi, **tidak ada perbedaan yang dapat dibuktikan antara 0.3 dan 0.1/0.2, dan tidak ada klaim lebih ringan/lebih cepat untuk versi mana pun**: konsumsi RAM rata-rata `0.3` tercatat **`1.058,2 MiB`** (rentang `1.046–1.067 MiB`) dan `0.2` **`1.068,2 MiB`** (`1.058–1.080 MiB`), dibanding `0.1` **`1.038,2 MiB`** (`1.016–1.056 MiB`) (dengan rentang `0.3` saling tumpang tindih dengan `0.1` dan `0.2`). Untuk waktu boot, rata-rata `0.3` adalah **`8,808 detik`** (`8,460s–9,014s`, tumpang tindih dengan `0.1` **`8,460s`** / `8,359s–8,676s`); meski 5 run `0.3` seluruhnya berada di bawah rentang `0.2` (`9,317s` / `9,072s–9,458s`), **perbedaan versi kernel (`7.0.0-43-generic` pada `0.3` vs `7.0.0-31-generic` pada `0.1`/`0.2`) menjadi variabel pembeda**, sehingga selisih tersebut tidak diklaim sebagai hasil optimasi LabKita. Sisa RAM tersedia `0.3` rata-rata **`2.852,0 MiB`** (~`2,79 GiB`) tetap memadai untuk praktikum.

*Eksperimen kontrol installer GUI (Ubuntu asli sukses; LabKita 0.3 gagal pada 3D mati maupun hidup; 3 build bisect bertahap—repack tanpa `customize.sh`, paket+locale+YAML, serta tema `WhiteSur`/`dconf`/`labkita-runtime.service` tanpa bentrok `.disk/info`+`groupadd labkita`—ketiganya lulus sehingga pemicu langsung `"Ada yang salah"` tetap menjadi keterbatasan terbuka), penjelasan kernel `-31` vs `-43`, dan spot-check angka: [`docs/CONTROL-EXPERIMENT.md`](docs/CONTROL-EXPERIMENT.md).*

*Dokumentasi lengkap hasil pengujian, kegagalan nyata, dan tangkapan layar VM asli tersedia di [`docs/evidence/`](docs/evidence/) (termasuk [`docs/evidence/benchmarks/`](docs/evidence/benchmarks/) dan [`docs/evidence/control/`](docs/evidence/control/)) serta [`docs/TEST-PLAN.md`](docs/TEST-PLAN.md).*

---

## 4. Panduan Menjalankan ISO di Mesin Virtual

### A. Rekomendasi Spesifikasi VM (VMware / VirtualBox)
- **Tipe Sistem:** Linux → Ubuntu (64-bit)
- **CPU:** Minimal 2 vCPU
- **RAM:** Minimal 4096 MB (4 GB)
- **Penyimpanan:** Minimal 25 GB
- **Display:** Resolusi disarankan minimal 1280×800 (akselerasi 3D opsional)

### B. Menjalankan Live Session
1. Buat VM baru dan pasang file `labkita-linux-0.3-amd64.iso` pada drive CD/DVD virtual.
2. Nyalakan mesin virtual. Pada bootloader GRUB, pilih **"Coba atau Pasang LabKita Linux 0.3 (Bahasa Indonesia)"**.
3. Sistem akan memuat desktop LabKita dengan bahasa Indonesia, dock terpusat, dan perkakas praktikum siap pakai.
4. Buka terminal (`Ctrl + Alt + T`) lalu jalankan verifikasi:
   ```bash
   labkita-check
   ```
5. Buka editor Geany dari dock untuk mulai mengerjakan program C atau Python.

### C. Prosedur Instalasi Resmi (`subiquity.cmd.tui`) & Akun Praktikan
Karena installer GUI normal (`ubuntu-desktop-bootstrap`) pada ISO 0.3 masih terhenti di dialog *"Ada yang salah"* (keterbatasan terbuka; pemicu langsung belum terisolasi dalam 3 build bisect), prosedur instalasi resmi ke disk adalah jalur TUI:
```bash
sudo /snap/ubuntu-desktop-bootstrap/current/bin/subiquity/subiquity/cmd/tui.py
```
Setelah instalasi selesai dan reboot ke sistem terinstal, siapkan akun mahasiswa dengan:
```bash
sudo labkita-postinstall praktikan
```
Skrip akan membuat user `praktikan`, mengunci hak sudo, mengatur izin folder privat `0700`, dan mengisi direktori `~/Praktikum` dengan modul latihan serta menyinkronkan panduan offline.

---

## 5. Anggota Tim & Pembagian Tugas

| No | Nama | NPM | Peran | Tugas & Kontribusi |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Dafa Zahran** | **257006111188** | Ketua Kelompok & Integrasi Build | Koordinasi proyek, pipeline mastering ISO via Cubic, manajemen repositori GitHub, integrasi rilis v0.3, dan orkestrasi pengujian VM. |
| 2 | **Rafly Fauzi Pratama** | **257006111152** | Pengembang Inti & Toolchain | Pembuatan skrip kustomisasi Cubic (`customize.sh`), perbaikan lokalisasi Bahasa Indonesia (`id_ID.UTF-8`), konfigurasi compiler GCC/G++, Python, Geany IDE, serta pengembangan suite `labkita-check`. |
| 3 | **Muhammad Ilham Rizky** | **257006111154** | Sistem, Keamanan & QA | Implementasi unit systemd tmpfs (`labkita-runtime.service`), skrip isolasi non-sudo (`labkita-postinstall`), perbaikan launcher Firefox Snap, serta eksekusi benchmark empiris RAM & boot time VM. |
| 4 | **Vadien Athallah Lukman** | **257006111160** | UI/UX, Dokumentasi & Media | Integrasi tema WhiteSur GTK & ikon, tipografi Inter font, desain wallpaper orisinal gradien LabKita, penyusunan laporan akhir proyek (PDF), slide presentasi (PPTX), dan naskah demo. |

Panduan alur kerja tim, konvensi commit, dan pembagian tugas GitHub Issue tersedia di [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) dan [`docs/issues/`](docs/issues/).

---

## 6. Struktur Direktori Repositori

```text
labkita-linux/
├── config/
│   └── packages.txt             # Daftar paket esensial tambahan
├── dist/
│   ├── labkita-kit.tar.gz       # Arsip payload untuk injeksi Cubic
│   ├── labkita-linux-0.3-amd64.iso.md5      # Checksum MD5 berkas ISO 0.3
│   └── labkita-linux-0.3-amd64.iso.sha256   # Checksum SHA256 berkas ISO 0.3
├── docs/
│   ├── BUILD-CUBIC.md           # Prosedur pembuatan ISO dengan Cubic
│   ├── CONTRIBUTING.md          # Panduan kolaborasi & konvensi commit git
│   ├── CREDITS.md               # Atribusi lisensi tema, ikon, font, wallpaper
│   ├── DEMO-SCRIPT.md           # Naskah video demonstrasi
│   ├── LAPORAN-PROYEK-LABKITA.pdf # Laporan lengkap proyek akhir (PDF)
│   ├── TEST-PLAN.md             # Matriks pengujian & hasil tolok ukur empiris
│   ├── VM-BUILD.md              # Konfigurasi VM lingkungan build
│   ├── evidence/                # Tangkapan layar bukti pengujian di VM
│   ├── issues/                  # Template pembagian tugas GitHub Issue
│   └── presentation/            # Slide presentasi proyek akhir (PPTX)
├── payload/                     # Berkas kustomisasi sistem
│   ├── etc/
│   │   ├── dconf/db/local.d/    # Konfigurasi dconf (dock, tema, buttons)
│   │   ├── default/             # Konfigurasi default locale & keyboard
│   │   └── systemd/system/      # Unit layanan labkita-runtime.service
│   └── usr/
│       ├── local/bin/           # Skrip `labkita-check` & `labkita-guide`
│       ├── local/sbin/          # Skrip pembuatan user `labkita-postinstall`
│       └── share/labkita/       # Panduan HTML offline dan contoh kode
├── scripts/
│   └── customize.sh             # Skrip kustomisasi utama di chroot
├── tools/
│   ├── generate_report_pdf.py   # Generator laporan proyek PDF
│   ├── generate_slides.py       # Generator slide presentasi PPTX
│   ├── pack.py                  # Skrip pembuat arsip kit
│   ├── test_runner.py           # Otomasi pengujian VM via VNC
│   └── vmctl.py                 # Utilitas kontrol VMware
└── README.md
```

---

## 7. Lisensi

- Kustomisasi dan skrip konfigurasi LabKita dirilis di bawah [MIT License](LICENSE).
- Komponen tema visual WhiteSur, ikon, dan kursor tunduk pada lisensi aslinya masing-masing (GPL-3.0 / CC-BY-SA-4.0).
- Komponen upstream Ubuntu, kernel Linux, GCC, Python, Geany, dan pustaka pendukung tetap tunduk pada lisensi aslinya masing-masing (GPL, LGPL, PSF, dll.). Atribusi lengkap tercantum pada [`docs/CREDITS.md`](docs/CREDITS.md).
