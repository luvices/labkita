# Rencana dan Hasil Pengujian LabKita Linux 0.5

Dokumen ini mencatat hasil verifikasi dan audit nyata pada **LabKita Linux 0.5** (`labkita-linux-0.5-amd64.iso`, dibangun di WSL lewat [`tools/build_v05.py`](../tools/build_v05.py) dari tag `v0.5-iso`) beserta riwayat perbandingan `0.1`, `0.2`, `0.3`, dan `0.4` (build Cubic) yang diuji langsung pada VMware Workstation (`labkita-test.vmx`, 2 vCPU, RAM 4 GB / `3911 MiB` usable, disk virtual 40 GB SCSI kosong, `mks.enable3d = "FALSE"`). Seluruh tangkapan layar pada [`docs/evidence/`](evidence/) merupakan capture layar VM asli.

## 1. Daftar Pengujian Fungsional & Integritas Media (0.5 vs 0.4)

| Pengujian | Target | Hasil Nyata di VM 0.5 (Build WSL) | Status 0.5 | Bukti |
| :--- | :--- | :--- | :---: | :--- |
| **Integritas ISO `md5sum.txt` & Hash Host** | Regenerasi `md5sum.txt` final dan kecocokan SHA256/MD5 di Windows | Di ISO terpasang loop: **`1016/1016` berkas `OK`** (`MD5_EXIT=0`, mengecualikan `boot.catalog` dan `./boot/grub/i386-pc/eltorito.img` yang di-patch `xorriso --grub2-boot-info`). SHA256 Windows `Get-FileHash`: `d0dae277d140decd3e1ecaff9b908c551109a10efd069b1472acd34b046f5f1c` | **LULUS** | `dist/labkita-linux-0.5-amd64.iso.sha256` |
| **GRUB & Autologin Live Session (`ubuntu`)** | Boot GRUB 0.5 & langsung masuk desktop live tanpa `gnome-initial-setup` | Menu GRUB tampil `Coba atau Pasang LabKita Linux 0.5 (Bahasa Indonesia)`. `.disk/info` diawali `"Ubuntu"` & grup `labkita-praktikum` → `casper` membuat user `ubuntu` (`uid=1000`), autologin langsung desktop tanpa `gnome-initial-setup` | **LULUS** | `docs/evidence/0.5-01-grub-menu.png`, `0.5-08` |
| **Installer GUI Resmi (`ubuntu-desktop-bootstrap`)** | Instalasi ke disk kosong 40 GB lewat wizard grafis normal | Berjalan lancar melalui seluruh tahap Bahasa Indonesia (Pemilihan bahasa, Aksesibilitas, Papan ketik, Offline, Hapus disk, Identitas `labadmin`, Zona waktu `Asia/Jakarta`, Ringkasan) hingga **"Instalasi selesai — Ubuntu 24.04 LabKita 0.5 telah terpasang dan siap digunakan"** *(kontras dengan build Cubic `0.1`–`0.4` yang gagal dialog "Ada yang salah")* | **LULUS (Prosedur Resmi)** | `docs/evidence/0.5-02` s.d. `0.5-07-gui-install-complete.png` |
| **Installer TUI (`subiquity.cmd.tui`)** | Prosedur cadangan apabila instalasi grafis tidak dipakai | Tetap tersedia pada snap `ubuntu-desktop-bootstrap` (digunakan sebagai prosedur utama pada arsip `0.1`–`0.4`) | **CADANGAN** | `docs/evidence/0.4-03` s.d. `0.4-05` |
| **Konsistensi Branding & Metadata 0.5** | Seluruh metadata & sambutan tampil `0.5` | `/etc/os-release` (`PRETTY_NAME="LabKita Linux 0.5 (Noble Numbat)"`), `/etc/labkita-release` (`0.5`), layar sambutan (`Selamat datang di LabKita Linux 0.5 (Noble Numbat)!`), & panduan badge `LabKita Linux 0.5` konsisten | **LULUS** | `docs/evidence/0.5-10`, `v05-r1.png` |
| **Desktop WhiteSur, Dock & Bahasa Indonesia** | Tema GTK/Ikon/Kursor WhiteSur, tombol kiri, dock tengah, UI Indonesia | Tema WhiteSur, tombol kiri, dock tengah bawah, wallpaper LabKita, top bar `Sen 23 Nov`, `Rumah`, & UI berbahasa Indonesia | **LULUS** | `docs/evidence/0.5-11-desktop-whitesur-dock.png` |
| **Uji Diagnostik `labkita-check`** | Toolchain, lokalisasi, tema, tmpfs, layanan, & baca Firefox Snap | Seluruh pemeriksaan **`[LULUS]`** (`SEMUA PEMERIKSAAN LULUS`), termasuk `~/Dokumen/Panduan-LabKita`, Python/C/fork, tmpfs `/run/labkita` `1777`, `labkita-runtime.service` aktif, & `Pembacaan panduan oleh sandbox Firefox Snap (AppArmor OK)` | **LULUS** | `docs/evidence/0.5-12-os-release-and-labkita-check.png` |
| **Panduan Lokal di Firefox Snap (`labkita-guide`)** | Panduan offline dibuka langsung di Firefox Snap | Firefox Snap membuka & merender `file:///home/labadmin/Dokumen/Panduan-LabKita/index.html` dengan badge **`LabKita Linux 0.5`** tanpa blokir AppArmor | **LULUS** | `docs/evidence/0.5-14-labkita-guide-firefox.png` |
| **`labkita-postinstall praktikan` & Isolasi `0700`** | Akun praktikan non-sudo, grup `labkita-praktikum`, izin `0700`, tanpa grup `labkita` | `sudo labkita-postinstall praktikan` `[SUKSES]`, `id praktikan` = `uid=1001(praktikan) gid=1001(praktikan) groups=1001(praktikan),986(labkita-praktikum)` (tanpa `sudo`, tidak ada grup `labkita`), `/home/praktikan` mode `700` | **LULUS** | `docs/evidence/0.5-13-postinstall-praktikan.png` |

*(Catatan jujur pra-perbaikan di FASE 3: build ke-2 `0.5` sempat mengalami error `/usr/bin/env: 'python3\r'` / `'bash\r'` pada `labkita-check`, `labkita-postinstall`, dan `labkita-guide` akibat checkout Windows Git berakhiran CRLF. Masalah diselesaikan melalui `.gitattributes` + normalisasi LF di `tools/build_v05.py` pada build final `d0dae277...`, yang kemudian lulus seluruh FASE 1–4 di atas.)*

## 2. Pengukuran Kinerja 0.1 vs 0.2 vs 0.3 vs 0.4 vs 0.5 Setelah Instalasi (5x per Versi)

Setiap versi (`0.1`–`0.5`) diinstal ulang bersih satu per satu ke disk virtual kosong 40 GB pada **VM yang sama** (`labkita-test.vmx`: 2 vCPU, RAM 4.096 MB / `3.911 MiB` terbaca kernel Linux), lalu dijalankan **5 kali cold boot bersih per versi** dengan pembacaan `uname -r`, `free -m`, dan `systemd-analyze time` di terminal 20 detik setelah desktop selesai login.

> **Variabel Tidak Terkontrol (Perbedaan Versi Kernel):**  
> Instalasi bersih LabKita `0.1` dan `0.2` berjalan pada kernel **`7.0.0-31-generic`**, sedangkan `0.3`, `0.4`, dan `0.5` terinstal berjalan pada kernel **`7.0.0-43-generic`**.

### A. Konsumsi Memori RAM (`free -m` — Used / Available dalam MiB)

| Versi (Kernel) | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Rata-rata Used | Rentang Min–Maks Used | Rata-rata Available |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **LabKita 0.1** (`7.0.0-31-generic`) | 1052 / 2859 | 1018 / 2892 | 1056 / 2855 | 1049 / 2862 | 1016 / 2895 | **1.038,2 MiB** | **1.016–1.056 MiB** | 2.872,6 MiB *(2.855–2.895)* |
| **LabKita 0.2** (`7.0.0-31-generic`) | 1072 / 2839 | 1080 / 2830 | 1072 / 2839 | 1059 / 2851 | 1058 / 2852 | **1.068,2 MiB** | **1.058–1.080 MiB** | 2.842,2 MiB *(2.830–2.852)* |
| **LabKita 0.3** (`7.0.0-43-generic`) | 1049 / 2861 | 1067 / 2844 | 1067 / 2843 | 1062 / 2848 | 1046 / 2864 | **1.058,2 MiB** | **1.046–1.067 MiB** | 2.852,0 MiB *(2.843–2.864)* |
| **LabKita 0.4** (`7.0.0-43-generic`) | 1043 / 2868 | 1051 / 2860 | 1075 / 2835 | 1071 / 2839 | 1073 / 2837 | **1.062,6 MiB** | **1.043–1.075 MiB** | 2.847,8 MiB *(2.835–2.868)* |
| **LabKita 0.5** (`7.0.0-43-generic`) | 1041 / 2870 | 1039 / 2871 | 1049 / 2861 | 1054 / 2857 | 1031 / 2879 | **1.042,8 MiB** | **1.031–1.054 MiB** | 2.867,6 MiB *(2.857–2.879)* |

### B. Waktu Booting Sistem (`systemd-analyze time` — Total & `graphical.target`)

| Versi (Kernel) | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Rata-rata Total (Kernel + User) | Rentang Min–Maks Total | Rata-rata `graphical.target` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **LabKita 0.1** (`7.0.0-31-generic`) | 8,359s | 8,403s | 8,676s | 8,434s | 8,426s | **8,460s** *(3,205s + 5,255s)* | **8,359s–8,676s** | **5,180s** *(5,084s–5,371s)* |
| **LabKita 0.2** (`7.0.0-31-generic`) | 9,437s | 9,401s | 9,458s | 9,218s | 9,072s | **9,317s** *(3,330s + 5,987s)* | **9,072s–9,458s** | **5,918s** *(5,786s–6,057s)* |
| **LabKita 0.3** (`7.0.0-43-generic`) | 8,840s | 8,938s | 8,788s | 8,460s | 9,014s | **8,808s** *(3,197s + 5,610s)* | **8,460s–9,014s** | **5,532s** *(5,215s–5,717s)* |
| **LabKita 0.4** (`7.0.0-43-generic`) | 10,713s | 8,520s | 8,726s | 8,967s | 9,000s | **9,185s** *(3,363s + 5,822s)* | **8,520s–10,713s** | **5,779s** *(5,202s–6,823s)* |
| **LabKita 0.5** (`7.0.0-43-generic`) | 9,515s | 9,444s | 9,370s | 8,349s | 8,502s | **9,036s** *(3,287s + 5,749s)* | **8,349s–9,515s** | **5,686s** *(5,132s–6,100s)* |

Bukti seluruh 25 screenshot pengukuran (`5x` per versi) tersedia di [`docs/evidence/benchmarks/`](evidence/benchmarks/): `v01-r1.png` s.d. `v05-r5.png`.

## 3. Analisis Jujur: Hasil Kinerja, Build WSL (`0.5`) vs Cubic (`0.1`–`0.4`)

1. **Tidak Ada Klaim "Lebih Ringan" atau "Lebih Cepat":**
   - **Memori RAM:** Rentang `0.5` (`1.031–1.054 MiB`, rata-rata `1.042,8 MiB`) saling tumpang tindih dengan `0.1` (`1.016–1.056 MiB`), `0.3` (`1.046–1.067 MiB`), dan `0.4` (`1.043–1.075 MiB`).
   - **Waktu Boot:** Rentang `0.5` (`8,349s–9,515s`, rata-rata `9,036s`) bertumpang tindih dengan seluruh versi `0.1`–`0.4`, ditambah variabel kernel (`7.0.0-43-generic` vs `7.0.0-31-generic`). Kesimpulan: **tidak ada perbedaan yang dapat dibuktikan** antarversi.
   - **Komponen terlama (`systemd-analyze blame` 0.5):** Didominasi oleh `plymouth-quit-wait.service` (`2,098s–2,874s`), `snapd.seeded.service` (`1,062s–1,238s`), `snapd.service` (`0,912s–1,191s`), `NetworkManager.service`, `gpu-manager.service`, dan `apport.service`.
2. **Installer GUI Berhasil di Build WSL `0.5` vs Gagal di Build Cubic `0.1`–`0.4`:**
   - Installer GUI `ubuntu-desktop-bootstrap` **berfungsi penuh pada build WSL `0.5`** (`tools/build_v05.py`, resep Bisect #3 + `.disk/info` berkutip `"Noble Numbat"`), sedangkan **gagal pada seluruh build Cubic `0.1`–`0.4`**.
   - Penelusuran `strace` & kode `canonical/ubuntu-desktop-provision` (`ProductService._extractIsoInfo`) menemukan bahwa `.disk/info` tanpa tanda kutip `"` melempar `RangeError` (bukan `Exception`) sehingga `ubuntu-desktop-bootstrap` langsung jatuh ke layar error *"Ada yang salah"* tanpa menulis `/var/log/installer/telemetry`. Di `0.5`, `.disk/info` memakai format `Ubuntu 24.04 LabKita 0.5 "Noble Numbat" - Release amd64 (20261122)` yang kompatibel dengan `casper` maupun `ProductService`. Faktor tambahan di lapisan build Cubic tidak diisolasi ulang di Cubic karena rilis `0.5` memakai pipeline WSL.
   - **Prosedur instalasi resmi 0.5 kini adalah jalur GUI (`ubuntu-desktop-bootstrap`)**, dan jalur TUI **`subiquity.cmd.tui`** menjadi **prosedur cadangan** (dan prosedur utama untuk arsip `0.1`–`0.4`).

## 4. Eksperimen Kontrol, Kernel, & Spot-check

Ringkasan (detail & bukti lengkap di [`CONTROL-EXPERIMENT.md`](CONTROL-EXPERIMENT.md)):

- **Kontrol Ubuntu 24.04.5.1 asli (VMX identik, 3D off): installer GUI selesai.** LabKita 0.3 gagal pada 3D mati & hidup (3D bukan penyebab). Warning `DRI3` dan `im-ibus.so` juga muncul di Ubuntu asli yang sukses.
- **Bisect #1–#4 (WSL) & Perbaikan di 0.4 (`labkita-praktikum`) → 0.5 (WSL):**
  - Bisect #4 membuktikan bentrok grup `labkita` menyebabkan **gagal autologin live** (dipulihkan di `0.4` via `labkita-praktikum`).
  - Uji `username=ubuntu` pada `0.4` menunjukkan penggantian username saja via GRUB belum memulihkan GUI pada ISO Cubic `0.4`.
  - Build **LabKita 0.5** di WSL (`tools/build_v05.py`, dari tag `v0.5-iso`) dengan `.disk/info` diawali `"Ubuntu"` dan menyertakan codename berkutip `"Noble Numbat"` berhasil memulihkan installer GUI sepenuhnya sampai selesai ke disk kosong (`0.5-02` s.d. `0.5-07`).
- **Kernel terinstal:** `0.1`/`0.2` berjalan pada `7.0.0-31-generic`, sedangkan `0.3`, `0.4`, dan `0.5` berjalan pada `7.0.0-43-generic`.
- Pembacaan langsung seluruh screenshot `v04-r1..r5.png` dan `v05-r1..r5.png` (serta spot-check 9 screenshot `0.1`–`0.3`): tidak ada selisih angka terhadap tabel.
- Kesimpulan benchmark: **tidak ada perbedaan yang dapat dibuktikan** antara `0.1`, `0.2`, `0.3`, `0.4`, dan `0.5`.
## 5. Investigasi Tampilan Ikon Terminal & Berkas di Dock (Hipotesis Teknis)

Pada catatan pengujian antarmuka, ditemukan bahwa ikon **Terminal** (`org.gnome.Terminal`) dan **Berkas** (`org.gnome.Nautilus`) tampak kosong atau tidak muncul saat aplikasi dalam keadaan tidak aktif pada dock (hanya muncul saat aplikasi aktif/berjalan).

### A. Perintah Investigasi dan Bukti Nyata Berkas

Investigasi berkas ikon dilakukan langsung pada direktori tema WhiteSur di dalam payload repositori menggunakan PowerShell di lingkungan pengembang lokal:

```powershell
# 1. Memeriksa ukuran berkas SVG ikon Terminal
Get-Item payload/usr/share/icons/WhiteSur/apps/scalable/org.gnome.Terminal.svg | Select-Object Name, Length
# Output:
# Name                   Length
# ----                   ------
# org.gnome.Terminal.svg     12

# 2. Membaca isi teks berkas ikon Terminal
Get-Content payload/usr/share/icons/WhiteSur/apps/scalable/org.gnome.Terminal.svg
# Output:
# terminal.svg

# 3. Memeriksa ukuran berkas SVG ikon Nautilus (Berkas)
Get-Item payload/usr/share/icons/WhiteSur/apps/scalable/org.gnome.Nautilus.svg | Select-Object Name, Length
# Output:
# Name                   Length
# ----                   ------
# org.gnome.Nautilus.svg     16

# 4. Membaca isi teks berkas ikon Nautilus (Berkas)
Get-Content payload/usr/share/icons/WhiteSur/apps/scalable/org.gnome.Nautilus.svg
# Output:
# file-manager.svg
```

### B. Hipotesis Teknis Penyebab Masalah

Berdasarkan pemeriksaan isi berkas di atas, dirumuskan hipotesis teknis berikut:

1. **Berkas Symlink Berubah Menjadi Plain Text:** Berkas `org.gnome.Terminal.svg` (12 byte) dan `org.gnome.Nautilus.svg` (16 byte) bukan merupakan berkas XML/SVG grafis yang valid, melainkan teks biasa yang berisi nama berkas target (`terminal.svg` dan `file-manager.svg`). Hal ini mengindikasikan bahwa symlink Unix tertulis sebagai file teks biasa saat diekstraksi atau diarsip di lingkungan sistem berkas tertentu tanpa flag symlink yang sesuai.
2. **Kegagalan Parser Grafis GNOME (librsvg):** Ketika dock GNOME Shell memuat ikon aplikasi yang sedang tidak aktif melalui desktop file (`org.gnome.Terminal.desktop` dan `org.gnome.Nautilus.desktop`), pustaka `librsvg` atau `GdkPixbuf` mencoba mem-parsing berkas teks 12/16 byte tersebut sebagai berkas grafis XML SVG. Karena formatnya bukan XML valid, parser gagal merender ikon sehingga dock menampilkan kotak kosong atau ikon fallback yang tidak tampak.
3. **Mengapa Ikon Muncul Saat Aplikasi Berjalan:** Saat jendela aplikasi aktif, GNOME Shell dapat mengambil ikon runtime dari properti jendela X11/Wayland (`_NET_WM_ICON` atau icon cache memori proses), sehingga ikon dapat tampil saat aplikasi dibuka.

> **Catatan Integritas Pengujian (PENTING):**  
> Temuan di atas berstatus **HIPOTESIS TEKNIS** yang didasarkan pada audit berkas lokal. Hipotesis ini **belum diuji coba dan belum divalidasi langsung di dalam mesin virtual (VM) / live ISO LabKita**. Sesuai aturan keras proyek, konfigurasi tema ikon di `payload/` **tidak diubah** sebelum verifikasi nyata dapat dijalankan di lingkungan VM.

---

## Verifikasi Rilis 0.6 (Autoinstall, Dual Akun, Brand Logo, & Panduan 7 Modul)

Pembaruan cabang `feat/v06-autoinstall-brand` (`tools/build_v06.py`) memverifikasi langsung perbaikan atas temuan ikon WhiteSur, penghapusan Wizard installer yang panjang, penerapan logo LabKita di Plymouth & GDM, serta buku kerja HTML 7 modul.

### A. Integritas Berkas & Lint
- **Berkas ISO Final:** `labkita-linux-0.6-amd64.iso` berukuran `6.083.645.440 bytes` (~5,67 GiB).
- **SHA256:** `6a9a055b2833e3ef64e4633db81c061992a73ba4ae91f599c45b9943fdfcd115`
- **MD5:** `0dd73d162837435295dda31b0e901652`
- **Verifikasi Loop-Mount ISO (`md5sum.txt`):** `MD5SUM_ALL_OK` (mengecualikan `boot.catalog` & `eltorito.img`).
- **Validasi Skrip Lokal (`bash tools/verify-linux.sh`):** **LULUS** (sintaks Bash, contoh Python/proses, unit systemd, penolakan host).

### B. Hasil Pengujian Nyata di VMware Workstation (Rilis 0.6)
Lingkungan uji: VMware Workstation, disk virtual kosong 40 GB, RAM 6144 MB (`5921 MiB` terbaca kernel Linux `7.0.0-44-generic`), 2 vCPU, adaptor NAT aktif.

| Skenario Uji (0.6) | Hasil Aktual di VM 0.6 | Status | Bukti |
| :--- | :--- | :---: | :--- |
| **GRUB & Zero-Touch Autoinstall (`nocloud`)** | Menu GRUB default (`Pasang Otomatis LabKita Linux 0.6`) menyelesaikan instalasi ke disk tanpa input manual dalam ~4 menit, tanpa dialog akun/bug OpenGL | **LULUS** | `docs/evidence/0.6-01-grub-autoinstall.png`, `0.6-02` |
| **Splash Plymouth & Layar Login GDM** | Splash boot Plymouth dan layar login GDM menampilkan logo LabKita; daftar akun langsung memuat **LabKita Admin** & **praktikan** | **LULUS** | `docs/evidence/0.6-03-plymouth-logo.png`, `0.6-04` |
| **Desktop Admin & Kelengkapan Ikon WhiteSur** | Login `labkita` langsung masuk desktop tanpa GNOME Initial Setup/popup upgrade; Settings & App Grid menampilkan seluruh ikon utuh tanpa ikon kosong | **LULUS** | `docs/evidence/0.6-05`, `0.6-06`, `0.6-07` |
| **Diagnostik `labkita-check` (Rebuild Final)** | Seluruh 25 baris pemeriksaan menghasilkan **SEMUA PEMERIKSAAN LULUS**, termasuk `Logo Login GDM LabKita` dan baca Firefox Snap (`AppArmor OK`) | **LULUS** | `docs/evidence/0.6-11-labkita-check-pass.png` |
| **Panduan Kerja 7 Modul & Firefox Snap + Selenium Edge** | Terbuka di Firefox Snap via `labkita-guide`; audit Edge/Selenium memastikan `no_overflow=True` di `1280x800` & `390x844` CDP, `0` error konsol, tombol `Salin` & `localStorage` aktif, kontras >= `4.79:1` | **LULUS** | `docs/evidence/0.6-08-guide-workbook-firefox.png` |
| **Isolasi & Toolchain Akun `praktikan`** | `stat /home/praktikan` = `700`, `uid=1001` grup `labkita-praktikum`, `sudo -n true` ditolak, kompilasi `gcc ~/Praktikum/hello.c` & `python3 ~/Praktikum/thread_demo.py` sukses offline | **LULUS** | `docs/evidence/0.6-09`, `0.6-10` |

### C. Observasi Sumber Daya 0.6 & Catatan VMware Workstation
- **Observasi Pasca-Install (VM 6 GB RAM):** `free -m` mencatat `1.076 MiB` used (`4.844 MiB` available), `systemd-analyze` tercatat `22,207s` (`3,610s` kernel + `18,597s` userspace), dan pemakaian disk root `/` sebesar `11 GB / 40 GB`. Karena diukur 1x pada alokasi VM 6 GB RAM (berbeda dari pengujian benchmark 5x cold boot pada VM 4 GB RAM untuk `0.1`-`0.5`), angka `0.6` dicatat sebagai observasi terpisah dan tidak diklaim lebih ringan/cepat dibanding rilis sebelumnya.
- **Catatan Deploy VMware Workstation GUI:** Gunakan opsi **"I will install the operating system later"** saat membuat VM baru agar *Easy Install* VMware tidak menimpa seed `nocloud`. Setelah instalasi selesai dan reboot ke HDD, nonaktifkan *Connect at power on* pada CD/DVD dan aktifkan **Accelerate 3D graphics** pada Display (atau pilih *Ubuntu on Xorg* di layar GDM) untuk menghindari layar hitam sesi Wayland VMware.
