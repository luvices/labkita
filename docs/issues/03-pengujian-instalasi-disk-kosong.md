# Issue 3: Pengujian Instalasi Mandiri pada Disk Virtual Kosong

- **Nomor:** #3
- **Pemilik (Assignee):** Muhammad Ilham Rizky (@ilhamrizky)
- **Peran:** Sistem, Keamanan & Penguji Kualitas (QA)
- **Label:** `testing`, `installation`, `qa`
- **Prioritas:** Tinggi
- **Status:** Terencana

## Deskripsi Singkat
Master ISO LabKita Linux harus dapat dipasang secara mulus ke media penyimpanan fisik maupun mesin virtual tanpa error partisi, kegagalan bootloader GRUB, atau ketergantungan koneksi internet saat proses instalasi berjalan.

## Rincian Pekerjaan
1. Buat mesin virtual pengujian baru (VMware Workstation atau VirtualBox) dengan disk virtual NVMe/SATA kosong berkapasitas 25–40 GB.
2. Lakukan instalasi penuh menggunakan installer bawaan Ubuntu Desktop:
   - Pilih skema partisi otomatis (*Erase disk and install Ubuntu/LabKita*).
   - Setel nama pengguna administrator pengelola laboratorium.
3. Verifikasi proses reboot pascainstalasi:
   - Pastikan bootloader GRUB langsung memuat instalasi LabKita.
   - Pastikan antarmuka login grafis (GDM3) tampil normal.
4. Dokumentasikan log instalasi jika terdapat peringatan/error.

## Kriteria Selesai (Acceptance Criteria)
- [ ] Sistem terinstal 100% dan dapat melakukan booting mandiri dari disk.
- [ ] Tangkapan layar langkah instalasi disimpan pada `docs/evidence/`.
- [ ] Laporan pengujian dicatat pada matriks pengujian `docs/TEST-PLAN.md`.
