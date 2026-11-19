# LabKita Linux 🐧

> **Distro Linux praktikum berbasis Ubuntu 24.04 LTS — tidak perlu internet, langsung coding.**

Dibuat sebagai **Final Project Mata Kuliah Sistem Operasi**, Semester Ganjil 2026/2027  
**Dosen Pengampu:** Muhammad Sidik Asyaky, S.T., M.T.

---

## ⚡ Mulai Cepat (Mahasiswa)

Kalau kamu cuma mau langsung praktek di LabKita, ikuti langkah ini:

```bash
# 1. Siapkan folder kerja
mkdir -p "$HOME/Praktikum"
cp -n /usr/share/labkita/examples/* "$HOME/Praktikum/"
cd "$HOME/Praktikum"

# 2. Coba jalankan Python
python3 hello.py

# 3. Compile dan jalankan C
gcc -Wall -Wextra hello.c -o hello && ./hello

# 4. Cek semua komponen siap
labkita-check
```

📖 **Panduan lengkap** tersedia offline di: klik ikon **Panduan LabKita** di dock, atau buka `~/Dokumen/Panduan-LabKita/index.html` di Firefox.

---

## 📋 Info Rilis

| Atribut | Detail |
|---|---|
| **Nama** | LabKita Linux |
| **Versi** | 0.3 |
| **Basis** | Ubuntu 24.04.5 LTS Desktop (amd64) |
| **Nama File ISO** | `labkita-linux-0.3-amd64.iso` |
| **Ukuran** | ~6.07 GiB (6.52 GB) |
| **SHA256** | `21f38dc158a010e6f80920274dd7b8cd8f3e0d7f5e91283a310e98e53f045387` |
| **MD5** | `521f315f62a6c7cd08a31d40ad8c9fb5` |

### Verifikasi file ISO sebelum dipakai

**Windows (PowerShell):**
```powershell
Get-FileHash -Algorithm SHA256 .\labkita-linux-0.3-amd64.iso
```

**Linux / macOS:**
```bash
sha256sum labkita-linux-0.3-amd64.iso
```

Pastikan hash yang muncul sama persis dengan SHA256 di tabel atas.

---

## 🖥️ Cara Menjalankan di VM (Step-by-step)

### Spesifikasi VM yang Direkomendasikan

| Komponen | Minimum |
|---|---|
| CPU | 2 core (vCPU) |
| RAM | 4 GB (4096 MB) |
| Storage | 25 GB kosong |
| Display | Aktifkan akselerasi 3D, resolusi minimal 1280×800 |

Cocok untuk **VMware Workstation** maupun **VirtualBox**.

### Langkah 1 — Buat VM baru

1. Buat VM baru, pilih tipe **Linux → Ubuntu (64-bit)**
2. Pasang file `labkita-linux-0.3-amd64.iso` sebagai CD/DVD virtual
3. Nyalakan VM

### Langkah 2 — Boot

Saat layar GRUB muncul, pilih:
> **Coba atau Pasang LabKita Linux 0.3 (Bahasa Indonesia)**

Tunggu hingga desktop muncul.

### Langkah 3 — Verifikasi sistem

Buka terminal (`Ctrl + Alt + T`) dan jalankan:
```bash
labkita-check
```

Kalau semua baris menunjukkan `[LULUS]`, sistem sudah siap dipakai.

### Langkah 4 — Mulai coding

- Buka **Geany** dari dock untuk menulis kode C atau Python
- Buka **Panduan LabKita** dari dock untuk melihat panduan langkah demi langkah
- Semua contoh kode ada di `/usr/share/labkita/examples/`

### Instalasi Permanen ke Disk (Lab Komputer)

Kalau LabKita mau dipasang permanen di PC lab (bukan live session), gunakan installer TUI:

> **Catatan:** Installer grafis (`ubuntu-desktop-bootstrap`) pada versi 0.3 masih mengalami masalah. Gunakan fallback **Subiquity TUI** yang sudah teruji bekerja.

Setelah terinstal, buat akun mahasiswa dengan perintah ini sebagai admin:
```bash
sudo labkita-postinstall praktikan
```

Perintah itu akan otomatis:
- Membuat user `praktikan`
- Mengunci hak `sudo` (mahasiswa tidak bisa ubah sistem)
- Mengatur izin folder privat (`0700`)
- Menyalin semua contoh kode dan panduan ke folder home-nya

---

## ✨ Fitur LabKita Linux 0.3

### 🌐 Bahasa Indonesia Penuh
Seluruh tampilan sistem — dari menu GRUB, desktop, hingga teks utilitas — sudah dalam Bahasa Indonesia. Locale `id_ID.UTF-8`, zona waktu Jakarta (WIB).

### 🎨 Tampilan Modern Bergaya macOS
- Tema **WhiteSur GTK** (sumber terbuka, bukan aset Apple)
- Dock terpusat di bawah, tombol jendela di sebelah kiri
- Font **Inter** yang nyaman untuk coding dan membaca
- Wallpaper gradien minimalis karya tim LabKita

> **Catatan minor (v0.3):** Ikon Terminal dan Berkas di dock tampak redup saat aplikasi belum dibuka. Ini sudah diinvestigasi — kemungkinan karena symlink ikon yang tidak terbaca benar saat dipaketkan. Belum diperbaiki karena butuh pengujian di VM terlebih dulu.

### 💻 Toolchain Coding Lengkap (Offline!)

| Kategori | Tersedia |
|---|---|
| **Bahasa C** | GCC 13.3.0, G++, Make, GDB, `build-essential` |
| **Python** | Python 3.12.3 + modul `venv` |
| **Editor** | Geany 2.0 (shortcut build sudah dikonfigurasi), Nano |
| **Version Control** | Git 2.43 |

### 📚 Contoh Program yang Disertakan
Semua ada di `~/Praktikum/` setelah setup awal:

| File | Isi |
|---|---|
| `hello.c` | Program C paling dasar |
| `hello.py` | Program Python paling dasar |
| `memory_demo.c` | Alokasi memori dinamis (`malloc` / `free`) |
| `thread_demo.py` | Multithreading dengan modul `threading` |
| `processes.py` | Multiprocessing dengan `fork` |

### 🔒 Keamanan Praktikum
- Akun mahasiswa (`praktikan`) tidak punya hak `sudo` — tidak bisa mengubah sistem
- Folder antar mahasiswa terisolasi (izin `0700`)
- Panduan otomatis disalin ke `~/Dokumen/Panduan-LabKita/` agar bisa dibuka Firefox Snap

### ⚡ RAM Disk untuk Kerja Cepat
Folder `/run/labkita` adalah RAM disk (tmpfs) yang sangat cepat untuk file sementara.
> ⚠️ Isinya hilang saat komputer dimatikan! Simpan kode di `~/Praktikum`.

---

## 📊 Hasil Pengujian (Jujur)

Pengujian dilakukan di VMware Workstation dengan spesifikasi identik, 5x cold boot per versi setelah instalasi bersih ke disk.

| Pengujian | v0.1 | v0.2 | v0.3 |
|---|:---:|:---:|:---:|
| Integritas ISO (md5sum) | — | ❌ Gagal | ✅ 957/957 OK |
| Boot GRUB Bahasa Indonesia | ❌ | ✅ | ✅ |
| Autologin live session | ❌ | ❌ | ❌ (belum) |
| Installer GUI | ❌ | ❌ | ❌ (fallback TUI ✅) |
| Instalasi ke disk | ✅ | ✅ | ✅ |
| Toolchain offline (gcc, python3) | ✅ | ✅ | ✅ |
| Panduan terbuka di Firefox Snap | ❌ | ❌ | ✅ |
| `labkita-postinstall` tanpa error | ✅ | ❌ | ✅ |

**Rata-rata RAM terpakai:** ~1.058 MiB | **Rata-rata waktu boot:** ~8.8 detik  
*(Tidak diklaim "lebih cepat/ringan" — perbedaan antar versi tidak terbukti karena versi kernel berbeda saat pengujian. Detail lengkap di [`docs/TEST-PLAN.md`](docs/TEST-PLAN.md) dan [`docs/CONTROL-EXPERIMENT.md`](docs/CONTROL-EXPERIMENT.md).)*

---

## 👥 Tim Pengembang

| Nama | NPM | Peran |
|---|:---:|---|
| **Dafa Zahran** | 257006111188 | Ketua & Build ISO (Cubic, pipeline rilis, manajemen repo) |
| **Rafly Fauzi Pratama** | 257006111152 | Core Dev & Toolchain (customize.sh, lokalisasi, labkita-check) |
| **Muhammad Ilham Rizky** | 257006111154 | Sistem & QA (tmpfs, labkita-postinstall, benchmark VM) |
| **Vadien Athallah Lukman** | 257006111160 | UI/UX & Dokumentasi (tema WhiteSur, wallpaper, panduan, laporan) |

---

## 📁 Struktur Repositori

```
labkita/
├── config/
│   └── packages.txt              # Daftar paket yang diinstal
├── dist/
│   ├── labkita-kit.tar.gz        # Payload siap injeksi ke Cubic
│   ├── *.iso.md5                 # Checksum MD5
│   └── *.iso.sha256              # Checksum SHA256
├── docs/
│   ├── CONTRIBUTING.md           # Cara kontribusi & aturan commit
│   ├── BUILD-CUBIC.md            # Cara build ISO dengan Cubic
│   ├── TEST-PLAN.md              # Hasil pengujian lengkap
│   ├── CONTROL-EXPERIMENT.md     # Eksperimen kontrol & audit angka
│   ├── CREDITS.md                # Lisensi tema, ikon, font
│   ├── DEMO-SCRIPT.md            # Naskah video demo
│   ├── evidence/                 # Screenshot bukti pengujian VM
│   ├── issues/                   # Pembagian tugas per anggota
│   └── presentation/             # Slide presentasi (PPTX)
├── payload/                      # File kustomisasi sistem
│   ├── etc/dconf/db/local.d/     # Konfigurasi dock, tema, tampilan
│   ├── etc/systemd/system/       # Service labkita-runtime (tmpfs)
│   └── usr/share/labkita/        # Panduan HTML & contoh kode
├── scripts/
│   └── customize.sh              # Skrip utama kustomisasi di chroot Cubic
└── tools/                        # Utilitas bantu tim (PDF, PPTX, pengujian)
```

---

## 📄 Lisensi

- **Kode & skrip LabKita** → [MIT License](LICENSE)
- **Tema WhiteSur** (GTK, ikon, kursor) → GPL-3.0 / CC-BY-SA-4.0 (lihat [`docs/CREDITS.md`](docs/CREDITS.md))
- **Ubuntu, GCC, Python, Geany, dll.** → Lisensi masing-masing (GPL, LGPL, PSF, dll.)
