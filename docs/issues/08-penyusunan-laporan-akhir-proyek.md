# Issue 8: Pembaruan dan Penyusunan Laporan Proyek Akhir Sistem Operasi (PDF)

- **Nomor:** #8
- **Pemilik (Assignee):** Vadien Athallah Lukman (@vadienal) & Dafa Zahran (@dafazahran)
- **Peran:** Dokumentasi & Ketua Kelompok
- **Label:** `documentation`, `academic`, `report`
- **Prioritas:** Tinggi
- **Status:** Terencana

## Deskripsi Singkat
Menyusun dan memutakhirkan Laporan Proyek Akhir Sistem Operasi (format PDF standar akademik) yang memuat landasan teori, metodologi rancang bangun, analisis hasil pengujian empiris versi 0.2, perbandingan tolok ukur, dan pembagian tugas kelompok.

## Rincian Pekerjaan
1. Perbarui generator laporan PDF (`tools/generate_report_pdf.py`):
   - Bab I: Latar belakang kendala laboratorium dan pembaruan arsitektur versi 0.2.
   - Bab II: Perancangan sistem (manajemen memori tmpfs, isolasi hak akses, dan tema macOS open-source).
   - Bab III: Implementasi teknis (paket lokalisasi id_ID, peluncur `labkita-guide`, skrip kustomisasi Cubic).
   - Bab IV: Analisis hasil pengujian empiris (tabel perbandingan RAM & waktu booting, bukti tangkapan layar antarmuka baru).
   - Bab V: Kesimpulan dan evaluasi kelebihan/kekurangan sistem.
2. Lampirkan lembar pengesahan kontribusi anggota kelompok dan pernyataan kejujuran akademik.
3. Kompilasi PDF menggunakan ReportLab dan verifikasi keterbacaan tipografi.

## Kriteria Selesai (Acceptance Criteria)
- [ ] Berkas laporan `docs/LAPORAN-PROYEK-LABKITA.pdf` terkompilasi rapi tanpa error visual.
- [ ] Data metrik pada laporan selaras 100% dengan hasil pengujian aktual di VM.
- [ ] Pembagian peran keempat anggota kelompok tertulis transparan.
