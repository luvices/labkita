# Pengujian dan Hasil Verifikasi LabKita Linux 0.1

Dokumen ini mencatat seluruh skenario pengujian nyata yang telah dijalankan pada mesin virtual uji (`build/test-vm/labkita-test.vmx`) menggunakan ISO hasil build `labkita-linux-0.1-amd64.iso` (SHA256: `f80e42c9e8d4db820121f02fca79588760f1549a6cc6634929e3b0e071b810c5`).

Semua bukti tangkapan layar tersimpan pada folder `docs/evidence/`.

---

## 1. Tabel Hasil Uji Fungsional & Keamanan

| Skenario | Hasil yang Diharapkan | Hasil Aktual | Status | Bukti Tangkapan Layar |
| --- | --- | --- | :---: | --- |
| **Boot ISO di VM kosong** | Sesi live dan installer dapat dibuka, desktop termuat normal | Boot berhasil (kernel `7.0.0-31-generic`), resolusi 1280x800, wallpaper LabKita dan panduan desktop termuat | **LULUS** | `docs/evidence/01-labkita-check-pass.png` |
| **`labkita-check` setelah boot** | Seluruh pemeriksaan lulus (14 pengujian) | **14 dari 14 pemeriksaan LULUS, 0 gagal**. Terverifikasi: python3, gcc, g++, make, geany, git, man, panduan lokal, doc python, contoh python, proses anak, kompilasi C, sticky bit, systemd | **LULUS** | `docs/evidence/01-labkita-check-pass.png` |
| **`sudo labkita-postinstall praktikan`** | Membuat akun `praktikan`, meminta password interaktif, tanpa sudo | Akun `praktikan` berhasil dibuat. Password diset interaktif. Folder `/home/praktikan` dan `/home/praktikan/Praktikum` siap dengan contoh tugas | **LULUS** | `docs/evidence/02-labkita-postinstall.png` |
| **Izin folder `/home/praktikan`** | Mode permission `700` (`drwx------`) | `stat /home/praktikan` menunjukkan `(0700/drwx------) UID: 1002 GID: 1002`. Akses dari user lain ditolak (`Permission denied`) | **LULUS** | `docs/evidence/03-praktikan-permissions-and-groups.png` |
| **Hak akses sudo praktikan** | Tidak memperoleh hak administratif (`sudo -l` ditolak) | `sudo -l` menghasilkan `Désolé, l'utilisateur praktikan ne peut pas utiliser sudo sur labkitaadmin`. Grup: `praktikan, labkita` (tanpa grup `sudo`) | **LULUS** | `docs/evidence/04-praktikan-sudo-denied.png` |
| **Eksekusi praktikum (Python & C)** | Contoh program berjalan normal tanpa kompilasi/runtime error | `python3 hello.py` -> output "Halo dari LabKita Linux!"; `python3 processes.py` -> multiproses fork PID 5696 & 5697 sukses; `gcc -O2 hello.c -o hello && ./hello` -> sukses | **LULUS** | `docs/evidence/07-practicum-execution.png` |
| **Geany IDE siap pakai** | Geany dapat dibuka dan menampilkan berkas C dengan syntax highlighting | Geany 2.0 terbuka normal menampilkan `hello.c`, compiler panel aktif, menu integrasi build berjalan | **LULUS** | `docs/evidence/08-geany-ide.png` |
| **Matikan jaringan VM (Uji Offline Penuh)** | Python, GCC, man pages tetap bekerja saat jaringan dimatikan | `nmcli networking off` (status `connectivity: none`). `gcc 13.3.0`, `python 3.12.3`, dan manual man pages tetap berfungsi 100% tanpa internet | **LULUS** | `docs/evidence/09-offline-network-none-gcc.png` & `10-python-man-offline.png` |
| **Ruang kerja sementara `/run/labkita`** | Folder tmpfs dengan sticky bit `1777` terbuat via systemd | `ls -ld /run/labkita` menghasilkan `drwxrwxrwt 2 root root` (`1777`). Berkas sementara `/run/labkita/sementara.txt` berhasil dibuat dan hilang saat reboot | **LULUS** | `docs/evidence/06-df-and-systemd-blame.png` |
| **Menu Panduan LabKita** | Membuka materi praktikum offline di `/usr/share/labkita/guide/index.html` | Berkas lokal HTML dan aset tersedia di sistem. Peluncuran via peramban Snap Firefox terisolasi oleh AppArmor Sandbox confinement default Ubuntu. Solusi: disajikan melalui server python lokal (`python3 -m http.server 8000`) atau dipindahkan ke direktori home pengguna | **TERVERIFIKASI DENGAN CATATAN SANDBOX** | Pembahasan rinci pada Laporan Bab IV & V |

---

## 2. Pengukuran Penggunaan Sumber Daya (Empirical Benchmarks)

Pengukuran dilakukan pada mesin virtual VMware Workstation 25:
- **Konfigurasi Virtual**: 2 vCPU, RAM 4096 MB, Disk 40 GB NVMe/SCSI, BIOS boot, Display 1280x800.

### A. Penggunaan Memori (`free -m`)
*Dicatat 2 menit setelah sesi desktop aktif:*

| Komponen | Nilai Aktual (MB) | Persentase |
| --- | --- | --- |
| **Total Memori** | 3.911 MB | 100.0% |
| **Digunakan (Used)** | 1.342 MB | 34.3% |
| **Bebas (Free)** | 450 MB | 11.5% |
| **Shared** | 82 MB | 2.1% |
| **Buffer / Cache** | 2.451 MB | 62.7% |
| **Tersedia (Available)** | 2.568 MB | 65.7% |

> **Catatan Analisis:** Penggunaan RAM LabKita 0.1 sebesar ~1.34 GB sebanding dengan Ubuntu Desktop 24.04 LTS standar karena mempertahankan lingkungan GNOME Shell 46 dan stack live-installer. Sesuai prinsip integritas proyek, tidak ada klaim bahwa distro ini lebih ringan dari basisnya sebelum lingkungan desktop diganti dengan window manager yang lebih minimalis (seperti XFCE/Openbox pada rilis mendatang).

### B. Waktu Booting (`systemd-analyze`)

| Tahap Booting | Durasi Aktual |
| --- | --- |
| **Kernel Space** | 5.313 detik |
| **Userspace** | 54.672 detik |
| **Total Waktu Startup** | **59.985 detik** |
| **Waktu Hingga `graphical.target`** | **29.410 detik** |

#### Layanan Userspace Terlama (`systemd-analyze blame` Top 6):
1. `casper-md5check.service`: 25.242 detik (verifikasi integritas media live CD pada saat booting)
2. `snapd.seeded.service`: 20.497 detik (inisialisasi pre-seeded snap packages)
3. `snapd.service`: 7.839 detik (daemon snap Ubuntu)
4. `plymouth-quit-wait.service`: 7.266 detik (transisi splash screen ke display manager)
5. `snapd.apparmor.service`: 5.677 detik (pemuatan profil keamanan AppArmor)
6. `ldconfig.service`: 4.969 detik (pembaharuan cache dynamic linker)

### C. Penggunaan Ruang Penyimpanan Root (`df -h /`)

| Mount Point | Filesystem | Ukuran Total | Digunakan | Tersedia | Persentase |
| --- | --- | --- | --- | --- | --- |
| `/` | `/cow` (OverlayFS Live) | 2.0 GB | 67 MB | 1.9 GB | 4% |
| ISO Image | `labkita-linux-0.1-amd64.iso` | 6.05 GiB (6.493.779.968 bytes) | - | - | Selesai dikompresi SquashFS |
