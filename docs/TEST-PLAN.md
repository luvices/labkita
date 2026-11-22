# Rencana dan Hasil Pengujian LabKita Linux 0.4

Dokumen ini mencatat hasil verifikasi dan audit nyata pada **LabKita Linux 0.4** (`labkita-linux-0.4-amd64.iso`, Cubic `2026.09.110-release~202609120048~ubuntu24.04.1`) beserta riwayat perbandingan `0.1`, `0.2`, dan `0.3` yang diuji langsung pada VMware Workstation (`labkita-test.vmx`, 2 vCPU, RAM 4 GB / `3911 MiB` usable, disk virtual 40 GB SCSI kosong). Seluruh tangkapan layar pada [`docs/evidence/`](evidence/) merupakan capture layar VM asli, termasuk pengujian yang masih gagal di 0.4.

## 1. Daftar Pengujian Fungsional & Integritas Media (0.4)

| Pengujian | Target | Hasil Nyata di VM 0.4 | Status | Bukti |
| :--- | :--- | :--- | :---: | :--- |
| **Integritas ISO `md5sum.txt` & Hash Host** | Regenerasi `md5sum.txt` di `custom-disk` dan kecocokan SHA256/MD5 di Windows | Di ISO terpasang loop: **`957/957` berkas `OK`** (`MD5_VERIFY_EXIT=0`, mengecualikan `boot.catalog`, `./boot/grub/i386-pc/eltorito.img` yang di-patch `xorriso --grub2-boot-info`, dan `./casper/install-sources.yaml.original`). SHA256 Linux & `Get-FileHash` Windows identik (`7ae9e815a02e58ca5f700344541aadba3db47a6b5a15c942c9b0e4587f64b9d4`). Di VM live: `casper-md5check` seluruh berkas `OK` | **LULUS** | `dist/labkita-linux-0.4-amd64.iso.sha256` |
| **Autologin Live Session (`labkita`)** | Langsung masuk ke desktop live tanpa wizard `gnome-initial-setup` | Setelah grup sistem diubah menjadi `labkita-praktikum`, `casper.log` bersih dari `"The group 'labkita' already exists."` dan autologin `labkita` (`uid=1000`) langsung masuk desktop WhiteSur | **LULUS** | `docs/evidence/0.4-01-live-autologin-desktop.png` |
| **Installer GUI (`ubuntu-desktop-bootstrap`)** | Instalasi ke disk kosong lewat wizard grafis normal | **Masih gagal** memunculkan dialog *"Ada yang salah"* (`ubuntu_bootstrap.log` berhenti setelah `Inhibiting Gnome session`), meskipun autologin `labkita` sudah berhasil dan `casper-md5check` `pass` | **GAGAL** | `docs/evidence/0.4-02-gui-installer-error.png` |
| **Instalasi Resmi ke Disk via `subiquity.cmd.tui`** | Instalasi penuh ke `/dev/sda` pada disk kosong 40 GB | Sumber tampil **`(X) LabKita Linux 0.4`**, partisi LVM + instalasi tuntas (*"Installation complete!"*) hingga reboot ke sistem terinstal | **LULUS (Prosedur Resmi)** | `docs/evidence/0.4-03-tui-source-labkita04.png`, `0.4-04`, `0.4-05` |
| **Konsistensi Branding & Metadata 0.4** | Tidak ada sisa label `0.1`–`0.3` di metadata & dialog | `/etc/os-release` (`PRETTY_NAME="LabKita Linux 0.4 (Noble Numbat)"`), `/etc/labkita-release` (`VERSION="0.4"`), layar sambutan (`Selamat datang di LabKita Linux 0.4`), & deskripsi rilis konsisten `0.4` | **LULUS** | `docs/evidence/0.4-06-installed-welcome-0.4.png`, `0.4-08-os-release-and-labkita-check.png` |
| **Desktop WhiteSur, Dock & Bahasa Indonesia** | Tema GTK/Ikon/Kursor WhiteSur, tombol kiri, dock tengah, UI Indonesia | Tema WhiteSur, tombol kiri, dock tengah bawah, wallpaper LabKita, top bar `Sen 23 Nov`, `Rumah`, & menu berbahasa Indonesia | **LULUS** | `docs/evidence/0.4-07-installed-desktop-dock.png` |
| **Uji Diagnostik `labkita-check` (Dengan Tes Baca Snap)** | Seluruh toolchain, tmpfs, layanan, & pembacaan panduan Firefox Snap | **23/23 `[LULUS]`**, termasuk `Lokasi panduan non-dotfolder (~/Dokumen)` (`~/Dokumen/Panduan-LabKita/index.html`) dan **`Pembacaan panduan oleh sandbox Firefox Snap (AppArmor OK)`** | **LULUS** | `docs/evidence/0.4-08-os-release-and-labkita-check.png` |
| **Lokasi & Pembacaan Panduan di Firefox Snap** | Panduan offline dibuka langsung lewat `labkita-guide` di Firefox Snap | Firefox Snap merender `file:///home/labkitavm/Dokumen/Panduan-LabKita/index.html` dengan badge **`LabKita Linux 0.4`** tanpa blokir AppArmor | **LULUS** | `docs/evidence/0.4-10-firefox-snap-guide.png` |
| **Fix Grup `labkita-praktikum` & `labkita-postinstall`** | Akun praktikan non-sudo, izin `0700`, bebas grup `labkita` & error `printf` | `sudo labkita-postinstall praktikan` `[SUKSES]` (0 error `printf`), `getent group labkita` kosong, `labkita-praktikum:x:986:praktikan`, `id praktikan` (`uid=1001`, tanpa `sudo`), `/home/praktikan` mode `700` | **LULUS** | `docs/evidence/0.4-09-postinstall-praktikan-check.png` |

## 2. Pengukuran Kinerja 0.1 vs 0.2 vs 0.3 vs 0.4 Setelah Instalasi (5x per Versi)

Setiap versi (`0.1`, `0.2`, `0.3`, `0.4`) diinstal ulang bersih satu per satu ke disk virtual kosong 40 GB pada **VM yang sama** (`labkita-test.vmx`: 2 vCPU, RAM 4.096 MB / `3.911 MiB` terbaca kernel Linux), lalu dijalankan **5 kali cold boot bersih per versi** dengan pembacaan `uname -r`, `free -m`, dan `systemd-analyze time` di terminal tepat 20 detik setelah desktop selesai login.

> **Variabel Tidak Terkontrol (Perbedaan Versi Kernel):**  
> Instalasi bersih LabKita `0.1` dan `0.2` berjalan pada kernel **`7.0.0-31-generic`**, sedangkan `0.3` dan `0.4` terinstal berjalan pada kernel **`7.0.0-43-generic`** (karena tahap *downloading and installing security updates* berjalan saat instalasi; ISO `0.1`–`0.4` tetap membawa `7.0.0-31-generic`).

### A. Konsumsi Memori RAM (`free -m` — Used / Available dalam MiB)

| Versi (Kernel) | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Rata-rata Used | Rentang Min–Maks Used | Rata-rata Available |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **LabKita 0.1** (`7.0.0-31-generic`) | 1052 / 2859 | 1018 / 2892 | 1056 / 2855 | 1049 / 2862 | 1016 / 2895 | **1.038,2 MiB** | **1.016–1.056 MiB** | 2.872,6 MiB *(2.855–2.895)* |
| **LabKita 0.2** (`7.0.0-31-generic`) | 1072 / 2839 | 1080 / 2830 | 1072 / 2839 | 1059 / 2851 | 1058 / 2852 | **1.068,2 MiB** | **1.058–1.080 MiB** | 2.842,2 MiB *(2.830–2.852)* |
| **LabKita 0.3** (`7.0.0-43-generic`) | 1049 / 2861 | 1067 / 2844 | 1067 / 2843 | 1062 / 2848 | 1046 / 2864 | **1.058,2 MiB** | **1.046–1.067 MiB** | 2.852,0 MiB *(2.843–2.864)* |
| **LabKita 0.4** (`7.0.0-43-generic`) | 1043 / 2868 | 1051 / 2860 | 1075 / 2835 | 1071 / 2839 | 1073 / 2837 | **1.062,6 MiB** | **1.043–1.075 MiB** | 2.847,8 MiB *(2.835–2.868)* |

### B. Waktu Booting Sistem (`systemd-analyze time` — Total & `graphical.target`)

| Versi (Kernel) | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Rata-rata Total (Kernel + User) | Rentang Min–Maks Total | Rata-rata `graphical.target` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **LabKita 0.1** (`7.0.0-31-generic`) | 8,359s | 8,403s | 8,676s | 8,434s | 8,426s | **8,460s** *(3,205s + 5,255s)* | **8,359s–8,676s** | **5,180s** *(5,084s–5,371s)* |
| **LabKita 0.2** (`7.0.0-31-generic`) | 9,437s | 9,401s | 9,458s | 9,218s | 9,072s | **9,317s** *(3,330s + 5,987s)* | **9,072s–9,458s** | **5,918s** *(5,786s–6,057s)* |
| **LabKita 0.3** (`7.0.0-43-generic`) | 8,840s | 8,938s | 8,788s | 8,460s | 9,014s | **8,808s** *(3,197s + 5,610s)* | **8,460s–9,014s** | **5,532s** *(5,215s–5,717s)* |
| **LabKita 0.4** (`7.0.0-43-generic`) | 10,713s | 8,520s | 8,726s | 8,967s | 9,000s | **9,185s** *(3,363s + 5,822s)* | **8,520s–10,713s** | **5,779s** *(5,202s–6,823s)* |

Bukti seluruh 20 screenshot pengukuran (`5x` per versi) tersedia di [`docs/evidence/benchmarks/`](evidence/benchmarks/): `v01-r1.png` s.d. `v04-r5.png`.

## 3. Analisis Jujur: Hasil Kinerja, Bisect #1–#4, & Uji ISO 0.4

1. **Tidak Ada Klaim "Lebih Ringan" atau "Lebih Cepat":**
   - **Memori RAM:** Rentang `0.4` (`1.043–1.075 MiB`, rata-rata `1.062,6 MiB`) saling tumpang tindih dengan `0.1` (`1.016–1.056 MiB`), `0.2` (`1.058–1.080 MiB`), dan `0.3` (`1.046–1.067 MiB`).
   - **Waktu Boot:** Rentang `0.4` (`8,520s–10,713s`, rata-rata `9,185s`) saling tumpang tindih dengan `0.2` dan `0.3` (serta mencakup `8,520s`–`8,726s`), ditambah adanya variabel perbedaan kernel (`7.0.0-43-generic` vs `7.0.0-31-generic`). Kesimpulan: **tidak ada perbedaan yang dapat dibuktikan** antarversi.
   - **Komponen terlama (`systemd-analyze blame`):** Didominasi oleh `plymouth-quit-wait.service` (`~2,18s–3,04s`), `snapd.seeded.service` (`~0,98s–1,22s`), `snapd.service` (`~0,82s–1,10s`), `NetworkManager.service`, dan `gpu-manager.service`.
2. **Temuan Bisect #1–#4 vs Hasil Nyata ISO 0.4 (Cubic):**
   - Pada bisect manual di **WSL** (bukan Cubic): **Bisect #1–#3 lulus seluruhnya** hingga layar pemilihan bahasa installer GUI (`10`–`12`), sedangkan **Bisect #4** (= Bisect #3 + `.disk/info` `"LabKita Linux 0.3"` + `groupadd --system labkita`) **terbukti gagal** dengan `casper.log: fatal: The group 'labkita' already exists.`, jatuh ke `gnome-initial-setup`, lalu `ubuntu-desktop-bootstrap` memunculkan dialog *"Ada yang salah"* (`13`–`14`).
   - **Uji perbaikan pada ISO 0.4 hasil Cubic (`labkita-praktikum`):** Penggantian grup menjadi `labkita-praktikum` dan penghapusan grup `labkita` lama **berhasil memulihkan autologin live `labkita`** tanpa `gnome-initial-setup` (`0.4-01`). Namun pada ISO 0.4 hasil build Cubic tersebut, `ubuntu-desktop-bootstrap` **masih menampilkan dialog *"Ada yang salah"*** setelah `Inhibiting Gnome session` (`0.4-02`). Karena bisect dilakukan di WSL sedangkan ISO 0.4 dibangun di Cubic (`custom-live`, `casper` menurunkan `USERNAME=labkita`), **kegagalan installer GUI pada ISO build Cubic tetap tercatat sebagai keterbatasan terbuka**, dan **jalur TUI `subiquity.cmd.tui` dipertahankan sebagai prosedur instalasi resmi**.

## 4. Eksperimen Kontrol, Kernel, & Spot-check

Ringkasan (detail & bukti lengkap di [`CONTROL-EXPERIMENT.md`](CONTROL-EXPERIMENT.md)):

- **Kontrol Ubuntu 24.04.5.1 asli (VMX identik): installer GUI selesai.** LabKita 0.3: gagal pada 3D mati & hidup (3D bukan penyebab). Warning `DRI3` dan `im-ibus.so` juga muncul di Ubuntu asli yang sukses.
- **Bisect #1–#4 (WSL) & Verifikasi ISO 0.4 (Cubic):** Tabrakan `.disk/info` + `groupadd --system labkita` terbukti menyebabkan gagal autologin live dan memicu kegagalan GUI di Bisect #4; perbaikan `labkita-praktikum` pada ISO 0.4 Cubic menyembuhkan autologin live, tetapi dialog *"Ada yang salah"* masih muncul pada build Cubic sehingga instalasi resmi memakai **`subiquity.cmd.tui`**.
- Kernel 0.2 `-31` (19 Nov) vs `-43` (16 Nov): ISO selalu berisi `-31`; `-43` berasal dari langkah update online installer (*downloading and installing security updates*, teramati pula saat instalasi TUI 0.4).
- Spot-check 9 screenshot benchmark 0.1–0.3 serta pembacaan langsung 5 screenshot benchmark 0.4: tidak ada selisih angka terhadap tabel.
- Kesimpulan benchmark: **tidak ada perbedaan yang dapat dibuktikan** antara `0.1`, `0.2`, `0.3`, dan `0.4`.
