# LabKita Linux

Distribusi sistem operasi berbasis Ubuntu 24.04 LTS (Noble Numbat) yang dikustomisasi khusus untuk kebutuhan **praktikum pemrograman dasar dan sistem operasi secara luring (*offline*)** di laboratorium komputer kampus tanpa ketergantungan koneksi internet.

Proyek ini dikembangkan sebagai luaran **Final Project Mata Kuliah Sistem Operasi**, Semester Ganjil 2026/2027.  
**Dosen Pengampu:** Muhammad Sidik Asyaky, S.T., M.T.

---

## 1. Identitas Rilis, Produk/Unduhan, & Checksum ISO

| Atribut | Detail |
| --- | --- |
| **Nama Distro** | LabKita Linux |
| **Versi Rilis** | 0.4 |
| **Basis Sistem** | Ubuntu 24.04.5 LTS Desktop (amd64) |
| **Arsitektur** | x86_64 / amd64 |
| **Nama Berkas ISO** | `labkita-linux-0.4-amd64.iso` |
| **Tautan Unduhan ISO** | https://drive.google.com/drive/folders/10ZI4s-CYWAKA8GsHbTBCZm-p0QArp8lM?usp=sharing |
| **Ukuran Berkas** | 6.520.395.776 bytes (~6,07 GiB / 6,52 GB) |
| **SHA256 Checksum** | `7ae9e815a02e58ca5f700344541aadba3db47a6b5a15c942c9b0e4587f64b9d4` |
| **MD5 Checksum** | `00ea1d333ab0e52b953d7fe3806044ed` |
| **Metode Build** | Cubic (*Custom Ubuntu ISO Creator*) `2026.09.110-release~202609120048~ubuntu24.04.1` |
| **Status Verifikasi** | Teruji di VM (`md5sum` loop ISO `957/957 OK`, `Get-FileHash` Windows identik, autologin live `labkita` **berhasil** tanpa `gnome-initial-setup`, `labkita-check` `23/23` + uji baca sandbox Firefox Snap lulus, `labkita-postinstall praktikum` dengan grup `labkita-praktikum` lulus; **installer GUI normal `ubuntu-desktop-bootstrap` masih gagal dialog *"Ada yang salah"* di ISO build Cubic** sehingga prosedur instalasi resmi memakai jalur TUI `subiquity.cmd.tui` — lihat [`docs/TEST-PLAN.md`](docs/TEST-PLAN.md) & [`docs/CONTROL-EXPERIMENT.md`](docs/CONTROL-EXPERIMENT.md)) |

### Produk / Unduhan & Verifikasi Integritas Berkas
- **Unduhan ISO 0.4:** `https://drive.google.com/drive/folders/10ZI4s-CYWAKA8GsHbTBCZm-p0QArp8lM?usp=sharing` (`labkita-linux-0.4-amd64.iso`, ukuran `6.520.395.776 bytes`)
- **Prosedur Instalasi Resmi:** Karena installer GUI (`ubuntu-desktop-bootstrap`) masih gagal pada ISO hasil Cubic (*keterbatasan terbuka*), pemasangan permanen ke disk dijalankan lewat jalur TUI resmi **`subiquity.cmd.tui`** (lihat Bagian 4.C).
- Sebelum mengimpor atau membakar ISO ke media instalasi, lakukan verifikasi integritas berkas:

- **PowerShell (Windows):**
  ```powershell
  Get-FileHash -Algorithm SHA256 .\labkita-linux-0.4-amd64.iso
  # Hash: 7AE9E815A02E58CA5F700344541AADBA3DB47A6B5A15C942C9B0E4587F64B9D4
  ```

- **Linux / macOS (Bash):**
  ```bash
  sha256sum labkita-linux-0.4-amd64.iso
  # 7ae9e815a02e58ca5f700344541aadba3db47a6b5a15c942c9b0e4587f64b9d4  labkita-linux-0.4-amd64.iso
  ```

---

## 2. Latar Belakang & Fitur Utama

Laboratorium komputer kampus sering menghadapi masalah koneksi internet yang lambat atau tidak stabil saat praktikum berlangsung. LabKita Linux dirancang agar mahasiswa dan asisten lab dapat menjalankan sesi praktikum secara mandiri tanpa membutuhkan akses repository online.

### Fitur & Perbaikan pada Versi 0.4:
1. **Perbaikan Bentrok Grup Autologin (`labkita-praktikum`) & Konsistensi Branding 0.4:**
   - Investigasi bisect #1–#4 (manual di WSL) membuktikan bahwa grup sistem `labkita` (`customize.sh:107`) bertabrakan dengan penurunan `USERNAME=labkita` oleh `casper` dari `.disk/info` (`casper.log: fatal: The group 'labkita' already exists.`), sehingga **autologin sesi live gagal** dan jatuh ke `gnome-initial-setup`.
   - Pada rilis 0.4, grup sistem diubah menjadi **`labkita-praktikum`** (`scripts/customize.sh` dan `payload/usr/local/sbin/labkita-postinstall`) dan grup `labkita` lama dibersihkan saat mastering Cubic. Hasil nyata di VM: **autologin sesi live `labkita` berhasil pulih** tanpa `gnome-initial-setup`. Namun **kegagalan installer GUI tidak ikut pulih oleh fix grup ini**, sehingga penyebab kegagalan installer GUI **belum teridentifikasi** (kandidat tersisa: `.disk/info` diawali `"LabKita"` yang membuat `casper` menurunkan `USERNAME=labkita` belum diuji; prosedur resmi tetap TUI).
   - Integrasi paket bahasa lengkap (`language-pack-id`, `language-pack-gnome-id`, `hunspell-id`, `firefox-locale-id`), locale `id_ID.UTF-8`, zona waktu `Asia/Jakarta` (WIB), dan label rilis `0.4` konsisten di GRUB, `/usr/lib/os-release`, `/etc/lsb-release`, `/etc/labkita-release`, layar sambutan, `casper/install-sources.yaml`, `labkita-check`, serta `labkita-guide`.

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

4. **Isolasi Keamanan & `labkita-postinstall` (Grup `labkita-praktikum`):**
   - Utilitas `/usr/local/sbin/labkita-postinstall` memakai perbaikan **`printf --`** serta grup **`labkita-praktikum`** (tanpa sisa grup `labkita` di `scripts/` maupun `payload/`), sekaligus menyalin panduan ke `/home/<user>/Dokumen/Panduan-LabKita/`.
   - Direktori `/home/praktikan` dilindungi izin akses ketat `0700` (`drwx------`), mencegah akses tidak sah antarmahasiswa, dan akun mahasiswa tidak memiliki hak `sudo`.

5. **Workspace Temporer Cepat (RAM Disk tmpfs) & Regenerasi `md5sum.txt` ISO:**
   - Layanan systemd `labkita-runtime.service` otomatis membuat `/run/labkita` berbasis memori RAM (*tmpfs*) dengan sticky bit `1777` (`drwxrwxrwt`). *(Catatan: `/run` dipasang `noexec` oleh sistem, sehingga binary hasil kompilasi dijalankan dari `~/Praktikum`, sementara `/run/labkita` dipakai untuk berkas scratch sementara).*
   - Manifest `md5sum.txt` ISO 0.4 diregenerasi setelah seluruh berkas final terbentuk (mengecualikan `boot.catalog`, `./boot/grub/i386-pc/eltorito.img` yang di-patch `xorriso --grub2-boot-info`, dan `./casper/install-sources.yaml.original`) dan lolos verifikasi **`957/957 OK`** di ISO terpasang loop serta `casper-md5check` saat live boot. *(Catatan jujur: meskipun autologin `labkita` berhasil dan checksum lulus, installer GUI normal `ubuntu-desktop-bootstrap` pada ISO 0.4 hasil Cubic masih gagal memunculkan dialog `"Ada yang salah"` sehingga instalasi resmi tetap menggunakan **`subiquity.cmd.tui`**.)*

6. **Suite Diagnostik Mandiri dengan Tes Baca Sandbox (`labkita-check`):**
   - Memverifikasi toolchain, locale, timezone, tema WhiteSur, wallpaper, tmpfs, layanan runtime, lokasi non-dotfolder `~/Dokumen/Panduan-LabKita`, asosiasi `xdg-mime`, sekaligus **menguji pembacaan nyata file HTML melalui `snap run --shell firefox -c 'cat "$1"'`** (`AppArmor OK`).

---

## 3. Hasil Pengujian & Tolok Ukur Empiris (0.1 vs 0.2 vs 0.3 vs 0.4)

Pengujian empiris dilakukan ulang **setelah instalasi penuh ke disk kosong** pada VMware Workstation dalam **kondisi identik** (VM `labkita-test.vmx`: 2 vCPU, RAM 4096 MB / `3911 MiB` usable, Disk 40 GB SCSI, **5 kali reboot bersih per versi**, pengukuran 20 detik setelah desktop siap).  
*Catatan variabel:* `0.1` dan `0.2` berjalan pada kernel **`7.0.0-31-generic`**, sedangkan `0.3` dan `0.4` berjalan pada kernel **`7.0.0-43-generic`** (berasal dari langkah *downloading and installing security updates* saat instalasi TUI; ISO `0.1`–`0.4` tetap membawa `7.0.0-31-generic`).

| Pengujian | Perintah / Tolok Ukur | LabKita 0.1 | LabKita 0.2 | LabKita 0.3 | LabKita 0.4 (Terinstal) | Status 0.4 |
| --- | --- | :---: | :---: | :---: | :---: | :---: |
| **Integritas ISO (`md5sum.txt`)** | `md5sum -c` & `casper-md5check` | — | Gagal mismatch | 957/957 OK | **957/957 OK** *(kecuali `boot.catalog`, `eltorito.img`, `.yaml.original`)* | **LULUS** |
| **Boot Menu GRUB** | Layar GRUB 2.12 | Bahasa Inggris | Bahasa Indonesia | LabKita 0.3 (ID) | **LabKita Linux 0.4 (Bahasa Indonesia)** | **LULUS** |
| **Autologin Live Session** | Live boot tanpa wizard | Jatuh ke `gnome-initial-setup` | Jatuh ke `gnome-initial-setup` | Jatuh ke `gnome-initial-setup` | **Langsung ke desktop `labkita` (`USERNAME=labkita`, 0 error grup)** | **LULUS (Pulih)** |
| **Installer GUI** | `ubuntu-desktop-bootstrap` | Gagal | Gagal (*Ada yang salah*) | Gagal (*Ada yang salah*) | **Masih gagal (*Ada yang salah*) pada ISO build Cubic** | **GAGAL** |
| **Instalasi ke Disk** | `subiquity.cmd.tui` | Sukses hingga reboot | Sukses hingga reboot | Sukses hingga reboot | **Sukses (*LabKita Linux 0.4*) hingga reboot** | **LULUS (Resmi)** |
| **Self-Diagnostic Suite** | `labkita-check` | Lulus (cek dasar) | 21/21 (cek file) | Semua lulus + Snap OK | **23/23 `[LULUS]` + uji baca `snap run firefox` OK** | **LULUS** |
| **Konsumsi RAM (5x)** | `free -m` Used (rata-rata & rentang) | **1.038,2 MiB** *(1016–1056)* | **1.068,2 MiB** *(1058–1080)* | **1.058,2 MiB** *(1046–1067)* | **1.062,6 MiB** *(1.043–1.075 MiB)* | **TERUKUR** |
| **Waktu Booting (5x)** | `systemd-analyze time` (rata-rata & rentang) | **8,460s** *(8,359–8,676s)* | **9,317s** *(9,072–9,458s)* | **8,808s** *(8,460–9,014s)* | **9,185s** *(8,520–10,713s)* | **TERUKUR** |
| **Konsistensi Branding** | `os-release`, sambutan, Tentang | Label `0.1` | Sisa label `0.1` | Label `0.3` | **Seluruh label & sambutan tampil `0.4`** | **LULUS** |
| **Tampilan WhiteSur & ID** | Desktop, dock, `Berkas` | Default Yaru (EN) | WhiteSur + Dock (ID) | WhiteSur + Dock (ID) | **WhiteSur + Dock bawah + Bahasa Indonesia** | **LULUS** |
| **Pembuatan Akun Praktikan** | `sudo labkita-postinstall praktikan` | Lulus | Error `printf` baris 45 | Lulus (`0` error) | **Lulus (`0` error, grup sistem `labkita-praktikum`)** | **LULUS** |
| **Isolasi Akun & Izin 0700** | `id`, `stat`, `ls /home/praktikan` | `0700` / ditolak | `0700` / ditolak | `0700`, non-`sudo` | **`0700`, non-`sudo`, tidak ada grup `'labkita'`** | **LULUS** |
| **Akses Panduan Firefox Snap** | `labkita-guide` GUI Firefox Snap | Terblokir `/usr/share` | Terblokir `~/.local` | Terbuka di `~/Dokumen` | **Terbuka & terender di `~/Dokumen/Panduan-LabKita`** | **LULUS** |
| **Kompilasi & Eksekusi Offline** | `nmcli networking off`, `gcc`, `python3` | Lulus | Lulus | Lulus | **Lulus (`~/Praktikum` C, Python, `processes.py`)** | **LULUS** |
| **Ruang Kerja Tmpfs** | `/run/labkita` (`1777`) | Mode `1777` | Mode `1777` | Mode `1777` | **Mode `1777` aktif (`noexec` pada `/run`)** | **LULUS** |

> **Catatan Analisis Kinerja Empiris (Tanpa Klaim "Lebih Ringan/Cepat"):**  
> Pada 5 kali pengujian identik setelah instalasi per versi, **tidak ada perbedaan yang dapat dibuktikan antarversi (`0.1`, `0.2`, `0.3`, `0.4`), dan tidak ada klaim lebih ringan/lebih cepat untuk versi mana pun**: konsumsi RAM rata-rata `0.4` tercatat **`1.062,6 MiB`** (rentang `1.043–1.075 MiB`; tersedia rata-rata **`2.847,8 MiB`**), saling tumpang tindih dengan `0.3` **`1.058,2 MiB`** (`1.046–1.067`), `0.2` **`1.068,2 MiB`** (`1.058–1.080`), maupun `0.1` **`1.038,2 MiB`** (`1.016–1.056`). Untuk waktu boot, rata-rata `0.4` adalah **`9,185 detik`** (rentang **`8,520–10,713s`**), juga tumpang tindih dengan rentang `0.1` (`8,359–8,676s`), `0.2` (`9,072–9,458s`), dan `0.3` (`8,460–9,014s`), serta terdapat variabel pembeda kernel (`7.0.0-43-generic` pada `0.3`/`0.4` vs `7.0.0-31-generic` pada `0.1`/`0.2`).

> **Temuan Bisect Terkontrol & Keterbatasan ISO 0.4:**  
> - **Kegagalan autologin live terbukti disebabkan bentrok grup `'labkita'` dan sudah dipulihkan di 0.4:** melalui bisect terkontrol di WSL, Bisect #3 lulus penuh sedangkan Bisect #4 (= #3 + `.disk/info` `"LabKita Linux 0.3 (...)"` + `groupadd --system labkita`) gagal dengan log `casper.log: fatal: The group 'labkita' already exists.` dan jatuh ke `gnome-initial-setup`. Penggantian grup menjadi `labkita-praktikum` pada ISO `0.4` memulihkan autologin live `labkita` (`UID 1000`).
> - **Kegagalan installer GUI (`ubuntu-desktop-bootstrap`) TIDAK dipulihkan oleh fix grup & penyebabnya belum teridentifikasi:** pada ISO `0.4` hasil Cubic dengan autologin `labkita` sudah pulih, dialog *"Ada yang salah"* tetap muncul (`DEBUG desktop: Inhibiting Gnome session`).
> - **Kandidat tersisa (belum diuji):** `.disk/info` yang diawali `"LabKita"` menyebabkan `casper` menurunkan `USERNAME=labkita` (berbeda dari `USERNAME=ubuntu` pada Bisect #3 WSL), serta perbedaan lingkungan build Cubic vs WSL (`custom-live`).
> - **Prosedur instalasi resmi:** Jalur TUI **`subiquity.cmd.tui`**. (Catatan kernel: `0.1`/`0.2` memakai `7.0.0-31-generic`, sedangkan `0.3`/`0.4` memakai `7.0.0-43-generic` yang diunduh oleh langkah *security updates* saat instalasi TUI.)

*Detail lengkap eksperimen kontrol, bisect #1–#4, dan verifikasi 0.4 tersedia di [`docs/CONTROL-EXPERIMENT.md`](docs/CONTROL-EXPERIMENT.md), bukti VM di [`docs/evidence/`](docs/evidence/), serta matriks uji di [`docs/TEST-PLAN.md`](docs/TEST-PLAN.md).*

---

## 4. Panduan Menjalankan ISO di Mesin Virtual

### A. Rekomendasi Spesifikasi VM (VMware / VirtualBox)
- **Tipe Sistem:** Linux → Ubuntu (64-bit)
- **CPU:** Minimal 2 vCPU
- **RAM:** Minimal 4096 MB (4 GB)
- **Penyimpanan:** Minimal 25 GB
- **Display:** Resolusi disarankan minimal 1280×800 (akselerasi 3D opsional)

### B. Menjalankan Live Session
1. Buat VM baru dan pasang file `labkita-linux-0.4-amd64.iso` pada drive CD/DVD virtual.
2. Nyalakan mesin virtual. Pada bootloader GRUB, pilih **"Coba atau Pasang LabKita Linux 0.4 (Bahasa Indonesia)"**.
3. Sistem kini langsung melakukan **autologin ke user live `labkita`** menuju desktop LabKita (tanpa wizard `gnome-initial-setup`), dengan antarmuka bahasa Indonesia, dock terpusat, dan perkakas praktikum siap pakai.
4. Buka terminal (`Ctrl + Alt + T`) lalu jalankan verifikasi:
   ```bash
   labkita-check
   ```
5. Buka editor Geany dari dock untuk mulai mengerjakan program C atau Python.

### C. Prosedur Instalasi Resmi (`subiquity.cmd.tui`) & Akun Praktikan
Karena installer GUI normal (`ubuntu-desktop-bootstrap`) pada ISO 0.4 **tidak pulih** oleh fix grup (`labkita-praktikum`) dan **penyebabnya belum teridentifikasi** (kandidat tersisa: `.disk/info` diawali `"LabKita"` yang menurunkan `USERNAME=labkita` belum diuji), **prosedur instalasi resmi adalah jalur TUI** melalui terminal live:
```bash
sudo snap run --shell ubuntu-desktop-bootstrap.subiquity-server -c "subiquity.cmd.tui"
```
Setelah instalasi selesai dan reboot ke sistem terinstal, siapkan akun mahasiswa dengan:
```bash
sudo labkita-postinstall praktikan
```
Skrip akan membuat user `praktikan`, mengaitkannya ke grup sistem `labkita-praktikum` (bukan `sudo`), mengatur izin folder privat `0700`, mengisi direktori `~/Praktikum` dengan modul latihan, dan menyinkronkan panduan offline.

---

## 5. Anggota Tim & Pembagian Tugas

| No | Nama | NPM | Peran | Tugas & Kontribusi |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Dafa Zahran** | **257006111188** | Ketua Kelompok & Integrasi Build | Koordinasi proyek, pipeline mastering ISO via Cubic, manajemen repositori GitHub, integrasi rilis v0.4, dan orkestrasi pengujian VM. |
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
│   ├── labkita-linux-0.4-amd64.iso.md5      # Checksum MD5 berkas ISO 0.4
│   └── labkita-linux-0.4-amd64.iso.sha256   # Checksum SHA256 berkas ISO 0.4 (simpan juga arsip 0.1-0.3)
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
