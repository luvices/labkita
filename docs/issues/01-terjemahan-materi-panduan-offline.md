# Issue 1: Peninjauan dan Penyempurnaan Teks Materi Panduan Praktikum Offline

- **Nomor:** #1
- **Pemilik (Assignee):** Vadien Athallah Lukman (@vadienal)
- **Peran:** Pengembang Antarmuka, Dokumentasi & Media
- **Label:** `documentation`, `content`, `ui/ux`
- **Prioritas:** Menengah
- **Status:** Terencana

## Deskripsi Singkat
Halaman panduan praktikum offline (`payload/usr/share/labkita/guide/index.html`) merupakan pusat informasi utama bagi mahasiswa saat koneksi laboratorium sedang terputus. Materi perlu ditinjau agar seluruh istilah, langkah praktikum, dan penjelasan teknis menggunakan Bahasa Indonesia yang komunikatif, baku, dan mudah dipahami pemula.

## Rincian Pekerjaan
1. Lakukan audit menyeluruh terhadap teks pada `payload/usr/share/labkita/guide/index.html`.
2. Pastikan panduan mencakup alur dasar:
   - Persiapan direktori pribadi di `~/Praktikum`.
   - Pemrograman C dasar (kompilasi `gcc` dan flags `-Wall -Wextra`).
   - Pemrograman Python dasar (eksekusi dan virtual environment).
   - Penjelasan multiprocessing dan konsep Child Process (PID/PPID).
   - Peringatan penggunaan ruang memori sementara `/run/labkita` (tmpfs).
3. Verifikasi tautan ke dokumentasi lokal dan manual page offline.

## Kriteria Selesai (Acceptance Criteria)
- [ ] Teks bebas dari istilah asing yang tidak baku.
- [ ] Tampilan responsif pada resolusi 1280x800 hingga 1920x1080.
- [ ] Pull request dibuka dan lolos review oleh anggota tim.
