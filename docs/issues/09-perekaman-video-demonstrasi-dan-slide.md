# Issue 9: Pemutakhiran Slide Presentasi dan Produksi Video Demonstrasi

- **Nomor:** #9
- **Pemilik (Assignee):** Rafly Fauzi Pratama (@raflyfp) & Vadien Athallah Lukman (@vadienal)
- **Peran:** Pengembang Inti & Pengembang Media
- **Label:** `presentation`, `video`, `multimedia`
- **Prioritas:** Sedang
- **Status:** Terencana

## Deskripsi Singkat
Menyiapkan materi presentasi luring dan video demonstrasi interaktif berdurasi 3–5 menit yang membuktikan seluruh fitur unggulan LabKita Linux 0.2 berjalan mulus di hadapan penguji/dosen.

## Rincian Pekerjaan
1. Perbarui slide presentasi (`docs/presentation/labkita-presentation.pptx`):
   - Tambahkan slide perbandingan tampilan (sebelum vs sesudah tema WhiteSur).
   - Masukkan grafik tolok ukur penggunaan memori RAM dan waktu boot.
   - Perbarui foto antarmuka Bahasa Indonesia dan peluncur panduan offline.
2. Perbarui naskah demo (`docs/DEMO-SCRIPT.md`):
   - Scene 1: Bootloader GRUB berbahasa Indonesia dan desktop modern.
   - Scene 2: Eksekusi otomatis suite diagnostik `labkita-check`.
   - Scene 3: Pembuktian praktikum offline di Geany (C & Python).
   - Scene 4: Demonstrasi isolasi keamanan `sudo` dan perizinan `0700`.
   - Scene 5: Penjelasan ruang kerja memori sementara `/run/labkita`.
3. Rekam demo video sesuai alur naskah dan simpan tautan/rekaman untuk pengumpulan UAS.

## Kriteria Selesai (Acceptance Criteria)
- [ ] Berkas PPTX 16:9 widescreen selesai disusun dengan visual profesional.
- [ ] Naskah video memandu durasi 3–5 menit dengan pembagian peran presenter yang jelas.
- [ ] Seluruh materi selaras dengan spesifikasi rilis LabKita Linux 0.2.
