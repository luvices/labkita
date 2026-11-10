# Issue 4: Pengukuran Tolok Ukur Empiris Penggunaan RAM dan Waktu Booting

- **Nomor:** #4
- **Pemilik (Assignee):** Muhammad Ilham Rizky (@ilhamrizky)
- **Peran:** Sistem, Keamanan & Penguji Kualitas (QA)
- **Label:** `benchmark`, `performance`, `empirical`
- **Prioritas:** Tinggi
- **Status:** Terencana

## Deskripsi Singkat
Sesuai aturan akademik, dilarang mengklaim sistem "lebih ringan" atau "lebih cepat" tanpa bukti empiris terukur. Penambahan tema WhiteSur, kursor, dan wallpaper resolusi tinggi berpotensi meningkatkan konsumsi RAM dan memperpanjang waktu inisialisasi desktop. Pengukuran objektif harus dicatat apa adanya.

## Rincian Pekerjaan
1. Lakukan *cold boot* pada mesin virtual uji (spesifikasi: 2 vCPU, RAM 4096 MB).
2. Ukur waktu booting sistem menggunakan systemd analyzer:
   ```bash
   systemd-analyze
   systemd-analyze blame | head -n 15
   ```
3. Ukur konsumsi memori sistem dalam keadaan idle (setelah desktop GNOME memuat sempurna):
   ```bash
   free -m
   free -h
   ```
4. Bandingkan data versi 0.1 (basis default) dengan versi 0.2 (tema macOS WhiteSur aktif):
   - Hitung selisih penggunaan RAM (MB).
   - Hitung selisih waktu loading graphical target (detik).
5. Buat tangkapan layar terminal sebagai bukti otentik.

## Kriteria Selesai (Acceptance Criteria)
- [ ] Tabel perbandingan metrik kinerja tercatat lengkap di `docs/TEST-PLAN.md`.
- [ ] Bukti tangkapan layar `free -m` dan `systemd-analyze` tersimpan di `docs/evidence/`.
- [ ] Analisis dampak kinerja dilaporkan secara objektif tanpa manipulasi data.
