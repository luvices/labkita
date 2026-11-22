import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 Widescreen
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    c_bg_dark = RGBColor(15, 23, 42)      # Slate 900
    c_primary = RGBColor(30, 58, 138)     # Blue 900
    c_accent = RGBColor(234, 88, 12)      # Orange 600
    c_card_bg = RGBColor(241, 245, 249)   # Slate 100
    c_card_border = RGBColor(203, 213, 225)
    c_text_dark = RGBColor(30, 41, 59)
    c_text_muted = RGBColor(100, 116, 139)
    c_white = RGBColor(255, 255, 255)

    def add_header(slide, title, category="FINAL PROJECT SISTEM OPERASI 2026/2027"):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = category.upper()
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = c_accent
        
        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = c_primary

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE (Dark theme)
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = c_bg_dark
    bg1.line.color.rgb = c_bg_dark

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "FINAL PROJECT SISTEM OPERASI — GANJIL 2026/2027"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_accent

    p = tf1.add_paragraph()
    p.text = "LabKita Linux 0.4"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = c_white

    p = tf1.add_paragraph()
    p.text = "Distribusi Linux Turunan Ubuntu untuk Praktikum Pemrograman Tanpa Internet"
    p.font.size = Pt(20)
    p.font.color.rgb = RGBColor(148, 163, 184)
    p.space_after = Pt(24)

    p = tf1.add_paragraph()
    p.text = "Dosen Pengampu: Muhammad Sidik Asyaky, S.T., M.T.  |  Kategori A: Distro Linux Khusus"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_white

    p = tf1.add_paragraph()
    p.text = "Disusun oleh: Dafa Zahran (Ketua), Rafly Fauzi Pratama, Muhammad Ilham Rizky, Vadien Athallah Lukman"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(203, 213, 225)

    p = tf1.add_paragraph()
    p.text = "Repositori GitHub: https://github.com/luvices/labkita"
    p.font.size = Pt(11)
    p.font.color.rgb = c_accent

    # -------------------------------------------------------------
    # SLIDE 2: LATAR BELAKANG & VISI PRODUK
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Latar Belakang & Visi Produk LabKita Linux")

    # Card 1: Permasalahan di Lab
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = c_card_bg
    c1.line.color.rgb = c_card_border
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "Tantangan Laboratorium Komputer"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_primary
    p.space_after = Pt(12)
    bullets_1 = [
        "Ketergantungan Internet: Distro standar sering memerlukan koneksi online untuk mengunduh package/compiler.",
        "Koneksi Kampus Fluktuatif: Gangguan bandwidth menghentikan jalannya sesi praktikum mahasiswa.",
        "Distraksi & Penyalahgunaan: Akses web terbuka sering memicu mahasiswa membuka media sosial atau gaming saat jam kuliah.",
        "Kompleksitas Setup Pengajar: Dosen/asisten lab harus menginstal manual GCC, Python, dan editor pada puluhan PC."
    ]
    for b in bullets_1:
        p = tf_c1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = c_text_dark
        p.space_after = Pt(8)

    # Card 2: Visi & Solusi LabKita
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = RGBColor(239, 246, 255)
    c2.line.color.rgb = RGBColor(191, 219, 254)
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "Visi & Solusi: LabKita Linux"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_accent
    p.space_after = Pt(12)
    bullets_2 = [
        "100% Siap Pakai Offline: GCC, G++, Python 3, Geany, Make, dan Git sudah pre-installed di dalam ISO.",
        "Mandiri Sejak Booting: Media live-boot langsung menyediakan lingkungan pemrograman tanpa butuh setup.",
        "Keamanan Terisolasi: Mahasiswa praktikan tidak memiliki akses sudo dan folder pribadi terlindungi 0700.",
        "Workspace Cepat: Layanan systemd tmpfs (/run/labkita) otomatis membersihkan file sementara pasca restart.",
        "Standar Akademik: Sesuai silabus pemrograman C/Python dasar dan modul konsep Sistem Operasi."
    ]
    for b in bullets_2:
        p = tf_c2.add_paragraph()
        p.text = "✔ " + b
        p.font.size = Pt(12)
        p.font.color.rgb = c_text_dark
        p.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 3: PENERAPAN KONSEP SISTEM OPERASI
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Penerapan Konsep Inti Sistem Operasi (OS Concepts)")

    concepts = [
        ("1. Manajemen Memori & Filesystem", "Implementasi RAM disk (tmpfs) pada /run/labkita via systemd. Alokasi dynamic swap, serta manajemen partisi OverlayFS live root (/cow)."),
        ("2. Manajemen Proses & Multiprocessing", "Penyediaan modul multiprocessing Python (processes.py) mendemonstrasikan fork() proses anak, PID tracking, dan sinkronisasi komputasi paralel."),
        ("3. Keamanan & Kontrol Akses (Security)", "Pemisahan hak istimewa (Privilege Separation): Akun praktikan dibatasi tanpa grup sudo. Proteksi izin berkas direktori 0700 (drwx------)."),
        ("4. System Daemon & Inisialisasi", "Konfigurasi systemd target and unit service (labkita-runtime.service) yang dieksekusi otomatis pada multi-user.target saat boot time.")
    ]

    for idx, (head, desc) in enumerate(concepts):
        row = idx // 2
        col = idx % 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(1.8 + row * 2.5)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = c_card_bg
        card.line.color.rgb = c_card_border
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = c_primary
        p.space_after = Pt(6)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = c_text_dark

    # -------------------------------------------------------------
    # SLIDE 4: ARSITEKTUR & ALUR KERJA BUILD
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Arsitektur & Alur Kerja Pembuatan (Cubic Pipeline)")

    steps = [
        ("Step 1: Sumber Resmi", "Ubuntu 24.04.5 LTS Desktop amd64 ISO resmi diverifikasi integritas SHA256."),
        ("Step 2: Ekstraksi Cubic", "Cubic mengekstrak filesystem SquashFS asli ke chroot/systemd-nspawn container."),
        ("Step 3: Injeksi Payload", "Pemasangan paket (GCC, Python, Geany), wallpapers, service systemd, dan panduan."),
        ("Step 4: Regenerasi ISO", "Regenerasi md5sum.txt (957/957 OK) & xorriso hasilkan ISO (~6,07 GiB)."),
        ("Step 5: Verifikasi VM", "Uji autologin live, GUI vs TUI di disk kosong, Firefox Snap, & 5x benchmark 0.1–0.4.")
    ]

    for idx, (st, desc) in enumerate(steps):
        x = Inches(0.8 + idx * 2.38)
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.2), Inches(2.25), Inches(4.2))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(248, 250, 252)
        card.line.color.rgb = c_accent if idx == 2 else c_card_border
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"Tahap 0{idx+1}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = c_accent
        p2 = tf.add_paragraph()
        p2.text = st.split(": ")[1]
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = c_primary
        p2.space_after = Pt(10)
        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = c_text_dark

    # -------------------------------------------------------------
    # SLIDE 5: TOOLCHAIN & FITUR KUSTOMISASI
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Fitur Kustomisasi Nyata & Perangkat Praktikum")

    f1 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    f1.fill.solid()
    f1.fill.fore_color.rgb = c_card_bg
    f1.line.color.rgb = c_card_border
    tf = f1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Perangkat Lunak Pemrograman Offline"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_primary
    p.space_after = Pt(10)
    items = [
        "GCC & G++ 13.3.0: Compiler standar industri untuk bahasa C dan C++.",
        "Python 3.12.3: Lengkap dengan pustaka standar dan modul OS.",
        "GNU Make 4.3: Automasi build praktikum berskala multi-file.",
        "Geany 2.0 IDE: Text editor ringan dengan tombol Build & Run terintegrasi.",
        "Git 2.43: Version control untuk melatih kolaborasi kode lokal.",
        "Dokumentasi Offline: man-db, manpages-dev, dan materi HTML lokal."
    ]
    for it in items:
        p = tf.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(11.5)
        p.font.color.rgb = c_text_dark
        p.space_after = Pt(6)

    f2 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    f2.fill.solid()
    f2.fill.fore_color.rgb = c_card_bg
    f2.line.color.rgb = c_card_border
    tf2 = f2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Identitas Visual & Sistem Khusus"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_accent
    p.space_after = Pt(10)
    items2 = [
        "Tema WhiteSur & Dock: Tema GTK/Ikon/Kursor WhiteSur, tombol kiri, dock tengah bawah.",
        "Wallpaper & Bahasa: Gradien minimalis LabKita + Bahasa Indonesia + label konsisten 0.4.",
        "Panduan Lolos Snap: Disalin ke ~/Dokumen/Panduan-LabKita agar terbaca Firefox Snap.",
        "Manajemen Akun: labkita-postinstall buat akun praktikan 0700 non-sudo (grup labkita-praktikum).",
        "Suite Diagnostik: labkita-check 23/23 LULUS + uji baca nyata sandbox Firefox Snap (AppArmor OK)."
    ]
    for it in items2:
        p = tf2.add_paragraph()
        p.text = "✔ " + it
        p.font.size = Pt(11.5)
        p.font.color.rgb = c_text_dark
        p.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 6: KEAMANAN & ISOLASI HAK AKSES
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Manajemen Pengguna & Keamanan Sistem Lab")

    box_sec1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    box_sec1.fill.solid()
    box_sec1.fill.fore_color.rgb = RGBColor(254, 242, 242)
    box_sec1.line.color.rgb = RGBColor(252, 165, 165)
    tf = box_sec1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Pembatasan Hak Akses (Non-Sudo Account)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(185, 28, 28)
    p.space_after = Pt(12)
    sec_points = [
        "Akun Mahasiswa Terisolasi: Dibuat via 'sudo labkita-postinstall praktikan'.",
        "Tanpa Grup Sudo: User 'praktikan' hanya memiliki grup 'praktikan, labkita-praktikum'.",
        "Penolakan Akses Root: User praktikan tidak masuk grup sudo/adm maupun daftar sudoers.",
        "Uji Coba Akses Lintas User: User lain ditolak membaca /home/praktikan ('ls: ... Permission denied').",
        "Mencegah Sabotase: Praktikan tidak bisa menghapus paket inti, mengubah konfigurasi jaringan, atau merusak sistem operasi."
    ]
    for pt in sec_points:
        p = tf.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = c_text_dark
        p.space_after = Pt(8)

    box_sec2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    box_sec2.fill.solid()
    box_sec2.fill.fore_color.rgb = RGBColor(240, 253, 244)
    box_sec2.line.color.rgb = RGBColor(187, 247, 208)
    tf2 = box_sec2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Proteksi Berkas Mahasiswa (Chmod 0700)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(21, 128, 61)
    p.space_after = Pt(12)
    sec_points2 = [
        "Izin Ketat 0700: Folder '/home/praktikan' disetel ke mode (drwx------).",
        "Privasi Tugas Praktikum: Hanya pemilik akun yang dapat membaca dan menulis berkas latihannya.",
        "Teruji Nyata: User lain ('labkitavm') ditolak saat mencoba membaca folder praktikan (Permission denied).",
        "Pemberian Template Awal: Direktori otomatis dilengkapi contoh praktikum (/home/praktikan/Praktikum)."
    ]
    for pt in sec_points2:
        p = tf2.add_paragraph()
        p.text = "✔ " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = c_text_dark
        p.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 7: HASIL PENGUJIAN NYATA (TERMASUK TEMUAN GAGAL)
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Hasil Pengujian Nyata Pascainstalasi (Jujur & Transparan)")

    c7a = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    c7a.fill.solid()
    c7a.fill.fore_color.rgb = RGBColor(240, 253, 244)
    c7a.line.color.rgb = RGBColor(187, 247, 208)
    tf = c7a.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Komponen yang Lulus Uji (Sistem Terinstal)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = RGBColor(21, 128, 61)
    p.space_after = Pt(8)
    passed_items = [
        "Integritas ISO & Casper: md5sum 957/957 OK (kecuali boot.catalog, eltorito.img, .yaml.original).",
        "Autologin Live Session (PULIH): casper.log bebas error grup; langsung masuk desktop labkita.",
        "Instalasi TUI & Branding 0.4: GRUB ID 0.4, subiquity.cmd.tui sukses, os-release & sambutan 0.4.",
        "Desktop WhiteSur & ID: Tema WhiteSur, tombol kiri, dock tengah, wallpaper, Bahasa Indonesia.",
        "Panduan 0.4 di Firefox Snap: ~/Dokumen/Panduan-LabKita terbuka normal & labkita-check 23/23 LULUS.",
        "labkita-postinstall: Akun praktikan 0 error, isolasi 0700, non-sudo, grup labkita-praktikum.",
        "Offline Total (nmcli off) & Tmpfs: GCC (~/Praktikum), Python, processes.py sukses; /run/labkita 1777."
    ]
    for c in passed_items:
        p = tf.add_paragraph()
        p.text = "✔  " + c
        p.font.size = Pt(10)
        p.font.color.rgb = c_text_dark
        p.space_after = Pt(4)

    c7b = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    c7b.fill.solid()
    c7b.fill.fore_color.rgb = RGBColor(254, 242, 242)
    c7b.line.color.rgb = RGBColor(252, 165, 165)
    tf2 = c7b.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Kegagalan & Keterbatasan Terbuka 0.4"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = RGBColor(185, 28, 28)
    p.space_after = Pt(8)
    failed_items = [
        "GAGAL — Installer GUI ISO 0.4: Tidak dipulihkan oleh fix grup ('Ada yang salah' setelah Inhibiting Gnome session); penyebab installer GUI belum teridentifikasi.",
        "KANDIDAT TERSISA (BELUM DIUJI): .disk/info diawali 'LabKita' membuat casper menurunkan USERNAME=labkita (bukan 'ubuntu' spt Bisect #3 WSL), plus faktor Cubic vs WSL.",
        "PROSEDUR RESMI: Instalasi ke disk wajib via jalur TUI subiquity.cmd.tui.",
        "CATATAN TEKNIS — Flag noexec /run: Partisi /run bersifat noexec, sehingga biner C dikompilasi di ~/Praktikum."
    ]
    for f_it in failed_items:
        p = tf2.add_paragraph()
        p.text = "✖  " + f_it
        p.font.size = Pt(10)
        p.font.color.rgb = c_text_dark
        p.space_after = Pt(5)

    # -------------------------------------------------------------
    # SLIDE 8: TOLOK UKUR KINERJA & BENCHMARK (0.1 vs 0.2 vs 0.3 vs 0.4)
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Tolok Ukur Empiris 0.1 vs 0.2 vs 0.3 vs 0.4 (5x per Versi, VM Identik)")

    benchmarks = [
        ("Konsumsi RAM Rata-rata & Rentang", "free -m (VM 4 GB / 3.911 MiB)", "0.1 [7.0.0-31]: 1.038,2 MiB (1.016–1.056) | 0.2: 1.068,2 MiB (1.058–1.080)\n0.3 [7.0.0-43]: 1.058,2 MiB (1.046–1.067)\n0.4 [7.0.0-43]: 1.062,6 MiB avg (1.043–1.075 MiB)\nSisa RAM 0.4 avg: 2.847,8 MiB (~2,78 GiB)"),
        ("Waktu Booting Rata-rata & Rentang", "systemd-analyze time (5x Reboot)", "0.1: 8,460s (8,359–8,676s) | 0.2: 9,317s (9,072–9,458s)\n0.3: 8,808s (8,460–9,014s) | 0.4: 9,185s avg (8,520–10,713s)\nKesimpulan: tidak ada perbedaan yang dapat dibuktikan (rentang saling tumpang tindih & beda kernel)."),
        ("Variabel Kernel & Layanan Boot", "uname -r & systemd-analyze blame", "Kernel 0.1/0.2: 7.0.0-31-generic | 0.3/0.4: 7.0.0-43-generic (dari security updates TUI)\nplymouth-quit-wait: 2,18–3,04s | snapd.seeded: ~1,02–1,16s\ngraphical.target avg: 5,180s (0.1) | 5,918s (0.2) | 5,532s (0.3) | 5,779s (0.4)"),
        ("Identitas & Kapasitas Media ISO 0.4", "Cubic 2026.09.110 & SHA256", "Berkas: labkita-linux-0.4-amd64.iso\nUkuran: 6.520.395.776 bytes (~6,07 GiB / 6,52 GB)\nSHA256: 7ae9e815a02e58ca5f700344541aadba...87f64b9d4\nMD5: 00ea1d333ab0e52b953d7fe3806044ed | Unduh: [LINK-DRIVE-ISO]")
    ]

    for idx, (head, cmd, stats) in enumerate(benchmarks):
        col = idx % 2
        row = idx // 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(1.8 + row * 2.5)
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = c_card_bg
        card.line.color.rgb = c_card_border
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{head}  [{cmd}]"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = c_primary
        p.space_after = Pt(6)
        p2 = tf.add_paragraph()
        p2.text = stats
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = c_text_dark

    # -------------------------------------------------------------
    # SLIDE 9: TEMUAN TEKNIS & SANDBOX APPARMOR
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Temuan Teknis: Firefox Snap AppArmor & Kegagalan Installer")

    c1 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = c_card_bg
    c1.line.color.rgb = c_card_border
    tf = c1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Perbaikan yang Tuntas di Rilis 0.4"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_primary
    p.space_after = Pt(10)
    b_pts = [
        "Pulihkan Autologin Live (labkita-praktikum): Hapus bentrok grup 'labkita' -> casper sukses buat UID 1000 & masuk desktop langsung tanpa GIS.",
        "Lolos Sandbox Firefox Snap & Diagnostik: Panduan 0.4 di ~/Dokumen/Panduan-LabKita; labkita-check lulus 23/23 (snap run firefox OK).",
        "Postinstall & Integritas ISO: Akun praktikan 0 error (grup labkita-praktikum), metadata 0.4 konsisten, & md5sum 957/957 OK."
    ]
    for b in b_pts:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_text_dark
        p.space_after = Pt(6)

    c2 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = RGBColor(239, 246, 255)
    c2.line.color.rgb = RGBColor(191, 219, 254)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Bisect #1–#4 (WSL) vs ISO 0.4 (Cubic)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_accent
    p.space_after = Pt(10)
    sol_pts = [
        "Penyebab Autologin Terbukti & Pulih di 0.4: Bisect #4 buktikan bentrok .disk/info + groupadd labkita ('The group labkita already exists'); fix grup labkita-praktikum memulihkan autologin live labkita.",
        "Installer GUI Belum Pulih: Fix grup TIDAK memulihkan ubuntu-desktop-bootstrap pada ISO 0.4 ('Ada yang salah'); penyebab installer GUI belum teridentifikasi.",
        "Kandidat Tersisa (Belum Diuji) & Prosedur Resmi: .disk/info diawali 'LabKita' menurunkan USERNAME=labkita (vs 'ubuntu' di Bisect #3 WSL) belum diuji. Prosedur resmi = TUI subiquity.cmd.tui."
    ]
    for s in sol_pts:
        p = tf2.add_paragraph()
        p.text = "➜ " + s
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_text_dark
        p.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 10: BUKTI TANGKAPAN LAYAR NYATA VM TERINSTAL
    # -------------------------------------------------------------
    s_ev = prs.slides.add_slide(blank_layout)
    add_header(s_ev, "Bukti Tangkapan Layar Asli VM 0.4 (docs/evidence/)")

    ev_dir = Path("docs/evidence")
    ev_shots = [
        ("Live Autologin 0.4 Langsung Desktop (Tanpa GIS)", ev_dir / "0.4-01-live-autologin-desktop.png"),
        ("os-release 0.4 & labkita-check 23/23 LULUS", ev_dir / "0.4-08-os-release-and-labkita-check.png"),
        ("Firefox Snap Membuka Panduan LabKita 0.4", ev_dir / "0.4-10-firefox-snap-guide.png"),
        ("Benchmark 0.4 Run 1 (7.0.0-43, free/analyze)", ev_dir / "benchmarks" / "v04-r1.png"),
    ]
    for idx, (cap, img_p) in enumerate(ev_shots):
        col = idx % 2
        row = idx // 2
        x = Inches(1.1 + col * 5.9)
        y = Inches(1.6 + row * 2.85)
        if img_p.exists():
            s_ev.shapes.add_picture(str(img_p), x, y, height=Inches(2.35))
        cap_tb = s_ev.shapes.add_textbox(x, y + Inches(2.38), Inches(5.3), Inches(0.35))
        cp = cap_tb.text_frame.paragraphs[0]
        cp.text = cap
        cp.font.size = Pt(10)
        cp.font.bold = True
        cp.font.color.rgb = c_primary

    # -------------------------------------------------------------
    # SLIDE 10: PEMBAGIAN TUGAS KELOMPOK
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Struktur Tim & Pembagian Peran Kelompok")

    team = [
        ("Dafa Zahran — 257006111188", "Ketua Kelompok, Manajer Proyek & Integrasi (Build)", "Mengoordinasikan seluruh tahapan proyek, pipeline build Cubic, regenerasi md5sum & mastering ISO (labkita-linux-0.4-amd64.iso), repositori GitHub (github.com/luvices/labkita), dan kepatuhan silabus tugas."),
        ("Rafly Fauzi Pratama — 257006111152", "Pengembang Inti (Core Developer) & Toolchain", "Mengembangkan skrip kustomisasi Cubic (scripts/customize.sh), instalasi & konfigurasi compiler (GCC, G++, Python 3, Geany IDE), serta perancangan skrip pengujian labkita-check."),
        ("Muhammad Ilham Rizky — 257006111154", "Sistem, Keamanan & Penguji Kualitas (Sys, Sec & QA)", "Merancang layanan systemd labkita-runtime.service (tmpfs sticky bit 1777), skrip akun praktikan non-sudo (labkita-postinstall), isolasi izin 0700, serta tolok ukur benchmark RAM dan boot time."),
        ("Vadien Athallah Lukman — 257006111160", "Antarmuka, Dokumentasi & Media (UI/UX & Docs)", "Mendesain identitas visual distro (wallpaper SVG LabKita, konfigurasi dconf), modul materi panduan praktikum dan contoh kode (C/Python), penyusunan Laporan PDF Bab I-V, slide PPTX, dan naskah demo video.")
    ]

    for idx, (member, role, desc) in enumerate(team):
        col = idx % 2
        row = idx // 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(1.8 + row * 2.5)
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(2.3))
        card.fill.solid()
        card.fill.fore_color.rgb = c_card_bg
        card.line.color.rgb = c_card_border
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = member
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = c_primary
        p.space_after = Pt(2)
        p1 = tf.add_paragraph()
        p1.text = role
        p1.font.size = Pt(10.5)
        p1.font.bold = True
        p1.font.color.rgb = c_accent
        p1.space_after = Pt(4)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = c_text_dark

    # -------------------------------------------------------------
    # SLIDE 11: KESIMPULAN & SARAN
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Kesimpulan & Rencana Pengembangan Masa Depan")

    c1 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = c_card_bg
    c1.line.color.rgb = c_card_border
    tf = c1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Kesimpulan Akhir Proyek"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_primary
    p.space_after = Pt(10)
    concls = [
        "Produk Terwujud: ISO labkita-linux-0.4-amd64.iso (~6,07 GiB, SHA256 7ae9e815...87f64b9d4) terverifikasi md5sum 957/957 OK, autologin live pulih, & terinstal via subiquity TUI.",
        "Perbaikan 0.4 & Fitur Praktikum: Grup labkita-praktikum pulihkan autologin live; labkita-check 23/23 LULUS, Firefox Snap OK, postinstall 0 error.",
        "Benchmark 5x & Variabel Kernel: RAM avg 1.062,6 MiB (0.4) vs 1.038,2 / 1.068,2 / 1.058,2 MiB; boot avg 9,185s (7.0.0-43 dari security updates TUI) vs 8,460s / 9,317s (7.0.0-31) — tidak ada perbedaan yang dapat dibuktikan.",
        "Transparansi Jujur: Bentrok grup 'labkita' terbukti menyebabkan gagal autologin (pulih di 0.4); installer GUI tidak ikut pulih & penyebabnya belum teridentifikasi (.disk/info 'LabKita' -> USERNAME=labkita belum diuji). Prosedur resmi = TUI."
    ]
    for c in concls:
        p = tf.add_paragraph()
        p.text = "✔ " + c
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_text_dark
        p.space_after = Pt(6)

    c2 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = RGBColor(241, 245, 249)
    c2.line.color.rgb = c_card_border
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Rencana Pengembangan Rilis 0.5"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_accent
    p.space_after = Pt(10)
    future = [
        "Isolasi Build Cubic vs WSL: Bandingkan manifest & lapisan live build Cubic vs WSL untuk menuntaskan error GUI installer ubuntu-desktop-bootstrap.",
        "Penyelarasan Ikon Dock WhiteSur: Audit ulang cache ikon tema WhiteSur agar seluruh ikon favorit dock konsisten.",
        "Evaluasi Desktop Ringan: Menguji varian XFCE4/Openbox bila ditargetkan untuk PC laboratorium ber-RAM kecil.",
        "Kiosk Mode Ujian: Profil penguncian jaringan dan terminal untuk sesi evaluasi/ujian pemrograman."
    ]
    for f in future:
        p = tf2.add_paragraph()
        p.text = "➜ " + f
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_text_dark
        p.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 12: PENUTUP & TANYA JAWAB (Dark theme)
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    bg12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg12.fill.solid()
    bg12.fill.fore_color.rgb = c_bg_dark
    bg12.line.color.rgb = c_bg_dark

    tb12 = s12.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.5))
    tf12 = tb12.text_frame
    tf12.word_wrap = True

    p = tf12.paragraphs[0]
    p.text = "TERIMA KASIH"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = c_white
    p.space_after = Pt(10)

    p = tf12.add_paragraph()
    p.text = "LabKita Linux 0.4 — Ruang Belajar, Siap Offline."
    p.font.size = Pt(22)
    p.font.color.rgb = c_accent
    p.space_after = Pt(20)

    p = tf12.add_paragraph()
    p.text = "Sesi Tanya Jawab (Q&A)  |  Mata Kuliah Sistem Operasi 2026/2027"
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(148, 163, 184)

    # Save
    out_dir = Path("docs/presentation")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "labkita-presentation.pptx"
    prs.save(str(out_file))
    print(f"Presentation saved successfully to: {out_file}")

if __name__ == "__main__":
    create_deck()
