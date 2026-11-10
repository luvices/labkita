# Issue 2: Penambahan Contoh Kode Praktikum Konsep Sistem Operasi (C & Python)

- **Nomor:** #2
- **Pemilik (Assignee):** Rafly Fauzi Pratama (@raflyfp)
- **Peran:** Pengembang Inti (Core Developer) & Toolchain
- **Label:** `enhancement`, `practicum`, `toolchain`
- **Prioritas:** Tinggi
- **Status:** Terencana

## Deskripsi Singkat
Praktikan memerlukan contoh kode yang siap dijalankan secara offline untuk mempelajari konsep dasar sistem operasi, khususnya penjadwalan proses, alokasi memori, dan pembuatan thread/proses anak.

## Rincian Pekerjaan
1. Buat contoh kode C baru di `payload/usr/share/labkita/examples/`:
   - `fork_demo.c`: Demonstrasi pembuatan proses anak menggunakan fungsi `fork()`, pemisahan alur eksekusi `if (pid == 0)`, dan fungsi `wait()`.
   - `memory_demo.c`: Demonstrasi alokasi dinamis memori heap (`malloc`/`free`) dan pembacaan memori virtual.
2. Buat skrip Python di `payload/usr/share/labkita/examples/`:
   - `thread_demo.py`: Demonstrasi modul `threading` dan *race condition* sederhana.
3. Uji kompilasi seluruh kode sumber di lingkungan Linux lokal sebelum commit.

## Kriteria Selesai (Acceptance Criteria)
- [ ] Berkas contoh berhasil dikompilasi dengan `gcc -Wall -Wextra -Werror` tanpa warning.
- [ ] Skrip Python dapat dieksekusi tanpa modul eksternal pip (hanya standard library).
- [ ] Kode ditambahkan ke template skeleton user (`/etc/skel/Praktikum/`).
