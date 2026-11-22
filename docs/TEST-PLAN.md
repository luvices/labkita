# Rencana dan Hasil Pengujian LabKita Linux 0.3

Dokumen ini mencatat hasil verifikasi dan audit nyata pada **LabKita Linux 0.3** (`labkita-linux-0.3-amd64.iso`, Cubic `2026.09.110-release~202609120048~ubuntu24.04.1`) yang diuji langsung pada VMware Workstation (`labkita-test.vmx`, 2 vCPU, RAM 4 GB / `3911 MiB` usable, disk virtual 40 GB SCSI kosong). Seluruh tangkapan layar pada [`docs/evidence/`](evidence/) merupakan capture layar VM asli, termasuk pengujian yang masih gagal di 0.3.

## 1. Daftar Pengujian Fungsional & Integritas Media (0.3)

| Pengujian | Target | Hasil Nyata di VM 0.3 | Status | Bukti |
| :--- | :--- | :--- | :---: | :--- |
| **Integritas ISO `md5sum.txt`** | Regenerasi `md5sum.txt` di `custom-disk` setelah `squashfs`, kernel, `initrd`, & metadata selesai | Di ISO terpasang loop: **`957/957` berkas `OK`** (`MD5_VERIFY_EXIT=0`, mengecualikan `./boot/grub/i386-pc/eltorito.img` yang di-patch `xorriso --grub2-boot-info`). Di VM live (`subiquity-server-debug.log`): `casper-md5check results: {'checksum_missmatch': [], 'result': 'pass'}` | **LULUS** | Log installer VM & `md5sum -c` |
| **Boot Menu GRUB Bahasa Indonesia** | Menu GRUB menampilkan versi 0.3 dalam Bahasa Indonesia | Tampil `*Coba atau Pasang LabKita Linux 0.3 (Bahasa Indonesia)` di GNU GRUB 2.12 | **LULUS** | `docs/evidence/01-grub-boot-menu-v03-id.png` |
| **Autologin Live Session (`labkita`)** | Langsung masuk ke sesi live desktop tanpa wizard akun | Sesi live masih memunculkan `gnome-initial-setup` (*"Selamat Datang"*) untuk membuat pengguna sementara (tanpa `NOPASSWD:ALL` di sudoers) | **GAGAL** | *(diamati saat live boot 0.1–0.3)* |
| **Installer GUI (`ubuntu-desktop-bootstrap`)** | Instalasi ke disk kosong lewat wizard grafis normal | **Masih gagal** memunculkan dialog *"Ada yang salah"* (`Tampilkan log` berhenti di `WAITING`, meskipun `casper-md5check` sudah `pass`!) | **GAGAL** | `docs/evidence/02-v03-gui-installer-error.png`, `docs/evidence/03-v03-gui-installer-log.png` |
| **Instalasi ke Disk via `subiquity.cmd.tui`** | Instalasi penuh ke `/dev/sda` pada disk kosong 40 GB | Sumber tampil **`(X) LabKita Linux 0.3`**, partisi LVM + instalasi tuntas (*"Installation complete!"*) hingga reboot ke sistem terinstal | **LULUS (Fallback TUI)** | `docs/evidence/04-v03-subiquity-tui-complete.png` |
| **Konsistensi Branding & Metadata 0.3** | Tidak ada sisa label `0.1` atau `0.2` di metadata & dialog | `os-release` (`PRETTY_NAME="LabKita Linux 0.3 (Noble Numbat)"`), `/etc/lsb-release` (`DISTRIB_DESCRIPTION="LabKita Linux 0.3"`), `/etc/labkita-release` (`VERSION="0.3"`), layar sambutan (`Selamat datang di LabKita Linux 0.3`), dan Pengaturan `Tentang` semuanya tampil `0.3` | **LULUS** | `docs/evidence/05-v03-installed-welcome.png`, `docs/evidence/08-v03-installed-about-id.png` |
| **Desktop WhiteSur, Dock & Bahasa Indonesia** | Tema GTK/Ikon/Kursor WhiteSur, tombol kiri, dock tengah, UI Indonesia | Tema WhiteSur, tombol kiri, dock tengah bawah, wallpaper LabKita, top bar `Kam 19 Nov`, `Berkas`, & `Pengaturan` tampil Bahasa Indonesia *(catatan minor: slot ikon Terminal & Berkas di dock terlihat redup/kosong pada tampilan tidak aktif)* | **LULUS** *(catatan minor ikon dock)* | `docs/evidence/06-v03-installed-desktop-clean.png`, `docs/evidence/07-v03-installed-desktop-whitesur-id.png` |
| **Lokasi & Pembacaan Panduan di Firefox Snap** | Panduan offline lolos AppArmor Firefox Snap | `labkita-guide` menyalin panduan ke **`~/Dokumen/Panduan-LabKita`** (non-dotfolder). Firefox Snap benar-benar membuka & merender `file:///home/labkitaadmin/Dokumen/Panduan-LabKita/index.html` (`LabKita Linux 0.3`) tanpa error | **LULUS** | `docs/evidence/10-v03-installed-guide-firefox-snap.png` |
| **Uji Diagnostik `labkita-check` (Dengan Tes Baca Snap)** | Skrip benar-benar membaca berkas panduan lewat sandbox Firefox Snap | Seluruh item `[LULUS]` termasuk `Lokasi panduan non-dotfolder (~/Dokumen)`, `Asosiasi penampil HTML (xdg-mime)`, dan **`Pembacaan panduan oleh sandbox Firefox Snap (AppArmor OK)`** via `snap run --shell firefox -c 'cat "$1"'` | **LULUS** | `docs/evidence/09-v03-installed-labkita-check.png` |
| **Perbaikan `printf --` di `labkita-postinstall`** | `sudo labkita-postinstall praktikan` mencetak ringkasan tanpa error | `[SUKSES]` mencetak seluruh 4 baris ringkasan tanpa error `printf: - : pilihan tidak valid`; menyalin panduan ke `/home/praktikan/Dokumen/Panduan-LabKita` | **LULUS** | `docs/evidence/11-v03-installed-labkita-postinstall.png` |
| **Isolasi Akun Praktikan & Izin `0700`** | Non-sudo/adm, folder `0700`, panduan terbaca pemilik | `id praktikan` (`1001`, grup `praktikan,labkita`), `stat` `700 /home/praktikan`, `644 .../Panduan-LabKita/index.html`, `ls /home/praktikan` dari `labkitaadmin` ditolak (`Ijin ditolak`), `praktikan` ditolak saat mencoba `sudo` | **LULUS** | `docs/evidence/12-v03-installed-praktikan-isolation.png` |
| **Kompilasi & Eksekusi Offline + Tmpfs** | Toolchain offline jalan saat `nmcli networking off`; `/run/labkita` aktif `1777` | `STATE: mengantuk`, `CONNECTIVITY: tidak ada`; `gcc hello.c` di `~/Praktikum`, `./hello_c`, `hello.py`, & `processes.py` berjalan mulus; `labkita-runtime.service` `active` dengan `/run/labkita` mode `1777` *(catatan: `/run` bertipe `noexec` sehingga eksekusi binary biner C dilakukan di `~/Praktikum`, sedangkan `/run/labkita` dipakai untuk scratch data)* | **LULUS** | `docs/evidence/13-v03-installed-offline-c-python.png` |

## 2. Pengukuran Ulang Kinerja 0.1 vs 0.2 vs 0.3 Setelah Instalasi (5x per Versi)

Setiap versi (`0.1`, `0.2`, `0.3`) diinstal ulang bersih satu per satu ke disk virtual kosong 40 GB pada **VM yang sama** (`labkita-test.vmx`: 2 vCPU, RAM 4.096 MB / `3.911 MiB` terbaca kernel Linux), melewati wizard `gnome-initial-setup` pasca-instalasi lebih dulu, lalu dijalankan **5 kali cold boot berurutan** dengan `sudo poweroff` bersih antar run. Pembacaan `uname -r`, `free -m`, dan `systemd-analyze time` dilakukan di terminal tepat 20 detik setelah desktop selesai login.

> **Variabel Tidak Terkontrol (Perbedaan Versi Kernel):**  
> Instalasi bersih LabKita `0.1` dan `0.2` berjalan pada kernel **`7.0.0-31-generic`**, sedangkan LabKita `0.3` (yang membawa pembaruan paket kernel saat remastering Cubic) berjalan pada kernel **`7.0.0-43-generic`**. Perbedaan waktu boot dan pemakaian memori antar versi dapat dipengaruhi oleh versi kernel dan layanan sistem bawaan, bukan semata-mata perubahan skrip LabKita.

### A. Konsumsi Memori RAM (`free -m` — Used / Available dalam MiB)

| Versi (Kernel) | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Rata-rata Used | Rentang Min–Maks Used | Rata-rata Available |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **LabKita 0.1** (`7.0.0-31-generic`) | 1052 / 2859 | 1018 / 2892 | 1056 / 2855 | 1049 / 2862 | 1016 / 2895 | **1.038,2 MiB** | **1.016–1.056 MiB** | 2.872,6 MiB *(2.855–2.895)* |
| **LabKita 0.2** (`7.0.0-31-generic`) | 1072 / 2839 | 1080 / 2830 | 1072 / 2839 | 1059 / 2851 | 1058 / 2852 | **1.068,2 MiB** | **1.058–1.080 MiB** | 2.842,2 MiB *(2.830–2.852)* |
| **LabKita 0.3** (`7.0.0-43-generic`) | 1049 / 2861 | 1067 / 2844 | 1067 / 2843 | 1062 / 2848 | 1046 / 2864 | **1.058,2 MiB** | **1.046–1.067 MiB** | 2.852,0 MiB *(2.843–2.864)* |

### B. Waktu Booting Sistem (`systemd-analyze time` — Total & `graphical.target`)

| Versi (Kernel) | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Rata-rata Total (Kernel + User) | Rentang Min–Maks Total | Rata-rata `graphical.target` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **LabKita 0.1** (`7.0.0-31-generic`) | 8,359s | 8,403s | 8,676s | 8,434s | 8,426s | **8,460s** *(3,205s + 5,255s)* | **8,359s–8,676s** | **5,180s** *(5,084s–5,371s)* |
| **LabKita 0.2** (`7.0.0-31-generic`) | 9,437s | 9,401s | 9,458s | 9,218s | 9,072s | **9,317s** *(3,330s + 5,987s)* | **9,072s–9,458s** | **5,918s** *(5,786s–6,057s)* |
| **LabKita 0.3** (`7.0.0-43-generic`) | 8,840s | 8,938s | 8,788s | 8,460s | 9,014s | **8,808s** *(3,197s + 5,610s)* | **8,460s–9,014s** | **5,532s** *(5,215s–5,717s)* |

Bukti seluruh 15 screenshot pengukuran (`5x` per versi) tersedia di [`docs/evidence/benchmarks/`](evidence/benchmarks/): `v01-r1.png` s.d. `v01-r5.png`, `v02-r1.png` s.d. `v02-r5.png`, dan `v03-r1.png` s.d. `v03-r5.png`.

## 3. Analisis Jujur: Hasil Kinerja & Akar Kegagalan Installer GUI di 0.3

1. **Tidak Ada Klaim "Lebih Ringan" atau "Lebih Cepat" secara Umum:**
   - **Memori RAM:** Konsumsi RAM rata-rata `0.3` (`1.058,2 MiB`, rentang `1.046–1.067 MiB`) maupun `0.2` (`1.068,2 MiB`, rentang `1.058–1.080 MiB`) berbeda dari `0.1` (`1.038,2 MiB`, rentang `1.016–1.056 MiB`) tanpa penyebab yang terbukti; rentang `0.3` dan `0.1` saling bertumpang tindih (`1046–1056 MiB`). Rentang `0.3` dan `0.2` juga saling bertumpang tindih (`1058–1067 MiB`).
   - **Waktu Boot:** Rentang `0.3` (`8,460s–9,014s`, rata-rata `8,808s`) masih bertumpang tindih dengan `0.1` (`8,359s–8,676s`, rata-rata `8,460s`). Meskipun seluruh 5 run `0.3` (`maks 9,014s`) tercatat di bawah seluruh 5 run `0.2` (`min 9,072s`, selisih rata-rata `-0,509s`), **keduanya menggunakan versi kernel berbeda (`7.0.0-43-generic` di 0.3 vs `7.0.0-31-generic` di 0.2)** sehingga selisih tersebut tidak diklaim sebagai hasil optimasi skrip LabKita.
   - **Komponen terlama (`systemd-analyze blame`):** Layanan terlama pada ketiga versi berasal dari `plymouth-quit-wait.service` (`~2,18s–2,85s`), `snapd.seeded.service` (`~0,98s–1,22s`), `snapd.service` (`~0,82s–1,08s`), `NetworkManager.service`, dan `gpu-manager.service`.
2. **Mengapa Installer GUI Normal (`ubuntu-desktop-bootstrap`) Masih Gagal di 0.3?**
   - Kegagalan di `0.3` **bukan lagi disebabkan oleh `md5sum.txt`**: `/var/log/installer/subiquity-server-debug.log` memastikan `casper-md5check results: {'checksum_missmatch': [], 'result': 'pass'}` dan `md5sum -c md5sum.txt` di live VM mengembalikan `ALL_CDROM_MD5_OK`.
   - `subiquity-server` berhasil memindai disk `/dev/sda`, memuat `/cdrom/casper/install-sources.yaml`, dan masuk ke status `ApplicationState.WAITING` (`error: null`).
   - Namun frontend GTK/Flutter `ubuntu-desktop-bootstrap` (`rev 680`, versi `24.04.5.1`) tetap menampilkan dialog *"Ada yang salah"* (`Tampilkan log` hanya memperlihatkan `subiquity_event` sampai `subiquity/Late/apply_autoinstall_config`). Dari `ubuntu_bootstrap.log`, `journalctl -b`, dan stderr langsung di VM tercatat:
     - `ubuntu_bootstrap.log` berhenti setelah `state: null => WAITING` dan `DEBUG desktop: Inhibiting Gnome session`.
     - `journalctl -b` dan stderr mencatat `im-ibus.so: undefined symbol: ibus_input_context_set_post_process_key_event`, `libEGL warning: DRI3 error: Could not get DRI3 device`, `atk-bridge: get_device_events_reply: unknown signature`, serta saat penutupan `fl_view_set_textures` (catatan: warning `DRI3` dan `im-ibus.so` juga muncul di ISO Ubuntu asli yang **sukses**, sehingga bukan penyebab kegagalan).
     - Pada saat yang sama, bentrok `.disk/info` (`LabKita Linux 0.3`) + `groupadd --system labkita` di `scripts/customize.sh` menggagalkan pembuatan user autologin `casper` (`uid 1000`), sehingga sesi live jatuh ke `gnome-initial-setup` (user dibuat manual tanpa `NOPASSWD:ALL`).
     - Akibatnya, instalasi ke disk resmi menggunakan jalur TUI **`subiquity.cmd.tui`**.

## 4. Eksperimen Kontrol Installer GUI, Perbandingan ISO, & Bisect 3 Build

Ringkasan (detail & bukti lengkap di [`CONTROL-EXPERIMENT.md`](CONTROL-EXPERIMENT.md)):

- **Kontrol Ubuntu 24.04.5.1 asli (VMX identik): installer GUI selesai.** LabKita 0.3: **gagal** baik dengan 3D acceleration mati **maupun** hidup, sehingga 3D acceleration bukan penyebab.
- **Perbandingan ISO Ubuntu asli vs LabKita 0.3:** `/etc/gdm3/custom.conf`, `/etc/casper.conf`, `/etc/sudoers.d/casper`, `casper/initrd` (`SHA256` identik), 13 snap seed, dan `minimal.standard.live.manifest` (`115` paket) **identik**. Perbedaan nyata ada pada tabrakan `.disk/info` (`"LabKita Linux 0.3"`) + `groupadd --system labkita`, `casper/install-sources.yaml` (2 entri `langpack` vs 1 entri `locale_support: none`), `minimal.manifest` (`+280` paket), `grub.cfg` (`locale=id_ID.UTF-8`), serta lapisan live (`etc/dconf/*`, symlink `etc/default/locale -> ../locale.conf`, `snapd/state.json`).
- **Bisect bertahap (maksimal 3 build, 3D mati):**
  - Build #1 (repack `minimal.standard.live.squashfs` tanpa `customize.sh`): **LULUS** (`10-bisect1-repack-nocustomize.png`).
  - Build #2 (+ `config/packages.txt`, locale `id_ID.UTF-8`, `grub.cfg`, 1-entri `install-sources.yaml`): **LULUS** (`11-bisect2-pkgs-locale-yaml.png`).
  - Build #3 (+ `payload/` tema/ikon `WhiteSur`, wallpaper, `dconf`, `labkita-runtime.service`, `os-release`/`lsb-release`, tanpa `.disk/info` `"LabKita..."` & `groupadd labkita`): **LULUS** (`12-bisect3-theme-dconf-systemd-pass.png`).
  - **Keterbatasan terbuka:** Dalam batas 3 build, pemicu langsung dialog *"Ada yang salah"* belum terpicu ulang (kandidat tersisa: bentrok `.disk/info` + `groupadd labkita` ke `gnome-initial-setup`, atau delta lapisan live Cubic). ISO 0.3 tetap tidak diubah; instalasi resmi memakai **`subiquity.cmd.tui`**.
- Kernel 0.2 `-31` (19 Nov) vs `-43` (16 Nov): ISO selalu berisi `-31`; `-43` kemungkinan berasal dari langkah update online installer yang berjalan pada 16 Nov tetapi tidak tampak pada 19 Nov (alasannya tidak terbukti).
- Spot-check 9 screenshot benchmark: tidak ada selisih angka terhadap tabel.
- Kesimpulan benchmark: **tidak ada perbedaan yang dapat dibuktikan** antara 0.3 dan 0.1/0.2.
