# Panduan Kontribusi Tim - LabKita Linux

Selamat datang di repositori proyek **LabKita Linux**. Dokumen ini menjadi pedoman alur kerja (*git workflow*) kolaboratif bagi seluruh anggota kelompok dalam mengembangkan, menguji, dan mendokumentasikan distribusi sistem operasi ini.

---

## 1. Identitas Akun & Repositori

- **Repositori Resmi:** `https://github.com/luvices/labkita.git`
- **Cabang Utama:** `main`

Setiap anggota tim **wajib** menggunakan identitas Git pribadi masing-masing saat bekerja di mesin lokal, sesuai dengan akun GitHub yang terdaftar. Jangan pernah memalsukan atau mengubah identitas commit anggota lain.

Sebelum membuat commit pertama, atur identitas di terminal lokal:
```bash
git config user.name "Nama Lengkap Anda"
git config user.email "email-github-anda@example.com"
```

---

## 2. Alur Kerja Cabang (*Branching Strategy*)

Untuk menjaga kestabilan cabang `main`, **dilarang melakukan commit langsung ke `main`**. Seluruh fitur, pengujian, dan dokumentasi harus dikerjakan pada cabang fitur (*feature branch*):

1. **Sinkronisasi cabang `main` terbaru:**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Buat cabang baru sesuai tugas:**
   Format penamaan cabang:
   - Fitur sistem/antarmuka: `feature/<nama-fitur>`
   - Dokumentasi/laporan: `docs/<nama-dokumen>`
   - Pengujian/benchmark: `test/<fokus-pengujian>`
   - Perbaikan bug: `fix/<deskripsi-bug>`

   Contoh:
   ```bash
   git checkout -b feature/pointer-example
   # atau
   git checkout -b docs/translate-guide
   ```

---

## 3. Konvensi Pesan Commit (*Conventional Commits*)

Gunakan pesan commit yang deskriptif, terstruktur, dan berbahasa Indonesia atau format konvensional standar:

- `feat:` Penambahan fitur, skrip, atau komponen baru.
- `fix:` Perbaikan bug, kesalahan konfigurasi, atau perizinan berkas.
- `docs:` Pembaruan dokumentasi, panduan offline, catatan uji, atau spesifikasi sistem.
- `test:` Penambahan pengujian mandiri, hasil benchmark, atau tangkapan layar uji.
- `chore:` Pemeliharaan repositori, struktur folder, atau konfigurasi paket.

Contoh pesan commit yang baik:
```bash
git commit -m "feat(examples): tambahkan contoh implementasi fork dan execve di bahasa C"
git commit -m "docs(guide): perbaiki penjelasan hak akses memori sementara di panduan offline"
git commit -m "test(vm): tambahkan hasil benchmark penggunaan RAM sebelum dan sesudah tema"
```

---

## 4. Pengujian Lokal Sebelum Push

Sebelum mendorong (*push*) perubahan ke GitHub:
1. Pastikan skrip shell memiliki hak eksekusi (`chmod 0755`) dan menggunakan *line ending* LF.
2. Jalankan pengujian mandiri jika bekerja pada lingkungan VM LabKita:
   ```bash
   python3 payload/usr/local/bin/labkita-check
   ```
3. Pastikan tidak ada berkas temporer, kredensial lokal, berkas besar ISO/VMDK, atau path absolut laptop pribadi yang tidak sengaja terlacak Git.

---

## 5. Pengajuan Pull Request (PR) & Peer Review

1. **Dorong cabang ke GitHub:**
   ```bash
   git push -u origin feature/<nama-fitur>
   ```
2. **Buka Pull Request:**
   - Masuk ke antarmuka GitHub repositori `luvices/labkita`.
   - Klik **Compare & pull request**.
   - Berikan deskripsi singkat: masalah yang diselesaikan, berkas yang diubah, dan bukti pengujian.
   - Hubungkan ke nomor Issue terkait (contoh: `Resolves #2`).
3. **Peer Review:**
   - Minimal 1 anggota tim lain harus meninjau kode/dokumen sebelum PR disetujui.
   - Ketua tim (Dafa Zahran) akan melakukan merge ke cabang `main` setelah review selesai.

---

## 6. Pembagian Peran Anggota

| Nama | NPM | Peran Utama | Fokus Kontribusi |
| :--- | :---: | :--- | :--- |
| **Dafa Zahran** | 257006111188 | Ketua, Arsitektur Sistem & Build ISO | Pipeline build ISO 0.6 (`autoinstall nocloud`), pengelolaan repositori GitHub, manajemen rilis & integrasi sistem. |
| **Vadien Athallah Lukman** | 257006111160 | UI/UX, Branding & Dokumentasi Teknis | Identitas merek Keystone LK, wallpaper, pemulihan ikon WhiteSur, buku kerja 7 modul, visual README & penataan dokumentasi. |
| **Rafly Fauzi Pratama** | 257006111152 | Penyusunan Laporan & Materi Praktikum | Menyusun narasi laporan proyek (BAB I-V), uji fungsional materi/contoh C & Python serta panduan kerja luring, dan naskah demo. |
| **Muhammad Ilham Rizky** | 257006111154 | QA, Evaluasi Keamanan & Penyusunan Laporan | Menyusun checklist QA & evaluasi keamanan (`docs/QA-CHECKLIST.md`), pengujian isolasi akun `praktikan` (`0700`, non-`sudo`) & `tmpfs` di VMware, serta rekap hasil uji ke laporan akhir. |
