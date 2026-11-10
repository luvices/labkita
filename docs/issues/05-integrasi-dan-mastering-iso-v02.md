# Issue 5: Pipeline Mastering dan Rilis Master ISO LabKita Linux 0.2

- **Nomor:** #5
- **Pemilik (Assignee):** Dafa Zahran (@dafazahran)
- **Peran:** Ketua Kelompok, Manajer Proyek & Integrasi Build
- **Label:** `build`, `release`, `devops`
- **Prioritas:** Kritis
- **Status:** Terencana

## Deskripsi Singkat
Mengompilasi seluruh kustomisasi terbaru (lokalisasi Bahasa Indonesia, perbaikan peluncur panduan offline, tema WhiteSur GTK/icon/cursor, wallpaper gradien minimalis, dan font Inter) ke dalam master citra ISO versi 0.2 menggunakan Cubic di lingkungan chroot Ubuntu Noble.

## Rincian Pekerjaan
1. Bangun arsip payload terbaru menggunakan `python tools/pack.py`.
2. Impor `dist/labkita-kit.tar.gz` ke dalam terminal virtual Cubic.
3. Eksekusi `bash scripts/customize.sh --cubic` di lingkungan nspawn Cubic.
4. Pada tab Boot Cubic, tambahkan parameter kernel:
   `locale=id_ID.UTF-8 keyboard-configuration/layoutcode=us console-setup/layoutcode=us`
5. Lakukan kompresi dan mastering citra ISO `labkita-linux-0.2-amd64.iso`.
6. Hitung checksum integritas resmi:
   - MD5: `labkita-linux-0.2-amd64.iso.md5`
   - SHA256: `labkita-linux-0.2-amd64.iso.sha256`

## Kriteria Selesai (Acceptance Criteria)
- [ ] Berkas ISO versi 0.2 berhasil dihasilkan tanpa error pemaketan xorriso.
- [ ] Checksum SHA256 tercatat pada repositori dan README.
- [ ] Master ISO siap diuji pada mesin virtual terpisah.
