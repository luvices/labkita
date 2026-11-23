# Eksperimen Kontrol Installer GUI & Audit Angka (LabKita 0.3)

Semua data di bawah berasal dari VM uji yang sama (`labkita-test.vmx`: 2 vCPU, RAM 4096 MB, disk kosong 40 GB, jaringan NAT) dan screenshot asli di [`docs/evidence/control/`](evidence/control/). ISO LabKita tidak diubah. Log mentah (`journalctl`, `/var/log/installer`) disimpan lokal dan **tidak di-commit** karena `journalctl` memuat artefak sesi pengujian; yang dikutip di sini hanya baris relevan.

## 1. Kontrol: ISO Ubuntu 24.04.5.1 asli (3D acceleration mati)

| Hal | Hasil |
| :-- | :-- |
| Installer GUI (`ubuntu-desktop-bootstrap`) | **Selesai** — "Ubuntu 24.04.5 LTS is installed and ready to use" (`02-ubuntu-24045-gui-install-complete.png`, ringkasan `01-...review.png`) |
| `casper-md5check` | `pass` |
| `install-sources.yaml` | 2 sumber dimuat (minimal + penuh) |
| Sesi live | `gdm-autologin` untuk user `ubuntu` (uid 1000); tidak ada sesi `gnome-initial-setup` |
| `libEGL ... DRI3 error` | 7 baris di journal (tidak menggagalkan installer) |
| `im-ibus.so: undefined symbol` | 1 baris (tidak menggagalkan installer) |

## 2. LabKita 0.3: 3D acceleration mati vs hidup

| Kombinasi (`mks.enable3d`) | Xorg `vmware(0)` | Hasil installer GUI | Bukti |
| :-- | :-- | :-- | :-- |
| `FALSE` | DRI2/DRI3 3D *disabled* | **Gagal** — dialog "Ada yang salah" | `03-labkita03-3d-off-gui-error.png` |
| `TRUE` | DRI2/DRI3 3D *enabled*, `DRI3 error` = 0 baris | **Gagal** — dialog "Ada yang salah" (sama) | `04-labkita03-3d-on-gui-error.png` |

Pada kedua kombinasi: `casper-md5check` `pass`, `install-sources.yaml` memuat 1 sumber, server `subiquity` mencapai `WAITING`, tetapi `ubuntu_bootstrap.log` berhenti setelah `Inhibiting Gnome session` (16 baris). Pada Ubuntu asli log lanjut ke pemilihan bahasa, keyboard, dst.

**Kesimpulan:** 3D acceleration **bukan** penyebab (hasil gagal identik dengan 3D mati dan hidup; Ubuntu asli sukses dengan 3D mati). Warning `DRI3` dan `im-ibus` juga muncul di Ubuntu asli yang sukses, jadi bukan penyebab.

**Perbedaan awal yang teramati antara Ubuntu asli dan LabKita 0.3 sebelum uji bisect:**
1. Ubuntu asli: autologin `ubuntu` (uid 1000). LabKita 0.3: sesi live jatuh ke `gnome-initial-setup`, user dibuat manual (uid 1001), tanpa `NOPASSWD:ALL`.
2. `install-sources.yaml`: 2 sumber (Ubuntu) vs 1 sumber ditulis ulang (LabKita).

Kandidat #1 kemudian diuji langsung melalui Bisect #4 (Bagian 7) dan perbaikan di LabKita 0.4 (Bagian 8).

## 3. Kenapa kernel 0.2 terinstal sekarang `7.0.0-31`, bukan `7.0.0-43`?

Bukti `uname -r` asli dari instalasi 0.2 yang sekarang (`05-labkita02-uname-r-7.0.0-31.png`): `7.0.0-31-generic`, `/etc/labkita-release` `VERSION="0.2"`.
Audit 16 Nov melaporkan `7.0.0-43-generic` untuk 0.2 (`09-...7.0.0-43.png`).

Yang bisa dibuktikan:
- Kernel di dalam ISO 0.1/0.2/0.3 identik (`vmlinuz` 16.992.648 byte; manifest `linux-image-7.0.0-31-generic`). ISO tidak membawa `-43`.
- Instalasi 16 Nov menjalankan langkah *"downloading and installing security updates"* (`07-...security-updates-step.png`) → paket kernel `-43` kemungkinan besar diunduh dari arsip online saat instalasi.
- Instalasi 19 Nov tidak menampilkan langkah itu (`08-...no-security-updates-step.png`); `/var/log/apt/history.log` hanya berisi pemasangan dari `file:/cdrom` (`06-...cdrom-only.png`), sehingga kernel tetap `-31`.

Kesimpulan: versi kernel di VM ditentukan oleh **apakah langkah update online installer berjalan**, bukan oleh isi ISO. **Mengapa langkah itu tidak berjalan pada 19 Nov tidak berhasil dipastikan** (tidak ada log yang menjelaskannya). Artinya variabel kernel pada benchmark tidak terkontrol, dan klaim 0.3 (`-43`) vs 0.1/0.2 (`-31`) berasal dari perbedaan kondisi jaringan/instalasi, bukan fitur LabKita.

## 4. Spot-check screenshot benchmark vs README/laporan

Dicek 9 screenshot (di atas 3 yang diminta): `v01-r1,r2,r3`, `v02-r1,r3,r5`, `v03-r1,r4,r5` (`docs/evidence/benchmarks/`).

| Screenshot | used / avail (MiB) | total boot | Tabel README/TEST-PLAN | Selisih |
| :-- | :-- | :-- | :-- | :-- |
| v01-r1 | 1052 / 2859 | 8,359 s | 1052/2859, 8,359 | tidak ada |
| v01-r2 | 1018 / 2892 | 8,403 s | sama | tidak ada |
| v01-r3 | 1056 / 2855 | 8,676 s | sama | tidak ada |
| v02-r1 | 1072 / 2839 | 9,437 s | sama | tidak ada |
| v02-r3 | 1072 / 2839 | 9,458 s | sama | tidak ada |
| v02-r5 | 1058 / 2852 | 9,072 s | sama | tidak ada |
| v03-r1 | 1049 / 2861 | 8,840 s | sama | tidak ada |
| v03-r4 | 1062 / 2848 | 8,460 s | sama | tidak ada |
| v03-r5 | 1046 / 2864 | 9,014 s | sama | tidak ada |

Tidak ada selisih angka pada 9 screenshot yang dicek (6 run lain tidak dicek ulang pada sesi ini). Catatan: screenshot 0.1 memakai desktop Yaru, 0.2/0.3 memakai WhiteSur, dan jam di v03 berbeda hari/waktu — variabel tambahan di luar kernel.

## 5. Kesimpulan benchmark yang dipakai

- 0.3 vs 0.1 dan 0.3 vs 0.2: **tidak ada perbedaan yang dapat dibuktikan** (rentang RAM tumpang tindih dengan 0.1 dan 0.2; kernel berbeda `-43` vs `-31`, dan penyebab perbedaan kernel adalah kondisi instalasi, bukan LabKita).
- 0.2 vs 0.1 (sama-sama kernel `-31`): pada 5 run, 0.2 lebih tinggi pada RAM (1058–1080 vs 1016–1056 MiB) dan boot (9,072–9,458 vs 8,359–8,676 s) tanpa tumpang tindih. Ini hanya satu VM, n=5, dan dengan desktop berbeda; **tidak diklaim sebagai sebab (mis. tema WhiteSur) dan tidak ada klaim "lebih cepat/ringan" untuk versi mana pun**.

## 6. Perbandingan ISO Ubuntu 24.04.5.1 Asli vs LabKita 0.3

Dilakukan diff isi ISO dan squashfs antara Ubuntu `24.04.5.1` asli dan `labkita-linux-0.3-amd64.iso` tanpa build baru:

| Berkas / Lapisan | Hasil Diff | Status Kandidat |
| :-- | :-- | :-- |
| `/etc/gdm3/custom.conf` | Identik (`#AutomaticLogin*` tetap dikomentari) | Bukan penyebab langsung perbedaan |
| `/etc/casper.conf` (lapisan live) | Identik (`USERNAME="ubuntu"`, `HOST="ubuntu"`, `# export FLAVOUR="Ubuntu"`) | Tidak diubah `customize.sh` |
| `/etc/sudoers.d/casper` & `casper/initrd` | Identik (`initrd` vs `initrd.gz` SHA256 `26edba6a...`) | Identik byte-for-byte |
| `/var/lib/snapd/seed/seed.yaml` (live) | 13 snap seed identik (termasuk `ubuntu-desktop-bootstrap_680`); hanya pemformatan YAML (`1182` vs `1130` B) | Minimal layer 0.3 juga memuat `thunderbird_1255.snap` |
| `minimal.standard.live.manifest` | `115` vs `115` paket (0 selisih) | Identik |
| `.disk/info` + `groupadd --system labkita` | `.disk/info` 0.3 = `"LabKita Linux 0.3 (20261117)"`; `scripts/casper` menurunkan `FLAVOUR=labkita` → `USERNAME=labkita`, lalu bertabrakan dengan grup sistem `labkita` (`customize.sh:107`) sehingga `user-setup-apply` gagal membuat UID `1000` dan GDM jatuh ke `gnome-initial-setup` | **Kandidat kuat penyebab gagal autologin & sesi non-standar installer** |
| `casper/install-sources.yaml` | Ubuntu: 2 entri (`langpack`, `preinstalled_langs`). LabKita 0.3: 1 entri (`ubuntu-desktop-minimal`, `locale_support: none`) + symlink `minimal.standard.squashfs -> minimal.squashfs` | **Kandidat perubahan konfigurasi installer** |
| `minimal.manifest` | `1490` vs `1768` paket (`+280` gabungan `minimal.standard` + `config/packages.txt`, 4 pembaruan minor `glib2.0`) | **Kandidat perubahan paket** |
| `boot/grub/grub.cfg` & lapisan live | Tambahan cmdline `locale=id_ID.UTF-8 keyboard-configuration/layoutcode=us console-setup/layoutcode=us`; lapisan live 0.3 juga memuat `etc/dconf/*`, `etc/default/keyboard`, symlink `etc/default/locale -> ../locale.conf`, serta `var/lib/snapd/state.json` berbeda (`369747` vs `235001` B) | **Kandidat perubahan boot, locale, & dconf** |

## 7. Eksperimen Bisect Bertahap (Bisect #1–#4, Dibangun Manual di WSL)

Seluruh build bisect dibangun **secara manual di WSL** (unsquashfs/chroot/mksquashfs/xorriso langsung dari ISO Ubuntu 24.04.5.1, **bukan** lewat lingkungan Cubic `custom-live`/`custom-root`), lalu diuji pada VMX identik (`labkita-test.vmx`: `mks.enable3d = "FALSE"`, disk kosong 40 GB). Perbedaan proses build Cubic belum dapat dikesampingkan hanya dari bisect WSL. ISO `labkita-linux-0.3-amd64.iso` tidak diubah.

| Build | Lapisan Kustomisasi yang Diuji | Hasil Live Boot & Installer GUI | Bukti |
| :-- | :-- | :-- | :-- |
| **Bisect #1** | Repack `minimal.standard.live.squashfs` tanpa `customize.sh` + `md5sum.txt` + `xorriso` | **LULUS** — autologin `ubuntu`, installer GUI mencapai *Choose your language:* | `10-bisect1-repack-nocustomize.png` |
| **Bisect #2** | Bisect #1 + 19 paket `config/packages.txt` + locale `id_ID.UTF-8` (`/etc/default/locale`, `Asia/Jakarta`, `grub.cfg` `locale=id_ID.UTF-8`) + 1-entri `install-sources.yaml` (`locale_support: none`) + symlink `minimal.standard.squashfs -> minimal.squashfs` | **LULUS** — autologin `ubuntu`, installer GUI mencapai *Pilih bahasa Anda: Bahasa Indonesia* | `11-bisect2-pkgs-locale-yaml.png` |
| **Bisect #3** | Bisect #2 + seluruh `payload/` (tema/ikon/kursor `WhiteSur`, wallpaper LabKita, `etc/dconf/db/local.d/20-labkita`, `dconf update`, `labkita-runtime.service`, `/etc/os-release` `PRETTY_NAME`, `/etc/lsb-release`, `/etc/skel/*`), sengaja tanpa `.disk/info` `"LabKita..."` dan tanpa `groupadd --system labkita` | **LULUS** — autologin `ubuntu` dengan wallpaper & tema LabKita aktif, installer GUI mencapai *Pilih bahasa Anda: Bahasa Indonesia* tanpa error | `12-bisect3-theme-dconf-systemd-pass.png` |
| **Bisect #4** | Persis Bisect #3 + **hanya** dua tambahan: `.disk/info` = `"LabKita Linux 0.3 (20261117)"` dan `groupadd --system labkita` (`customize.sh:107`) | **GAGAL (Bug Tereproduksi)** — sesi live gagal autologin dan jatuh ke `gnome-initial-setup`; setelah selesai wizard, `ubuntu-desktop-bootstrap` berhenti di `Inhibiting Gnome session` (`state: null => WAITING`) dan menampilkan dialog *"Ada yang salah"* | `13-bisect4-gis-autologin-failed.png`, `14-bisect4-gui-error-reproduced.png` |

### Log Bukti Reproduksi Bisect #4 (`casper.log` & `journalctl`)

Baris relevan dari `casper.log` dan `journalctl -b` VM Bisect #4 (tanpa kata sandi):
- `casper.log`:
  - `fatal: The group 'labkita' already exists.`
  - `usermod: user 'labkita' does not exist`, `passwd: user 'labkita' does not exist`, `install: invalid user 'labkita'`, `sudo: unknown user labkita`
  - `chown: invalid user: 'labkita.labkita'`
- `casper_diag.txt`: `labkita:x:986:`, `/cdrom/.disk/info` = `LabKita Linux 0.3 (20261117)`, `/etc/casper.conf` `export USERNAME="labkita"` (`# export FLAVOUR="Ubuntu"`), `/home` hanya memiliki `installer`, `labkita` (milik `root`), dan `labkitavm` (dibuat manual via `gnome-initial-setup`).
- `journalctl -b`: `gdm3: accountsservice: ActUserManager: user (null) has no username (uid: -1)` → `session opened for user gnome-initial-setup(uid=119)`.
- `ubuntu_bootstrap.log.4777`: berhenti tepat setelah `DEBUG desktop: Inhibiting Gnome session` dan `INFO subiquity_client: state: null => WAITING`.

## 8. Verifikasi Fix di ISO 0.4 Hasil Build Cubic & Keterbatasan Terbuka

Berdasarkan hasil Bisect #4, nama grup sistem pada `scripts/customize.sh` dan `payload/usr/local/sbin/labkita-postinstall` diganti dari `labkita` menjadi **`labkita-praktikum`**, grup `labkita` lama pada `custom-root` dihapus (`groupdel labkita`), dan ISO **`labkita-linux-0.4-amd64.iso`** dibangun melalui lingkungan Cubic `2026.09.110-release~202609120048~ubuntu24.04.1` (`6.520.395.776 bytes`, SHA256 `7ae9e815a02e58ca5f700344541aadba3db47a6b5a15c942c9b0e4587f64b9d4`, MD5 `00ea1d333ab0e52b953d7fe3806044ed`, verifikasi loop `957/957 OK`).

**Hasil pengujian ISO 0.4 pada VM uji yang sama (`labkita-test.vmx`, 3D off, disk kosong 40 GB):**
1. **Autologin Live Session (`labkita`):** **BERHASIL (LULUS)** — `casper.log` tidak lagi memunculkan error `"The group 'labkita' already exists."`; `casper` membuat user `labkita` (`uid=1000`, grup `labkita-praktikum:x:986`) dan desktop langsung masuk autologin LabKita 0.4 tanpa `gnome-initial-setup` (`docs/evidence/0.4-01-live-autologin-desktop.png`).
2. **Installer GUI Normal (`ubuntu-desktop-bootstrap`):** **MASIH GAGAL** — meskipun autologin `labkita` sudah berjalan, `casper-md5check` lulus, `install-sources.yaml` memuat `LabKita Linux 0.4`, dan `subiquity-server` berstatus `WAITING`, antarmuka grafis tetap memunculkan dialog *"Ada yang salah"* (`ubuntu_bootstrap.log.3211` berhenti setelah `DEBUG desktop: Inhibiting Gnome session`, `docs/evidence/0.4-02-gui-installer-error.png`).
3. **Kesimpulan Jujur & Keterbatasan Terbuka:**
   - **(a) Kegagalan autologin live** **terbukti** disebabkan bentrok `.disk/info` + `groupadd --system labkita` (`casper.log: fatal: The group 'labkita' already exists.`, Bisect #3 lulus vs Bisect #4 gagal), dan **telah dipulihkan di LabKita 0.4** lewat perubahan grup menjadi `labkita-praktikum`.
   - **(b) Kegagalan installer GUI (`ubuntu-desktop-bootstrap`) TIDAK dipulihkan oleh fix grup**; pada ISO 0.4 dengan autologin `labkita` sudah pulih, dialog *"Ada yang salah"* tetap muncul. Oleh karena itu, **penyebab kegagalan installer GUI belum teridentifikasi**.
   - **(c) Kandidat tersisa yang belum diuji:** `.disk/info` diawali `"LabKita"` membuat `casper` menurunkan `USERNAME=labkita` (berbeda dari `USERNAME=ubuntu` pada Bisect #3 WSL), serta perbedaan lingkungan build Cubic vs WSL (`custom-live`) — keduanya belum diuji isolasinya.
   - **(d) Prosedur instalasi resmi LabKita Linux 0.4:** Tetap jalur teks **`subiquity.cmd.tui`** (lulus menuntaskan partisi LVM dan instalasi penuh 0.4 ke disk, bukti `docs/evidence/0.4-03` s.d. `0.4-05`; langkah *security updates* selama instalasi TUI membawa kernel terinstal ke `7.0.0-43-generic`, konsisten dengan `0.3`, sedangkan `0.1`/`0.2` berjalan pada `7.0.0-31-generic`).

## 9. Uji parameter `username=ubuntu`

Hipotesis yang diuji **tanpa membangun ulang ISO** (`labkita-linux-0.4-amd64.iso` tidak diubah, checksum 0.4 tidak berubah): apakah mengganti user live dari `labkita` menjadi `ubuntu` melalui parameter kernel GRUB (`username=ubuntu hostname=ubuntu`) memulihkan installer GUI `ubuntu-desktop-bootstrap` pada VM uji (`labkita-test.vmx`: `mks.enable3d = "FALSE"`, disk kosong 40 GB baru).

| Aspek Uji | Hasil Nyata | Bukti |
| :--- | :--- | :--- |
| **Edit GRUB Kernel Cmdline** | Menekan `'e'` di GRUB lalu menambahkan `username=ubuntu hostname=ubuntu` pada baris `linux` dan boot via `Ctrl+X` | [`15-grub-username-ubuntu-param.png`](evidence/control/15-grub-username-ubuntu-param.png) |
| **User Autologin (`whoami`, `id`)** | **LULUS (user `ubuntu`)** — `whoami`: `ubuntu`; `id`: `uid=1000(ubuntu) gid=1000(ubuntu) groups=1000(ubuntu),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),100(users),114(lpadmin),124(sambashare)` | [`17-username-ubuntu-whoami-casper-log.png`](evidence/control/17-username-ubuntu-whoami-casper-log.png) |
| **Konfigurasi & Log `/var/log/casper.log`** | `/etc/casper.conf` tercatat `export USERNAME="ubuntu"` dan `export HOST="ubuntu"`; `/var/log/casper.log` bersih tanpa error (membaca label `'LabKita Linux 0.4 (20261122)'`, diakhiri `chown: warning: '.' should be ':': 'ubuntu.ubuntu'`) | [`17-username-ubuntu-whoami-casper-log.png`](evidence/control/17-username-ubuntu-whoami-casper-log.png) |
| **Installer GUI (`ubuntu-desktop-bootstrap`)** | **GAGAL** — tidak mencapai layar pemilihan bahasa dan kembali menampilkan dialog *"Ada yang salah"* (`casper-md5check result: pass`, 1 sumber termuat, `subiquity_server` berstatus `WAITING`, lalu `ubuntu_bootstrap.log.3258` berhenti setelah 22 baris pada `DEBUG desktop: Inhibiting Gnome session`) | [`16-username-ubuntu-gui-error.png`](evidence/control/16-username-ubuntu-gui-error.png), [`18-username-ubuntu-bootstrap-log.png`](evidence/control/18-username-ubuntu-bootstrap-log.png) |

**Kesimpulan Uji:** **GAGAL** menyembuhkan installer GUI. Meskipun `username=ubuntu hostname=ubuntu` aktif (`whoami = ubuntu`, `uid=1000`) dan `casper.log` bersih, `ubuntu-desktop-bootstrap` tetap berhenti di dialog *"Ada yang salah"* tepat setelah `DEBUG desktop: Inhibiting Gnome session`. Dengan demikian, hipotesis bahwa `.disk/info` menurunkan `USERNAME=labkita` (alih-alih `ubuntu`) gugur sebagai pemicu tunggal kegagalan installer GUI pada ISO 0.4.

## 10. LabKita Linux 0.5 (Build WSL `tools/build_v05.py` dari Tag `v0.5-iso`) — Pemulihan Penuh Installer GUI

Menggunakan resep build **WSL (`tools/build_v05.py`)** yang diturunkan dari Bisect #3 (bukan Cubic) plus grup `labkita-praktikum` dan label `0.5`, dilakukan verifikasi lengkap pada VM uji identik (`labkita-test.vmx`: 2 vCPU, RAM 4096 MB, disk kosong 40 GB baru, `mks.enable3d = "FALSE"`, tanpa parameter tambahan GRUB):

1. **Percobaan #1 (`Ubuntu 24.04 LabKita 0.5 (20261122)` tanpa tanda kutip pada `.disk/info`):**
   - Autologin live `ubuntu` (`uid=1000`) **LULUS** dan `casper.log` bersih, tetapi `ubuntu-desktop-bootstrap` masih menampilkan *"Ada yang salah"* setelah `Inhibiting Gnome session`.
   - Perbandingan `ubuntu_bootstrap.log` & `strace` terhadap kontrol Ubuntu asli menunjukkan `0.5` #1 berhenti tepat setelah `openat("/cdrom/.disk/info")` tanpa pernah menulis `/var/log/installer/telemetry` atau memanggil `GET /meta/interactive_sections`. Penelusuran sumber `canonical/ubuntu-desktop-provision` (`packages/ubuntu_provision/lib/src/services/product_service.dart` & `apps/ubuntu_bootstrap/lib/app.dart`) mengidentifikasi penyebab pasti: `ProductService._extractIsoInfo()` memanggil `isoName.substring(0, isoName.indexOf('"') - 1)`. Ketika `.disk/info` tidak memiliki tanda kutip ganda `"`, `indexOf('"')` mengembalikan `-1` sehingga `substring(0, -2)` melempar `RangeError` (di Dart merupakan `Error`, bukan `Exception`, sehingga lolos blok `on Exception {}` di `getProductInfo()` dan menggagalkan `FutureBuilder` ke `ErrorPage`). Fakta ini menjelaskan kegagalan GUI pada build Cubic `0.1`–`0.4` (yang menulis `.disk/info` tanpa kutip), uji `0.4 + username=ubuntu`, serta `0.5` percobaan #1. Faktor lingkungan Cubic lain di luar `.disk/info` belum diisolasi ulang di Cubic karena rilis `0.5` dibangun via pipeline WSL.
2. **Build Final `0.5` (`tools/build_v05.py`, `.disk/info` = `Ubuntu 24.04 LabKita 0.5 "Noble Numbat" - Release amd64 (20261122)`, normalisasi LF):**
   - Checksum: `6.643.179.520 bytes`, SHA256 `d0dae277d140decd3e1ecaff9b908c551109a10efd069b1472acd34b046f5f1c`, MD5 `b73178250b61cdfd900e3a3f8bdca660`, loop `md5sum -c md5sum.txt`: **`1016/1016 OK`**.
   - Boot live tanpa parameter tambahan: `whoami` = `ubuntu` (`uid=1000`), `casper.log` bersih, `/var/log/installer/telemetry` tertulis normal (`"Media": "Ubuntu 24.04 LabKita 0.5"`) [`0.5-08`](../evidence/0.5-08-live-whoami-casper.png).
   - **Installer GUI (`ubuntu-desktop-bootstrap`):** **LULUS PENUH** melewati pemilihan bahasa (*Bahasa Indonesia*), papan ketik, offline, penyiapan disk (*Hapus disk dan pasang Ubuntu*), akun `labadmin`, zona waktu `Asia/Jakarta`, penyalinan & pemasangan hingga dialog **"Instalasi selesai — Ubuntu 24.04 LabKita 0.5 telah terpasang dan siap digunakan"** (`docs/evidence/0.5-01` s.d. `0.5-07`). *(Catatan: build ke-2 sempat menemukan kegagalan shebang `'python3\r'`/`'bash\r'` akibat checkout Windows CRLF pada skrip `payload/`; diperbaiki lewat `.gitattributes` + normalisasi LF di `tools/build_v05.py` pada build final ini.)*
   - **Sistem Terinstal & Benchmark 5x (`7.0.0-43-generic`):** Sambutan `LabKita Linux 0.5`, `/etc/os-release` `0.5`, desktop WhiteSur + dock Bahasa Indonesia, `labkita-check` seluruh pemeriksaan **`[LULUS]`** (termasuk `AppArmor OK` Firefox Snap), `sudo labkita-postinstall praktikan` non-sudo (`labkita-praktikum`, `0700`), `labkita-guide` Firefox Snap normal (`0.5-10` s.d. `0.5-14`), serta 5x benchmark (`v05-r1..r5.png`): RAM rata-rata `1.042,8 MiB` (`1.031–1.054`), boot rata-rata `9,036s` (`8,349–9,515s`) — tidak ada perbedaan yang dapat dibuktikan antarversi `0.1`–`0.5`.

**Kesimpulan Rilis 0.5:** Installer GUI berfungsi penuh pada build WSL (`tools/build_v05.py`, tag `v0.5-iso`) dan gagal pada build Cubic `0.1`–`0.4`. **Prosedur instalasi resmi 0.5 ditetapkan ke jalur GUI (`ubuntu-desktop-bootstrap`)**, sedangkan jalur TUI `subiquity.cmd.tui` menjadi cadangan.
