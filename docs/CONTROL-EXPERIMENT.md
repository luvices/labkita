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

**Perbedaan yang teramati antara Ubuntu asli dan LabKita (korelasi, belum terbukti sebagai penyebab):**
1. Ubuntu asli: autologin `ubuntu` (uid 1000). LabKita: sesi live jatuh ke `gnome-initial-setup`, user dibuat manual (uid 1001), tanpa `NOPASSWD:ALL`.
2. `install-sources.yaml`: 2 sumber (Ubuntu) vs 1 sumber ditulis ulang (LabKita).

**Penyebab sebenarnya belum ditemukan.** Kami tidak menguji (dan tidak mengklaim) perbaikan untuk dua perbedaan di atas.

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
