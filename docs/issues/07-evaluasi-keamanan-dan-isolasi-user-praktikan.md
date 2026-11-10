# Issue 7: Audit Keamanan Hak Akses dan Isolasi Pengguna Mahasiswa (Non-Sudo)

- **Nomor:** #7
- **Pemilik (Assignee):** Muhammad Ilham Rizky (@ilhamrizky)
- **Peran:** Sistem, Keamanan & Penguji Kualitas (QA)
- **Label:** `security`, `permissions`, `audit`
- **Prioritas:** Kritis
- **Status:** Terencana

## Deskripsi Singkat
Laboratorium komputer memerlukan jaminan bahwa mahasiswa tidak dapat merusak konfigurasi sistem, menginstal paket sembarangan, atau membaca direktori mahasiswa lain. Skrip manajemen akun `labkita-postinstall` harus memastikan isolasi izin ketat dan larangan akses istimewa root.

## Rincian Pekerjaan
1. Buat akun praktikan menggunakan utilitas sistem:
   ```bash
   sudo labkita-postinstall praktikan
   ```
2. Uji larangan eksekusi hak istimewa (sudo restriction):
   - Masuk sebagai user `praktikan`.
   - Jalankan `sudo -l` atau `sudo apt update`.
   - Verifikasi bahwa sistem menolak eksekusi dan mencatat upaya pelanggaran.
3. Uji perizinan direktori rumah mahasiswa:
   - Verifikasi mode folder `/home/praktikan` berstatus `0700` (`drwx------`).
   - Buat user kedua, buktikan user kedua ditolak saat mencoba masuk ke `/home/praktikan`.
4. Uji sifat non-persistensi direktori memori sementara `/run/labkita` (sticky bit `1777`).

## Kriteria Selesai (Acceptance Criteria)
- [ ] User praktikan terbukti gagal menjalankan perintah berhak akses root/sudo.
- [ ] Hak akses direktori `/home/praktikan` terisolasi dengan mode `0700`.
- [ ] Berkas sementara di `/run/labkita` terhapus bersih saat sistem dimatikan atau direstart.
