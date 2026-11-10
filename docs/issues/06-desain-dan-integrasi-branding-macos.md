# Issue 6: Integrasi Desain Antarmuka macOS Bebas Aset Apple dan Wallpaper Orisinal

- **Nomor:** #6
- **Pemilik (Assignee):** Vadien Athallah Lukman (@vadienal)
- **Peran:** Pengembang Antarmuka, Dokumentasi & Media
- **Label:** `ui/ux`, `branding`, `theme`
- **Prioritas:** Tinggi
- **Status:** Terencana

## Deskripsi Singkat
Menerapkan estetika desktop bergaya macOS modern tanpa menggunakan aset berpemilik (*proprietary*) Apple Inc. Memastikan tata letak dock berada di bagian bawah tengah, sudut jendela membulat, bilah navigasi atas bersih, dan kustomisasi wallpaper gradien minimalis terpasang secara default.

## Rincian Pekerjaan
1. Rancang wallpaper gradien minimalis orisinal beresolusi 4K (3840x2160) dalam format SVG dan PNG:
   - Gradien mesh halus bernuansa biru, ungu lembut, dan aksen toska.
   - Logo vektor geometris khas LabKita Linux di bagian tengah.
2. Konfigurasikan profil dconf sistem (`payload/etc/dconf/db/local.d/20-labkita`):
   - Atur penempatan tombol jendela di sebelah kiri (`close,minimize,maximize:`).
   - Atur posisi dock di bawah tengah (*floating centered dock*) dengan auto-hide.
   - Pasang tema GTK `WhiteSur-Light`, icon `WhiteSur`, dan cursor `WhiteSur-cursors`.
3. Susun dokumen legalitas dan atribusi lisensi di `docs/CREDITS.md`.

## Kriteria Selesai (Acceptance Criteria)
- [ ] Tidak ada aset logo Apple, font SF Pro, atau wallpaper komersial Apple dalam repositori.
- [ ] Tema dan wallpaper aktif otomatis saat pengguna baru pertama kali masuk.
- [ ] Seluruh lisensi open source (GPL-3.0, OFL-1.1, CC-BY) terdokumentasi rapi.
