# LabKita Linux

Distribusi sistem operasi berbasis Ubuntu 24.04 LTS (Noble Numbat) yang dikustomisasi khusus untuk kebutuhan **praktikum pemrograman dasar dan sistem operasi secara luring (*offline*)** di laboratorium komputer kampus tanpa ketergantungan koneksi internet.

Proyek ini dikembangkan sebagai luaran **Final Project Mata Kuliah Sistem Operasi**, Semester Ganjil 2026/2027.  
**Dosen Pengampu:** Muhammad Sidik Asyaky, S.T., M.T.

---

## 1. Identitas Rilis, Produk/Unduhan, & Checksum ISO

| Atribut | Detail |
| --- | --- |
| **Nama Distro** | LabKita Linux |
| **Versi Rilis** | **0.5 (Final — versi akhir resmi)** |
| **Basis Sistem** | Ubuntu 24.04.5 LTS Desktop (amd64) |
| **Arsitektur** | x86_64 / amd64 |
| **Nama Berkas ISO** | `labkita-linux-0.5-amd64.iso` |
| **Tautan Unduhan ISO** | `https://drive.google.com/drive/folders/10ZI4s-CYWAKA8GsHbTBCZm-p0QArp8lM?usp=sharing` |
| **Ukuran Berkas** | 6.643.179.520 bytes (~6,19 GiB / 6,64 GB) |
| **SHA256 Checksum** | `d0dae277d140decd3e1ecaff9b908c551109a10efd069b1472acd34b046f5f1c` |
| **MD5 Checksum** | `b73178250b61cdfd900e3a3f8bdca660` |
| **Metode & Tag Build** | Build WSL [`tools/build_v05.py`](tools/build_v05.py) (resep Bisect #3, non-Cubic) dari tag **`v0.5-iso`** |
| **Status Verifikasi** | **LULUS PENUH** di VM uji (`md5sum` loop ISO **`1016/1016 OK`**, `Get-FileHash` Windows identik, autologin live `ubuntu` langsung desktop, **installer GUI normal `ubuntu-desktop-bootstrap` selesai hingga `"Instalasi selesai"`**, `labkita-check` seluruh pemeriksaan lulus termasuk sandbox Firefox Snap AppArmor OK, `labkita-postinstall praktikan` grup `labkita-praktikum` `0700` non-`sudo`, `labkita-guide` Firefox Snap OK — lihat [`docs/TEST-PLAN.md`](docs/TEST-PLAN.md) & [`docs/CONTROL-EXPERIMENT.md`](docs/CONTROL-EXPERIMENT.md)) |

### Produk / Unduhan & Verifikasi Integritas Berkas
- **Unduhan ISO Final 0.5 (Satu-Satunya Rilis Resmi):** `https://drive.google.com/drive/folders/10ZI4s-CYWAKA8GsHbTBCZm-p0QArp8lM?usp=sharing` (`labkita-linux-0.5-amd64.iso`, ukuran `6.643.179.520 bytes`, dibangun dari tag **`v0.5-iso`**). Versi **0.5** merupakan versi final proyek dan satu-satunya rilis yang diunduh; rilis `0.1`–`0.4` hanya dicatat sebagai arsip dan riwayat pengujian.
- **Prosedur Instalasi Resmi:** **Installer GUI (`ubuntu-desktop-bootstrap`)** pada ISO `0.5` (lihat Bagian 4.C). Jalur TUI **`subiquity.cmd.tui`** tetap tersedia sebagai **prosedur cadangan** (serta catatan prosedur kerja pada arsip pengujian `0.1`–`0.4` build Cubic).
- Sebelum mengimpor atau membakar ISO ke media instalasi, lakukan verifikasi integritas berkas:

- **PowerShell (Windows):**
  ```powershell
  Get-FileHash -Algorithm SHA256 .\labkita-linux-0.5-amd64.iso
  # Hash: D0DAE277D140DECD3E1ECAFF9B908C551109A10EFD069B1472ACD34B046F5F1C
  ```

- **Linux / macOS (Bash):**
  ```bash
  sha256sum labkita-linux-0.5-amd64.iso
  # d0dae277d140decd3e1ecaff9b908c551109a10efd069b1472acd34b046f5f1c  labkita-linux-0.5-amd64.iso
  ```

---

## 2. Latar Belakang & Fitur Utama

Laboratorium komputer kampus sering menghadapi masalah koneksi internet yang lambat atau tidak stabil saat praktikum berlangsung. LabKita Linux dirancang agar mahasiswa dan asisten lab dapat menjalankan sesi praktikum secara mandiri tanpa membutuhkan akses repository online.

### Fitur & Perbaikan pada Versi 0.5 (Dibangun dari Tag `v0.5-iso`):
1. **Pemulihan Penuh Installer GUI (`ubuntu-desktop-bootstrap`) & Build WSL Reproducible ([`tools/build_v05.py`](tools/build_v05.py)):**
   - Pada arsip ISO `0.1`–`0.4` hasil build Cubic, installer GUI normal (`ubuntu-desktop-bootstrap`) gagal dengan dialog *"Ada yang salah"* tepat setelah `Inhibiting Gnome session`, sedangkan build WSL resep Bisect #3 lulus penuh (hipotesis awal: perbedaan state snapd/lapisan Cubic, belum diuji ulang di Cubic karena `0.5` memakai pipeline WSL).
   - Melalui percobaan `0.5` #1 vs #2 serta audit `strace` & kode `canonical/ubuntu-desktop-provision` (`ProductService._extractIsoInfo`), teridentifikasi bahwa `isoName.substring(0, isoName.indexOf('"') - 1)` melempar `RangeError` (bukan `Exception`) ketika `/cdrom/.disk/info` tidak memiliki tanda kutip `"`. Dengan format `.disk/info` = `Ubuntu 24.04 LabKita 0.5 "Noble Numbat" - Release amd64 (20261122)` (kata pertama `Ubuntu` menjaga autologin `ubuntu` tanpa bentrok `labkita-praktikum`), `/var/log/installer/telemetry` tertulis normal dan **installer GUI berjalan penuh hingga *"Instalasi selesai"* **.
   - Normalisasi *line ending* **CRLF→LF** di `.gitattributes` & `tools/build_v05.py` mencegah kegagalan shebang `/usr/bin/env: 'python3\r'` / `'bash\r'` ketika disalin dari checkout Windows.
   - Integrasi paket bahasa lengkap (`language-pack-id`, `language-pack-gnome-id`, `hunspell-id`, `firefox-locale-id`), locale `id_ID.UTF-8`, zona waktu `Asia/Jakarta` (WIB), dan label rilis `0.5` konsisten di GRUB, `/usr/lib/os-release`, `/etc/lsb-release`, `/etc/labkita-release`, layar sambutan, `casper/install-sources.yaml`, `labkita-check`, serta `labkita-guide`.

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
   - **Contoh Program Praktikum (`/usr/share/labkita/examples/`):** Menyertakan contoh kode siap pakai: `hello.c`, `hello.py`, `processes.py`, serta contoh pengayaan `thread_demo.py` (multithreading Python) dan `memory_demo.c` (alokasi memori dinamis C).
     > **📌 Catatan Pembaruan Pasca-Rilis:** Pembaruan materi panduan praktikum serta contoh kode `thread_demo.py` dan `memory_demo.c` merupakan pembaruan repositori setelah rilis final dan **belum termasuk di dalam berkas ISO 0.5** (ISO dibangun dari tag **`v0.5-iso`**). Untuk mencobanya di dalam VM LabKita 0.5, salin berkas tersebut secara manual ke direktori `~/Praktikum/` atau unduh langsung dari repositori ini.

4. **Isolasi Keamanan & `labkita-postinstall` (Grup `labkita-praktikum`):**
   - Utilitas `/usr/local/sbin/labkita-postinstall` memakai perbaikan **`printf --`** serta grup **`labkita-praktikum`** (tanpa sisa grup `labkita` di `scripts/` maupun `payload/`), sekaligus menyalin panduan ke `/home/<user>/Dokumen/Panduan-LabKita/`.
   - Direktori `/home/praktikan` dilindungi izin akses ketat `0700` (`drwx------`), mencegah akses tidak sah antarmahasiswa, dan akun mahasiswa tidak memiliki hak `sudo`.

5. **Workspace Temporer Cepat (RAM Disk tmpfs) & Regenerasi `md5sum.txt` ISO:**
   - Layanan systemd `labkita-runtime.service` otomatis membuat `/run/labkita` berbasis memori RAM (*tmpfs*) dengan sticky bit `1777` (`drwxrwxrwt`). *(Catatan: `/run` dipasang `noexec` oleh sistem, sehingga binary hasil kompilasi dijalankan dari `~/Praktikum`, sementara `/run/labkita` dipakai untuk berkas scratch sementara).*
   - Manifest `md5sum.txt` ISO 0.5 diregenerasi setelah seluruh berkas final terbentuk (mengecualikan `boot.catalog` dan `./boot/grub/i386-pc/eltorito.img` yang di-patch `xorriso --grub2-boot-info`) dan lolos verifikasi **`1016/1016 OK`** di ISO terpasang loop serta `casper-md5check` saat live boot.

6. **Suite Diagnostik Mandiri dengan Tes Baca Sandbox (`labkita-check`):**
   - Memverifikasi toolchain, locale, timezone, tema WhiteSur, wallpaper, tmpfs, layanan runtime, lokasi non-dotfolder `~/Dokumen/Panduan-LabKita`, asosiasi `xdg-mime`, sekaligus **menguji pembacaan nyata file HTML melalui `snap run --shell firefox -c 'cat "$1"'`** (`AppArmor OK`).

---

## 3. Hasil Pengujian & Tolok Ukur Empiris (0.1 vs 0.2 vs 0.3 vs 0.4 vs 0.5)

Pengujian empiris dilakukan ulang **setelah instalasi penuh ke disk kosong** pada VMware Workstation dalam **kondisi identik** (VM `labkita-test.vmx`: 2 vCPU, RAM 4096 MB / `3911 MiB` usable, Disk 40 GB SCSI, `mks.enable3d = "FALSE"`, **5 kali reboot bersih per versi**, pengukuran 20 detik setelah desktop siap).  
*Catatan variabel:* `0.1` dan `0.2` berjalan pada kernel **`7.0.0-31-generic`**, sedangkan `0.3`, `0.4`, dan `0.5` berjalan pada kernel **`7.0.0-43-generic`** (pada `0.3`/`0.4` dari langkah *security updates* TUI, dan pada `0.5` dari lapisan target/update saat instalasi).

| Pengujian | Perintah / Tolok Ukur | LabKita 0.1–0.3 | LabKita 0.4 (Cubic + TUI) | LabKita 0.5 (Build WSL + GUI) | Status 0.5 |
| --- | --- | :---: | :---: | :---: | :---: |
| **Integritas ISO (`md5sum.txt`)** | `md5sum -c` & `casper-md5check` | 0.2 mismatch; 0.3 `957/957 OK` | `957/957 OK` | **`1016/1016 OK`** *(kecuali `boot.catalog`, `eltorito.img`)* | **LULUS** |
| **Boot Menu GRUB** | Layar GRUB 2.12 | 0.1 EN; 0.2–0.3 ID | LabKita Linux 0.4 (ID) | **LabKita Linux 0.5 (Bahasa Indonesia)** | **LULUS** |
| **Autologin Live Session** | Live boot tanpa wizard | Jatuh ke `gnome-initial-setup` | Autologin `labkita` pulih | **Autologin `ubuntu` langsung desktop** | **LULUS** |
| **Installer GUI** | `ubuntu-desktop-bootstrap` | Gagal (*Ada yang salah*) | Gagal (*Ada yang salah*) pada build Cubic | **Selesai penuh hingga `"Instalasi selesai"`** | **LULUS (Resmi)** |
| **Installer TUI (Cadangan)** | `subiquity.cmd.tui` | Sukses hingga reboot | Sukses hingga reboot (resmi 0.4) | **Tersedia sebagai prosedur cadangan** | **CADANGAN** |
| **Self-Diagnostic Suite** | `labkita-check` | 0.1 dasar; 0.2 `21/21`; 0.3 OK | `23/23 [LULUS]` + Snap OK | **Semua `[LULUS]` + `snap run firefox` AppArmor OK** | **LULUS** |
| **Konsumsi RAM (5x)** | `free -m` Used (rata-rata & rentang) | `0.1`: **1.038,2** *(1016–1056)*<br>`0.2`: **1.068,2** *(1058–1080)*<br>`0.3`: **1.058,2** *(1046–1067)* | **1.062,6 MiB** *(1.043–1.075 MiB)* | **1.042,8 MiB** *(1.031–1.054 MiB; avail avg `2.867,6`)* | **TERUKUR** |
| **Waktu Booting (5x)** | `systemd-analyze time` (rata-rata & rentang) | `0.1`: **8,460s**<br>`0.2`: **9,317s**<br>`0.3`: **8,808s** | **9,185s** *(8,520–10,713s)* | **9,036s** *(8,349–9,515s; `gfx` avg `5,686s`)* | **TERUKUR** |
| **Konsistensi Branding** | `os-release`, sambutan, panduan | 0.1/0.2 sisa label; 0.3 OK | Label `0.4` konsisten | **Seluruh label & sambutan tampil `0.5`** | **LULUS** |
| **Tampilan WhiteSur & ID** | Desktop, dock, `Rumah`/`Berkas` | 0.1 Yaru; 0.2–0.3 WhiteSur | WhiteSur + Dock + ID | **WhiteSur + Dock bawah + Bahasa Indonesia** | **LULUS** |
| **Pembuatan Akun Praktikan** | `sudo labkita-postinstall praktikan` | 0.2 error `printf`; 0.1/0.3 OK | `0` error (`labkita-praktikum`) | **`[SUKSES]`, grup `labkita-praktikum`, non-`sudo`, `0700`** | **LULUS** |
| **Akses Panduan Firefox Snap** | `labkita-guide` GUI Firefox Snap | 0.1/0.2 terblokir; 0.3 OK | Terbuka di `~/Dokumen` | **Terbuka di `~/Dokumen/Panduan-LabKita` (badge `0.5`)** | **LULUS** |
| **Kompilasi & Tmpfs** | GCC/Python + `/run/labkita` (`1777`) | Lulus | Lulus | **Lulus (`labkita-check` C/Python/fork & tmpfs `1777`)** | **LULUS** |

> **Catatan Analisis Kinerja Empiris (Tanpa Klaim "Lebih Ringan/Cepat"):**  
> Pada 5 kali pengujian identik setelah instalasi per versi, **tidak ada perbedaan yang dapat dibuktikan antarversi (`0.1`, `0.2`, `0.3`, `0.4`, `0.5`), dan tidak ada klaim lebih ringan/lebih cepat untuk versi mana pun**: konsumsi RAM rata-rata `0.5` tercatat **`1.042,8 MiB`** (rentang `1.031–1.054 MiB`; tersedia rata-rata **`2.867,6 MiB`**), saling tumpang tindih dengan `0.1` **`1.038,2 MiB`** (`1.016–1.056`), `0.3` **`1.058,2 MiB`** (`1.046–1.067`), maupun `0.4` **`1.062,6 MiB`** (`1.043–1.075`). Untuk waktu boot, rata-rata `0.5` adalah **`9,036 detik`** (rentang **`8,349–9,515s`**; kernel `3,287s` + userspace `5,749s`), juga tumpang tindih dengan rentang `0.1` (`8,359–8,676s`), `0.2` (`9,072–9,458s`), `0.3` (`8,460–9,014s`), dan `0.4` (`8,520–10,713s`), serta terdapat variabel kernel (`7.0.0-43-generic` pada `0.3`/`0.4`/`0.5` vs `7.0.0-31-generic` pada `0.1`/`0.2`).

> **Ringkasan Perbandingan Build WSL (`0.5`) vs Build Cubic (`0.1`–`0.4`):**  
> - **Installer GUI berfungsi penuh pada build WSL `0.5` (`tools/build_v05.py`, resep Bisect #3) dan gagal pada build Cubic `0.1`–`0.4`:** Selain perbedaan pipeline Cubic vs WSL (belum diisolasi ulang di Cubic), pengujian `0.5` #1 vs #2 serta kode `ProductService._extractIsoInfo()` membuktikan bahwa `.disk/info` tanpa tanda kutip `"` melempar `RangeError` tak tertangkap di `ubuntu-desktop-bootstrap`. Di `0.5` final, `.disk/info` menggunakan tanda kutip codename dan diawali `"Ubuntu"` sehingga autologin live `ubuntu` maupun instalasi GUI berjalan penuh hingga selesai.  
> - **Prosedur instalasi resmi LabKita Linux 0.5 (Final):** **Installer GUI normal (`ubuntu-desktop-bootstrap`)**, sedangkan jalur TUI **`subiquity.cmd.tui`** dijadikan **prosedur cadangan** (sebagaimana catatan riwayat pengujian arsip `0.1`–`0.4`).

*Detail lengkap eksperimen kontrol, bisect #1–#4, uji `username=ubuntu`, dan verifikasi `0.5` tersedia di [`docs/CONTROL-EXPERIMENT.md`](docs/CONTROL-EXPERIMENT.md), bukti VM di [`docs/evidence/`](docs/evidence/), serta matriks uji di [`docs/TEST-PLAN.md`](docs/TEST-PLAN.md).*

---

## 4. Panduan Menjalankan ISO di Mesin Virtual

### A. Rekomendasi Spesifikasi VM (VMware / VirtualBox)
- **Tipe Sistem:** Linux → Ubuntu (64-bit)
- **CPU:** Minimal 2 vCPU
- **RAM:** Minimal 4096 MB (4 GB)
- **Penyimpanan:** Minimal 25 GB
- **Display:** Resolusi disarankan minimal 1280×800 (akselerasi 3D opsional)

### B. Menjalankan Live Session & Mulai Praktikum
1. Buat VM baru di VMware atau VirtualBox, lalu pasang berkas `labkita-linux-0.5-amd64.iso` pada drive CD/DVD virtual.
2. Nyalakan mesin virtual. Pada menu bootloader GRUB, pilih **"Coba atau Pasang LabKita Linux 0.5 (Bahasa Indonesia)"**.
3. Sistem akan otomatis **autologin sebagai user live `ubuntu`** menuju desktop LabKita dengan dock terpusat di bawah. Jendela installer GUI akan muncul otomatis; pilih opsi *"Coba Ubuntu"* jika hanya ingin menjalankan sesi live praktikum tanpa memasang ke disk.
4. Buka terminal (`Ctrl + Alt + T`), lalu siapkan folder kerja praktikum Anda:
   ```bash
   # Siapkan folder latihan dan salin seluruh modul contoh
   mkdir -p "$HOME/Praktikum"
   cp -n /usr/share/labkita/examples/* "$HOME/Praktikum/"
   cd "$HOME/Praktikum"

   # Uji coba program Python dasar
   python3 hello.py

   # Uji coba kompilasi dan eksekusi program C dasar
   gcc -Wall -Wextra hello.c -o hello && ./hello

   # Jalankan pemeriksaan mandiri kesiapan sistem
   labkita-check
   ```
5. Buka editor **Geany** dari dock untuk mulai menulis atau mengedit kode C dan Python. Untuk panduan langkah demi langkah lengkap secara offline, klik ikon **Panduan LabKita** di dock.

### C. Prosedur Instalasi Resmi (Installer GUI) & Cadangan (TUI `subiquity.cmd.tui`)
Pada rilis **0.5** (dibangun dari tag **`v0.5-iso`**), **prosedur instalasi resmi menggunakan installer GUI normal (`ubuntu-desktop-bootstrap`)** yang otomatis muncul saat sesi live: pilih bahasa (*Bahasa Indonesia*), papan ketik, opsi *Pasang Ubuntu*, *Hapus disk dan pasang Ubuntu*, buat akun admin (mis. `labadmin`), zona waktu `Asia/Jakarta`, lalu klik **Pasang** hingga *"Instalasi selesai"* dan mulai ulang.

Sebagai **prosedur cadangan** (mengikuti metode yang sebelumnya dipakai pada riwayat pengujian arsip `0.1`–`0.4`), gunakan installer TUI melalui terminal live:
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
| 1 | **Dafa Zahran** | **257006111188** | Ketua Kelompok & Integrasi Build | Koordinasi proyek, build WSL (`tools/build_v05.py` untuk `0.5`; Cubic untuk arsip `0.1`–`0.4`), regenerasi manifest md5sum & mastering ISO `labkita-linux-0.5-amd64.iso` (`v0.5-iso`), manajemen repositori GitHub, dan orkestrasi pengujian VM. |
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
│   ├── labkita-kit.tar.gz       # Arsip payload kustomisasi
│   ├── labkita-linux-0.5-amd64.iso.md5      # Checksum MD5 ISO final 0.5
│   ├── labkita-linux-0.5-amd64.iso.sha256   # Checksum SHA256 ISO final 0.5
│   └── labkita-linux-0.1..0.4-amd64.iso.*   # Checksum arsip riwayat pengujian 0.1–0.4
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
│   ├── build_v05.py             # Skrip build ISO 0.5 di WSL (resep bisect #3)
│   ├── generate_report_pdf.py   # Generator laporan proyek PDF
│   ├── generate_slides.py       # Generator slide presentasi PPTX
│   ├── pack.py                  # Skrip pembuat arsip kit
│   ├── test_runner.py           # Otomasi pengujian VM via VNC
│   ├── verify_outputs.py        # Verifikasi PDF & PPTX
│   └── vmctl.py                 # Utilitas kontrol VMware
└── README.md
```

---

## 7. Lisensi

- Kustomisasi dan skrip konfigurasi LabKita dirilis di bawah [MIT License](LICENSE).
- Komponen tema visual WhiteSur, ikon, dan kursor tunduk pada lisensi aslinya masing-masing (GPL-3.0 / CC-BY-SA-4.0).
- Komponen upstream Ubuntu, kernel Linux, GCC, Python, Geany, dan pustaka pendukung tetap tunduk pada lisensi aslinya masing-masing (GPL, LGPL, PSF, dll.). Atribusi lengkap tercantum pada [`docs/CREDITS.md`](docs/CREDITS.md).
