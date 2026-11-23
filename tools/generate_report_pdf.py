import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress headers/footers on cover page
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header
        self.drawString(54, 800, "Laporan Final Project Sistem Operasi — LabKita Linux 0.5")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 794, 541, 794)
        
        # Footer
        self.line(54, 45, 541, 45)
        page_str = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(541, 32, page_str)
        self.drawString(54, 32, "Program Studi Teknik Informatika / Ilmu Komputer — Ganjil 2026/2027")
        self.restoreState()

def build_pdf(filename="docs/LAPORAN-PROYEK-LABKITA.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Palette
    c_primary = colors.HexColor("#1E3A8A")  # Deep Blue
    c_secondary = colors.HexColor("#0F172A") # Slate 900
    c_accent = colors.HexColor("#EA580C")   # Orange
    c_dark = colors.HexColor("#334155")     # Slate 700
    c_muted = colors.HexColor("#64748B")    # Slate 500
    c_bg_head = colors.HexColor("#F1F5F9")  # Slate 100

    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=c_primary,
        alignment=1, # Center
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=c_dark,
        alignment=1,
        spaceAfter=24
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_accent,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        alignment=4, # Justify
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F8FAFC"),
        borderPadding=4,
        spaceAfter=6
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=c_muted,
        alignment=1,
        spaceBefore=3,
        spaceAfter=8
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("LAPORAN AKHIR FINAL PROJECT<br/>MATA KULIAH SISTEM OPERASI", ParagraphStyle('CoverPre', fontName='Helvetica-Bold', fontSize=14, leading=18, alignment=1, textColor=c_accent)))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="60%", thickness=2, color=c_accent, spaceBefore=5, spaceAfter=20))
    story.append(Paragraph("LABKITA LINUX 0.5", title_style))
    story.append(Paragraph("Pengembangan Distribusi Linux Turunan Ubuntu 24.04 LTS untuk Praktikum Pemrograman Dasar Mandiri Tanpa Ketergantungan Internet", subtitle_style))
    story.append(Spacer(1, 40))

    meta_text = """
    <b>Semester / Tahun Akademik:</b> Ganjil 2026/2027<br/>
    <b>Dosen Pengampu:</b> Muhammad Sidik Asyaky, S.T., M.T.<br/>
    <b>Kategori Proyek:</b> Kategori A — Distro Linux dengan Visi Tertentu<br/>
    <b>Repositori GitHub:</b> https://github.com/luvices/labkita
    """
    story.append(Paragraph(meta_text, ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=10, leading=16, alignment=1, textColor=c_dark)))
    story.append(Spacer(1, 45))

    team_cover = [
        ["No", "Nama Mahasiswa", "NPM", "Peran Utama"],
        ["1", "Dafa Zahran", "257006111188", "Ketua Kelompok & Integrasi (Build)"],
        ["2", "Rafly Fauzi Pratama", "257006111152", "Pengembang Inti (Core Developer)"],
        ["3", "Muhammad Ilham Rizky", "257006111154", "Sistem, Keamanan & QA"],
        ["4", "Vadien Athallah Lukman", "257006111160", "Antarmuka, Dokumentasi & Media"]
    ]
    t_cover = Table(team_cover, colWidths=[25, 160, 95, 170])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 40))
    story.append(Paragraph("PROGRAM STUDI TEKNIK INFORMATIKA / ILMU KOMPUTER<br/>TAHUN 2026", ParagraphStyle('CoverFoot', fontName='Helvetica-Bold', fontSize=10, leading=14, alignment=1, textColor=c_secondary)))
    story.append(PageBreak())

    # =========================================================================
    # DAFTAR ISI
    # =========================================================================
    story.append(Paragraph("DAFTAR ISI", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=10))
    toc_data = [
        ["BAB I", "PENDAHULUAN", "3"],
        ["", "1.1 Latar Belakang Masalah", "3"],
        ["", "1.2 Visi dan Tujuan Produk", "3"],
        ["", "1.3 Sasaran Pengguna", "3"],
        ["", "1.4 Ruang Lingkup Proyek", "3"],
        ["", "1.5 Pembagian Tugas dan Kontribusi Anggota Kelompok", "4"],
        ["BAB II", "LANDASAN TEORI SISTEM OPERASI", "5"],
        ["", "2.1 Konsep Manajemen Proses dan Multiprocessing", "5"],
        ["", "2.2 Manajemen Memori dan Virtual Filesystem (Tmpfs)", "5"],
        ["", "2.3 Keamanan Sistem Operasi dan Privilege Separation", "5"],
        ["", "2.4 Inisialisasi Sistem dan Layanan Daemon (Systemd)", "5"],
        ["", "2.5 Arsitektur Live CD dan OverlayFS", "5"],
        ["BAB III", "PERANCANGAN SISTEM", "6"],
        ["", "3.1 Arsitektur LabKita Linux", "6"],
        ["", "3.2 Alur Kerja Build ISO 0.5 (WSL) vs Riwayat Cubic (0.1–0.4)", "6"],
        ["", "3.3 Rancangan Antarmuka dan Pengalaman Pengguna (UI/UX)", "6"],
        ["", "3.4 Spesifikasi Perangkat Keras dan Perangkat Lunak", "6"],
        ["BAB IV", "IMPLEMENTASI DAN PENGUJIAN", "7"],
        ["", "4.1 Langkah-Langkah Implementasi", "7"],
        ["", "4.2 Skenario dan Hasil Pengujian Fungsional", "7"],
        ["", "4.3 Pengukuran Kinerja dan Tolok Ukur Empiris (0.1–0.5)", "8"],
        ["", "4.4 Pembahasan Temuan Teknis: Bisect #4, ProductService & Pemulihan GUI 0.5", "9"],
        ["BAB V", "PENUTUP", "10"],
        ["", "5.1 Kesimpulan", "10"],
        ["", "5.2 Keterbatasan Terbuka & Perbandingan Build Cubic vs WSL", "10"],
        ["", "5.3 Saran Pengembangan Rilis Selanjutnya (0.6+)", "10"],
        ["DAFTAR PUSTAKA DAN LAMPIRAN", "", "11"],
        ["", "Daftar Pustaka", "11"],
        ["", "Lampiran 1: Tautan Repositori Kode Sumber dan Berkas ISO", "11"],
        ["", "Lampiran 2: Naskah dan Tautan Video Demonstrasi (3-5 Menit)", "11"],
        ["", "Lampiran 3: Pernyataan Kejujuran Akademik dan Penggunaan AI", "12"]
    ]
    t_toc = Table(toc_data, colWidths=[55, 380, 45])
    t_toc.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('TEXTCOLOR', (0,0), (-1,-1), c_dark),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # BAB I: PENDAHULUAN
    # =========================================================================
    story.append(Paragraph("BAB I. PENDAHULUAN", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("1.1 Latar Belakang Masalah", h2_style))
    story.append(Paragraph(
        "Praktikum pemrograman dasar dan sistem operasi merupakan mata kuliah fundamental dalam kurikulum ilmu komputer dan teknik informatika. "
        "Pada pelaksanaannya di laboratorium komputer kampus, kelancaran sesi praktikum seringkali menghadapi kendala infrastruktur jaringan internet. "
        "Ketergantungan terhadap koneksi internet untuk mengunduh pustaka (library), compiler, paket perangkat lunak, maupun modul dokumentasi kerap memicu hambatan teknis saat bandwidth kampus mengalami penurunan performa atau gangguan mendadak.",
        body_style
    ))
    story.append(Paragraph(
        "Di sisi lain, ketersediaan koneksi internet terbuka di komputer praktikum sering kali menjadi sumber distraksi bagi mahasiswa. "
        "Akses web yang tidak terbatas memudahkan mahasiswa membuka media sosial, video streaming, atau platform permainan daring saat sesi penyampaian materi berlangsung. "
        "Selain itu, asisten laboratorium dibebani oleh tugas administratif berulang untuk melakukan instalasi perangkat lunak (seperti GCC, Python, dan text editor) di puluhan unit komputer setiap semester baru dimulai.",
        body_style
    ))

    story.append(Paragraph("1.2 Visi dan Tujuan Produk", h2_style))
    story.append(Paragraph(
        "Proyek <b>LabKita Linux</b> hadir sebagai wujud nyata penerapan prinsip-prinsip sistem operasi dalam menyelesaikan permasalahan di lingkungan akademik. "
        "Visi dari LabKita Linux adalah menghadirkan sistem operasi praktikum mandiri (self-contained) yang siap pakai sejak detik pertama booting tanpa membutuhkan koneksi internet sama sekali (<i>Ruang belajar. Siap offline.</i>).",
        body_style
    ))
    story.append(Paragraph("Tujuan utama pengembangan LabKita Linux meliputi:", body_style))
    story.append(Paragraph("1. <b>Kemandirian Offline Total:</b> Mengintegrasikan seluruh compiler (GCC, G++), interpreter (Python 3), build automation (Make), debugger, editor kode (Geany), serta manual sistem (man-db) langsung di dalam berkas citra ISO bootable.", bullet_style))
    story.append(Paragraph("2. <b>Keamanan dan Isolasi Hak Akses:</b> Mengimplementasikan pembatasan hak akses berbasis pengguna (privilege separation) di mana akun praktikan tidak memiliki izin administratif (non-sudo) dan folder kerja mahasiswa terlindungi secara ketat.", bullet_style))
    story.append(Paragraph("3. <b>Efisiensi Penyimpanan Sesi:</b> Menyediakan area kerja temporer berbasis memori virtual (tmpfs) dengan mekanisme sticky bit yang otomatis bersih saat restart, menjaga integritas dan kebersihan sistem lab komputer.", bullet_style))
    story.append(Paragraph("4. <b>Kemudahan Distribusi:</b> Menyajikan format berkas ISO hibrida standar yang dapat dijalankan secara langsung via Live USB, instalasi fisik, maupun mesin virtual (VMware Workstation dan VirtualBox).", bullet_style))

    story.append(Paragraph("1.3 Sasaran Pengguna", h2_style))
    story.append(Paragraph(
        "Sasaran pengguna produk LabKita Linux terbagi atas dua kelompok utama:",
        body_style
    ))
    story.append(Paragraph("• <b>Mahasiswa Praktikan:</b> Memperoleh lingkungan belajar yang seragam, stabil, bebas distraksi, dan siap digunakan untuk menulis kode C, C++, algoritma struktur data, serta simulasi multiproses sistem operasi.", bullet_style))
    story.append(Paragraph("• <b>Asisten Laboratorium dan Dosen:</b> Mengeliminasi waktu persiapan perangkat lunak di awal semester, menjamin kepatuhan akademik selama praktikum/ujian, serta memudahkan standardisasi evaluasi penilaian praktikum.", bullet_style))

    story.append(Paragraph("1.4 Ruang Lingkup Proyek", h2_style))
    story.append(Paragraph(
        "Ruang lingkup pengerjaan LabKita Linux versi 0.5 (dibangun dari tag <code>v0.5-iso</code>) meliputi:",
        body_style
    ))
    story.append(Paragraph("1. Basis distribusi menggunakan Ubuntu Desktop 24.04.5 LTS (Noble Numbat) arsitektur x86_64; instalasi bersih 0.1 dan 0.2 berjalan pada kernel Linux 7.0.0-31-generic, sedangkan 0.3, 0.4, dan 0.5 pada 7.0.0-43-generic.", bullet_style))
    story.append(Paragraph("2. Perangkat lunak pemrograman mencakup GCC 13.3.0, G++ 13.3.0, Make 4.3, Python 3.12.3, Geany 2.0, Git 2.43, Nano, dan pustaka manpages-dev.", bullet_style))
    story.append(Paragraph("3. Pembuatan citra ISO 0.5 menggunakan skrip reproducible WSL <code>tools/build_v05.py</code> (resep Bisect #3, non-Cubic) beserta normalisasi LF dan regenerasi md5sum.txt (arsip 0.1–0.4 dibuat via Cubic 2026.09.110).", bullet_style))
    story.append(Paragraph("4. Pengujian dilakukan secara empiris pada hypervisor VMware Workstation 25 mencakup verifikasi integritas ISO, bisect #1–#4, uji live autologin & installer GUI penuh pada 0.5 (TUI sebagai cadangan), labkita-check (Firefox Snap AppArmor OK), labkita-postinstall (grup labkita-praktikum), pengujian offline, serta 5 kali tolok ukur RAM dan waktu boot per versi.", bullet_style))

    story.append(Paragraph("1.5 Pembagian Tugas dan Kontribusi Anggota Kelompok", h2_style))
    story.append(Paragraph(
        "Sesuai dengan ketentuan rubrik final project, tim kelompok terdiri atas mahasiswa dengan pembagian peran yang terukur dan adil:",
        body_style
    ))

    team_data = [
        ["No", "Nama", "NPM", "Peran", "Rincian Tugas dan Kontribusi"],
        ["1", "Dafa Zahran", "257006111188", "Ketua Kelompok, Manajer Proyek & Integrasi (Build/Integrasi)", "Mengoordinasikan pembagian modul tim, pipeline build WSL (tools/build_v05.py, tag v0.5-iso) & arsip Cubic, regenerasi manifest md5sum & mastering ISO (labkita-linux-0.5-amd64.iso), manajemen repositori GitHub (https://github.com/luvices/labkita), dan keselarasan luaran tugas."],
        ["2", "Rafly Fauzi Pratama", "257006111152", "Pengembang Inti (Core Developer) & Toolchain", "Mengembangkan skrip kustomisasi Cubic (scripts/customize.sh), instalasi dan konfigurasi toolchain pemrograman (GCC, G++, Python, Geany), serta perancangan dan pengujian suite diagnostik labkita-check."],
        ["3", "Muhammad Ilham Rizky", "257006111154", "Sistem, Keamanan & Penguji Kualitas (Sys, Sec & QA)", "Merancang unit systemd labkita-runtime.service, otomasi skrip labkita-postinstall, isolasi izin 0700, pembatasan non-sudo, serta menjalankan pengujian tolok ukur (RAM free -m dan boot time systemd-analyze)."],
        ["4", "Vadien Athallah Lukman", "257006111160", "Pengembang Antarmuka, Dokumentasi & Media (UI/UX & Docs)", "Mendesain identitas visual (wallpaper SVG LabKita, konfigurasi dconf), modul materi panduan praktikum dan contoh kode (C & Python multiprocessing), penyusunan Laporan Proyek Akhir (Bab I-V PDF), slide presentasi (PPTX), dan naskah video demo."]
    ]
    t_team = Table(team_data, colWidths=[20, 85, 55, 105, 215])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.5),
        ('ALIGN', (0,0), (2,-1), 'CENTER'),
        ('ALIGN', (3,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t_team)
    story.append(PageBreak())

    # =========================================================================
    # BAB II: LANDASAN TEORI
    # =========================================================================
    story.append(Paragraph("BAB II. LANDASAN TEORI SISTEM OPERASI", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("2.1 Konsep Manajemen Proses dan Multiprocessing", h2_style))
    story.append(Paragraph(
        "Proses adalah sebuah program yang sedang dieksekusi di dalam memori utama oleh CPU. "
        "Di dalam sistem operasi modern berbasis Unix/Linux, setiap proses memiliki Process Identifier (PID) unik, status eksekusi (Running, Ready, Blocked), program counter, stack, serta ruang alamat memori sendiri. "
        "Penciptaan proses baru pada Linux menggunakan system call <code>fork()</code> yang menduplikasi address space proses induk (parent process) ke proses anak (child process). "
        "LabKita Linux menyertakan modul praktikum <code>processes.py</code> yang memanfaatkan modul <code>multiprocessing</code> Python untuk mendemonstrasikan pembagian beban komputasi secara paralel antar proses anak independen dengan PID berbeda.",
        body_style
    ))

    story.append(Paragraph("2.2 Manajemen Memori dan Virtual Filesystem (Tmpfs)", h2_style))
    story.append(Paragraph(
        "Memori utama (RAM) adalah sumber daya kritis yang dikelola oleh kernel melalui mekanisme virtual memory management dan paging. "
        "Linux menyediakan antarmuka <b>tmpfs</b> (temporary filesystem), yaitu sebuah virtual filesystem yang memetakan direktori tertentu langsung ke dalam memori RAM dinamis dan swap, alih-alih menyimpannya pada media disk persisten. "
        "Karakteristik utama tmpfs adalah kecepatan operasi I/O yang sangat tinggi mendekati throughput RAM fisik, serta sifatnya yang sepenuhnya volatil (seluruh data akan terhapus seketika saat daya sistem mati). "
        "LabKita Linux memanfaatkan konsep ini pada direktori <code>/run/labkita</code> yang dialokasikan sebagai ruang kerja sementara praktikum dengan atribut keamanan <i>sticky bit</i> (izin 1777), memungkinkan setiap praktikan menulis berkas sementara tanpa risiko memenuhi media disk persisten.",
        body_style
    ))

    story.append(Paragraph("2.3 Keamanan Sistem Operasi dan Privilege Separation", h2_style))
    story.append(Paragraph(
        "Keamanan sistem operasi bertumpu pada prinsip pembatasan hak istimewa (<i>Principle of Least Privilege</i>), yaitu setiap entitas pengguna hanya diberikan izin minimum yang diperlukan untuk menyelesaikan tugasnya. "
        "Pada Linux, hak akses dibedakan antara administrator sistem (super-user <code>root</code> dengan UID 0) dan pengguna biasa (unprivileged user dengan UID ≥ 1000). "
        "Mekanisme kontrol akses diskresioner (Discretionary Access Control - DAC) menerapkan bit perizinan: Read (r=4), Write (w=2), dan Execute (x=1) untuk pemilik (User), grup (Group), dan pengguna lain (Others). "
        "LabKita Linux menerapkan DAC ketat mode <code>0700</code> (<code>drwx------</code>) pada folder <code>/home/praktikan</code> guna mengisolasi pekerjaan mahasiswa, serta mengecualikan praktikan dari file konfigurasi <code>/etc/sudoers</code> untuk mencegah eskalasi hak akses.",
        body_style
    ))

    story.append(Paragraph("2.4 Inisialisasi Sistem dan Layanan Daemon (Systemd)", h2_style))
    story.append(Paragraph(
        "Setelah kernel Linux selesai melakukan bootstrap hardware, kernel akan mengeksekusi proses inisialisasi pertama yaitu <code>systemd</code> (PID 1). "
        "Systemd bertindak sebagai init system dan service manager yang mengatur siklus hidup daemon, dependensi layanan, serta target sistem (seperti <code>multi-user.target</code> dan <code>graphical.target</code>). "
        "Pada LabKita Linux, dibuat sebuah unit layanan kustom <code>labkita-runtime.service</code> bertipe <code>oneshot</code> yang diinisialisasi otomatis saat boot untuk memastikan direktori memori virtual <code>/run/labkita</code> selalu tercipta dengan kepemilikan dan hak akses yang benar sebelum pengguna login ke sesi grafis.",
        body_style
    ))

    story.append(Paragraph("2.5 Arsitektur Live CD dan OverlayFS", h2_style))
    story.append(Paragraph(
        "Distribusi Linux Live berjalan di atas media read-only (citra ISO 9660) menggunakan mekanisme kompresi <b>SquashFS</b> dan penyatuan sistem berkas <b>OverlayFS</b>. "
        "OverlayFS menggabungkan dua lapisan direktori: lapisan bawah (lowerdir) yang bersifat read-only terkompresi dari file ISO, dan lapisan atas (upperdir) berupa writable layer di dalam memori RAM (dikenal sebagai <code>/cow</code> atau Copy-on-Write). "
        "Setiap modifikasi berkas yang dilakukan oleh pengguna saat menjalankan sesi live hanya akan dicatat pada lapisan RAM tanpa mengubah berkas citra asli pada media penyimpanan fisik.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # BAB III: PERANCANGAN SISTEM
    # =========================================================================
    story.append(Paragraph("BAB III. PERANCANGAN SISTEM", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("3.1 Arsitektur LabKita Linux", h2_style))
    story.append(Paragraph(
        "LabKita Linux dirancang dengan struktur berlapis yang mengedepankan isolasi dan keandalan operasional:",
        body_style
    ))
    story.append(Paragraph("1. <b>Lapisan Kernel & Driver:</b> Kernel 7.0.0-43-generic (0.3/0.4/0.5 terinstal; 7.0.0-31-generic pada 0.1/0.2 bersih) dengan open-vm-tools.", bullet_style))
    story.append(Paragraph("2. <b>Lapisan Inisialisasi & Runtime:</b> Systemd yang memuat layanan <code>labkita-runtime.service</code> untuk mount tmpfs <code>/run/labkita</code>.", bullet_style))
    story.append(Paragraph("3. <b>Lapisan Toolchain Praktikum:</b> Compiler C/C++ (GCC/G++), Python 3, debugger, dan editor Geany di <code>/usr/bin</code>.", bullet_style))
    story.append(Paragraph("4. <b>Lapisan Keamanan & Pengguna:</b> <code>labkita-postinstall</code> mengatur akun non-sudo pada grup sistem <code>labkita-praktikum</code> (tanpa bentrok grup <code>labkita</code>), <code>0700</code>, & salinan <code>~/Dokumen/Panduan-LabKita</code>.", bullet_style))
    story.append(Paragraph("5. <b>Lapisan Antarmuka Pengguna:</b> GNOME Shell 46 via <code>dconf</code> untuk tema WhiteSur, wallpaper LabKita, dan dock aplikasi.", bullet_style))

    story.append(Paragraph("3.2 Alur Kerja Build ISO 0.5 (WSL) vs Riwayat Cubic (0.1–0.4)", h2_style))
    story.append(Paragraph(
        "Rilis <b>LabKita Linux 0.5</b> (dibangun dari tag <code>v0.5-iso</code>) menggunakan pipeline skrip WSL reproducible (<code>tools/build_v05.py</code>, resep Bisect #3, non-Cubic) yang menggantikan metode Cubic pada 0.1–0.4:",
        body_style
    ))
    story.append(Paragraph("• <b>Tahap 1 (ISO Source Verification):</b> Memverifikasi ISO sumber resmi Ubuntu 24.04.5 LTS Desktop amd64 via SHA256 (<code>4da4a0c9...</code>).", bullet_style))
    story.append(Paragraph("• <b>Tahap 2 (SquashFS Extraction):</b> Mengekstrak layer <code>minimal.squashfs</code> + <code>minimal.standard.squashfs</code> di WSL (mempertahankan layer live asli Ubuntu).", bullet_style))
    story.append(Paragraph("• <b>Tahap 3 (Chroot & LF Normalization):</b> Memasang 19 paket praktikum, menyalin <code>payload/</code> dengan normalisasi CRLF→LF, menyetel grup sistem <code>labkita-praktikum</code>, dan melabeli rilis <code>0.5</code>.", bullet_style))
    story.append(Paragraph("• <b>Tahap 4 (Metadata, md5sum & Mastering):</b> Menulis <code>.disk/info</code> <code>Ubuntu 24.04 LabKita 0.5 \"Noble Numbat\" - Release amd64 (20261122)</code>, meregenerasi <code>md5sum.txt</code> (1016/1016 OK), dan membangun ISO hybrid via <code>xorriso</code>.", bullet_style))

    story.append(Paragraph("3.3 Rancangan Antarmuka dan Pengalaman Pengguna (UI/UX)", h2_style))
    story.append(Paragraph(
        "Antarmuka versi 0.5 memakai tema open source <b>WhiteSur GTK/Icon/Cursors</b>, font <b>Inter</b>, tombol jendela di kiri, dock bawah terpusat, dan lokalisasi Bahasa Indonesia penuh (<code>id_ID.UTF-8</code>, <code>Asia/Jakarta</code>) tanpa aset proprietary Apple. Panduan lokal ditaruh di <code>~/Dokumen/Panduan-LabKita/</code> agar lolos AppArmor Firefox Snap.",
        body_style
    ))

    story.append(Paragraph("3.4 Spesifikasi Perangkat Keras dan Perangkat Lunak", h2_style))
    story.append(Paragraph("Tabel berikut merangkum spesifikasi lingkungan pengembangan dan target mesin virtual pengujian:", body_style))

    specs_data = [
        ["Komponen", "Lingkungan Host Pembuat", "Spesifikasi Target VM Pengujian"],
        ["Sistem Operasi", "Windows 11 + WSL2 Ubuntu", "LabKita 0.1/0.2 (7.0.0-31), 0.3/0.4/0.5 (7.0.0-43)"],
        ["Hypervisor", "VMware Workstation 25.0.1", "Virtual Machine Hardware v21"],
        ["Prosesor / vCPU", "Prosesor Host x86_64", "2 Core vCPU Virtual"],
        ["Kapasitas RAM", "16 GB RAM Host", "4.096 MB / 3.911 MiB Terbaca Linux"],
        ["Penyimpanan", "SSD NVMe Host", "40 GB Growable Virtual Disk (SCSI, Disk Kosong)"],
        ["Resolusi Layar", "1920 x 1080", "1280 x 800 (SVGA ScreenTarget)"]
    ]
    t_specs = Table(specs_data, colWidths=[95, 192, 193])
    t_specs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t_specs)
    story.append(PageBreak())

    # =========================================================================
    # BAB IV: IMPLEMENTASI DAN PENGUJIAN
    # =========================================================================
    story.append(Paragraph("BAB IV. IMPLEMENTASI DAN PENGUJIAN", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("4.1 Langkah-Langkah Implementasi", h2_style))
    story.append(Paragraph(
        "Implementasi proyek LabKita Linux diselesaikan melalui serangkaian tindakan terukur:",
        body_style
    ))
    story.append(Paragraph("1. <b>Penyusunan Kit Payload:</b> Skrip <code>tools/pack.py</code> mengemas skrip kustomisasi, konfigurasi paket, unit systemd, aset SVG, panduan non-dotfolder, dan skrip pengujian menjadi arsip <code>dist/labkita-kit.tar.gz</code>.", bullet_style))
    story.append(Paragraph("2. <b>Eksekusi Kustomisasi WSL & Normalisasi LF:</b> Pipeline <code>tools/build_v05.py</code> (resep Bisect #3, non-Cubic, dibangun dari tag <code>v0.5-iso</code>) menyetel grup sistem <code>labkita-praktikum</code>, menormalisasi CRLF→LF seluruh skrip, melabeli metadata <code>0.5</code>, menulis <code>.disk/info</code> berformat kutip <code>Ubuntu 24.04 LabKita 0.5 \"Noble Numbat\"</code>, dan meregenerasi <code>md5sum.txt</code> (1016/1016 OK pada ISO terpasang loop).", bullet_style))
    story.append(Paragraph("3. <b>Mastering ISO 0.5:</b> Xorriso menghasilkan berkas <code>labkita-linux-0.5-amd64.iso</code> berukuran 6.643.179.520 bytes (~6,19 GiB / 6,64 GB) dengan SHA256 terverifikasi (Linux &amp; Windows Get-FileHash identik) <code>d0dae277d140decd3e1ecaff9b908c551109a10efd069b1472acd34b046f5f1c</code> dan MD5 <code>b73178250b61cdfd900e3a3f8bdca660</code>.", bullet_style))
    story.append(Paragraph("4. <b>Pengujian Mesin Virtual (VM Test):</b> VM uji bersih <code>build/test-vm/labkita-test.vmx</code> dengan disk kosong 40 GB diinstal ulang penuh secara bergantian untuk versi 0.1, 0.2, 0.3, 0.4, dan 0.5 guna menjamin perbandingan 5x run per versi yang setara.", bullet_style))

    story.append(Paragraph("4.2 Skenario dan Hasil Pengujian Fungsional", h2_style))
    story.append(Paragraph("Pengujian fungsional, integritas media ISO, live autologin, instalasi GUI penuh, dan keamanan dijalankan nyata pada VM uji untuk rilis 0.5. Hasil pengujian dicatat apa adanya:", body_style))

    test_matrix = [
        ["No", "Skenario Uji", "Hasil yang Diharapkan", "Hasil Aktual di VM 0.5", "Status"],
        ["1", "Integritas md5sum.txt & Casper", "Seluruh berkas manifest valid", "Loop ISO: 1016/1016 OK (exit 0; kecuali boot.catalog & eltorito.img)", "LULUS"],
        ["2", "GRUB & Live Autologin", "Boot ID 0.5 langsung desktop tanpa GIS", "casper.log bersih; user ubuntu (uid=1000) autologin langsung tanpa GIS", "LULUS"],
        ["3", "Installer GUI (Prosedur Resmi)", "Wizard grafis selesai instalasi ke disk", "LULUS PENUH s.d. 'Instalasi selesai' (kontras dengan build Cubic 0.1–0.4 yang gagal GUI)", "LULUS"],
        ["4", "Installer TUI (Cadangan)", "Jalur teks tersedia sebagai cadangan", "Tersedia via subiquity.cmd.tui (dipakai sebagai prosedur utama arsip 0.1–0.4)", "CADANGAN"],
        ["5", "Konsistensi Metadata 0.5", "Seluruh label & dialog tampil 0.5", "/etc/os-release, /etc/labkita-release, sambutan, & panduan tampil 0.5", "LULUS"],
        ["6", "Desktop WhiteSur & ID", "WhiteSur, dock tengah, UI Indonesia", "Tema WhiteSur, tombol kiri, dock bawah, wallpaper LabKita, & UI Bahasa Indonesia", "LULUS"],
        ["7", "Suite labkita-check (Snap)", "Menguji semua komponen & baca Firefox Snap", "SEMUA PEMERIKSAAN LULUS termasuk ~/Dokumen/Panduan-LabKita & AppArmor OK", "LULUS"],
        ["8", "Peluncur labkita-guide", "Panduan terbuka di Firefox Snap", "Firefox Snap merender ~/Dokumen/Panduan-LabKita/index.html (badge 0.5)", "LULUS"],
        ["9", "Postinstall & Grup Praktikum", "Akun praktikan grup labkita-praktikum", "sudo labkita-postinstall praktikan [SUKSES]; id praktikan tanpa sudo & tanpa grup labkita", "LULUS"],
        ["10", "Isolasi 0700 & Tmpfs", "Izin 0700 & /run/labkita sticky bit 1777", "stat /home/praktikan = 700; labkita-runtime aktif & /run/labkita mode 1777", "LULUS"],
        ["11", "Kompilasi Offline C/Python", "C, Python, & fork jalan offline", "labkita-check memverifikasi eksekusi Python, fork, & kompilasi C lulus", "LULUS"]
    ]
    t_test = Table(test_matrix, colWidths=[20, 95, 110, 205, 50])
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.5),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (4,0), (4,-1), 'CENTER'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 7),
        ('FONTNAME', (4,1), (4,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]
    for r_idx, row in enumerate(test_matrix[1:], start=1):
        st = row[4]
        if st == "GAGAL":
            clr = colors.HexColor("#DC2626")
        elif st in ("PARSIAL", "LULUS*", "CADANGAN"):
            clr = colors.HexColor("#D97706")
        else:
            clr = colors.HexColor("#16A34A")
        style_cmds.append(('TEXTCOLOR', (4, r_idx), (4, r_idx), clr))
    t_test.setStyle(TableStyle(style_cmds))
    story.append(t_test)
    story.append(Paragraph("<i>Catatan jujur: build ke-2 0.5 sempat mengalami error CRLF ('python3\\r'/'bash\\r') pada skrip payload; diperbaiki via .gitattributes & normalisasi LF pada build final d0dae277... yang lulus seluruh pemeriksaan di atas.</i>", caption_style))
    story.append(Spacer(1, 8))

    # Evidence Images (100% genuine VM captures)
    story.append(Paragraph("Bukti Tangkapan Layar Pengujian Nyata 0.5 (Capture VM Asli):", h3_style))
    ev_dir = Path("docs/evidence")

    img1_path = str(ev_dir / "0.5-07-gui-install-complete.png")
    img2_path = str(ev_dir / "0.5-12-os-release-and-labkita-check.png")
    img3_path = str(ev_dir / "0.5-14-labkita-guide-firefox.png")
    img4_path = str(ev_dir / "0.5-13-postinstall-praktikan.png")

    if os.path.exists(img1_path) and os.path.exists(img2_path) and os.path.exists(img3_path) and os.path.exists(img4_path):
        img_table_data = [
            [Image(img1_path, width=230, height=144), Image(img2_path, width=230, height=144)],
            [Paragraph("Gambar 4.1: Installer GUI 0.5 Selesai Penuh ('Instalasi selesai')", caption_style),
             Paragraph("Gambar 4.2: labkita-check 0.5 SEMUA LULUS (Termasuk Firefox Snap AppArmor OK)", caption_style)],
            [Image(img3_path, width=230, height=144), Image(img4_path, width=230, height=144)],
            [Paragraph("Gambar 4.3: Panduan LabKita Linux 0.5 Terbuka Normal di Firefox Snap", caption_style),
             Paragraph("Gambar 4.4: labkita-postinstall praktikan Grup labkita-praktikum & Izin 0700", caption_style)]
        ]
        t_img = Table(img_table_data, colWidths=[240, 240])
        t_img.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
        story.append(t_img)
        story.append(Spacer(1, 10))

    story.append(Paragraph("4.3 Pengukuran Kinerja dan Tolok Ukur Empiris (0.1–0.5, 5x per Versi)", h2_style))
    story.append(Paragraph(
        "Pengukuran dilakukan ulang pada VM yang sama (RAM 4.096 MB / 3.911 MiB terdeteksi, 2 vCPU, disk kosong 40 GB SCSI yang diinstal ulang bersih untuk setiap versi), sebanyak <b>5 kali cold boot bersih per versi</b> (settle 20 detik setelah desktop siap). "
        "<b>Variabel pembeda kernel:</b> 0.1 dan 0.2 bersih memakai kernel Linux <code>7.0.0-31-generic</code>, sedangkan 0.3, 0.4, dan 0.5 memakai <code>7.0.0-43-generic</code>.",
        body_style
    ))

    # Benchmark Table
    bench_data = [
        ["Parameter Uji", "LabKita 0.1 (5x)\n[7.0.0-31]", "LabKita 0.2 (5x)\n[7.0.0-31]", "LabKita 0.3 (5x)\n[7.0.0-43]", "LabKita 0.4 (5x)\n[7.0.0-43]", "LabKita 0.5 (5x)\n[7.0.0-43]"],
        ["Memori Used\n(free -m, MiB)", "Avg: 1.038,2\n(1.016–1.056)\nAvail: 2.872,6", "Avg: 1.068,2\n(1.058–1.080)\nAvail: 2.842,2", "Avg: 1.058,2\n(1.046–1.067)\nAvail: 2.852,0", "Avg: 1.062,6\n(1.043–1.075)\nAvail: 2.847,8", "1041/1039/1049/\n1054/1031 MiB\nAvg: 1.042,8 MiB\n(1.031–1.054)\nAvail: 2.867,6"],
        ["Waktu Boot Total\n(systemd-analyze)", "Avg: 8,460s\n(8,359–8,676s)\nK 3,205+U 5,255", "Avg: 9,317s\n(9,072–9,458s)\nK 3,330+U 5,987", "Avg: 8,808s\n(8,460–9,014s)\nK 3,197+U 5,610", "Avg: 9,185s\n(8,520–10,713s)\nK 3,363+U 5,822", "9,515/9,444/9,370/\n8,349/8,502 s\nAvg: 9,036s\n(8,349–9,515s)\nK 3,287+U 5,749"],
        ["graphical.target\n(userspace)", "Avg: 5,180s\n(5,084–5,371)", "Avg: 5,918s\n(5,786–6,057)", "Avg: 5,532s\n(5,215–5,717)", "Avg: 5,779s\n(5,202–6,823)", "Avg: 5,686s\n(5,132–6,100)"],
        ["Layanan Terlama", "plymouth: 2,18–2,50\nsnapd.seed: ~1,02", "plymouth: 2,61–2,85\nsnapd.seed: ~1,12", "plymouth: 2,21–2,70\nsnapd.seed: ~1,05", "plymouth: 2,21–3,04\nsnapd.seed: 1,06–1,16", "plymouth: 2,10–2,87\nsnapd.seed: 1,06–1,24"]
    ]
    t_bench = Table(bench_data, colWidths=[68, 80, 80, 80, 80, 92])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 6.5),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 6.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.0),
        ('TOPPADDING', (0,0), (-1,-1), 3.0),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Kesimpulan Empiris Benchmark (Tanpa Klaim Lebih Ringan/Cepat):</b> Rentang konsumsi RAM 0.5 (1.031–1.054 MiB; rata-rata 1.042,8 MiB; sisa rata-rata 2.867,6 MiB) bertumpang tindih dengan 0.1 (1.016–1.056 MiB), 0.3 (1.046–1.067 MiB), dan 0.4 (1.043–1.075 MiB). Rentang waktu boot 0.5 (8,349–9,515s; rata-rata 9,036s) juga bertumpang tindih dengan 0.1–0.4, ditambah perbedaan kernel (<code>7.0.0-43-generic</code> vs <code>7.0.0-31-generic</code>). Oleh karena itu, <b>tidak ada perbedaan yang dapat dibuktikan</b> antarversi.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.4 Pembahasan Temuan Teknis: Bisect #4, ProductService &amp; Pemulihan GUI 0.5", h2_style))
    story.append(Paragraph(
        "Rangkaian eksperimen kontrol, bisect #1–#4, uji ISO 0.4, dan rilis 0.5 WSL menghasilkan tiga temuan teknis utama:",
        body_style
    ))
    story.append(Paragraph(
        "1. <b>Penyebab Gagal Autologin (Bisect #1–#4 &amp; Fix 0.4):</b> Bisect #4 membuktikan bentrok <code>.disk/info</code> + <code>groupadd --system labkita</code> menyebabkan <code>casper.log: fatal: The group 'labkita' already exists.</code> dan jatuh ke <code>gnome-initial-setup</code>. Perubahan grup menjadi <code>labkita-praktikum</code> pada 0.4 memulihkan autologin.",
        body_style
    ))
    story.append(Paragraph(
        "2. <b>Penyebab Kegagalan Installer GUI &amp; Pemulihan di 0.5 (Build WSL vs Cubic):</b> Seluruh ISO build Cubic <code>0.1</code>–<code>0.4</code> gagal pada <code>ubuntu-desktop-bootstrap</code>, sedangkan resep WSL (Bisect #3) berhasil. Penelusuran <code>strace</code> &amp; sumber <code>ubuntu-desktop-provision</code> menunjukkan <code>ProductService._extractIsoInfo()</code> memanggil <code>isoName.substring(0, isoName.indexOf('\"') - 1)</code> yang melempar <code>RangeError</code> tak tertangkap bila <code>.disk/info</code> tidak memiliki tanda kutip. Di LabKita 0.5 (<code>tools/build_v05.py</code>, tag <code>v0.5-iso</code>), format <code>.disk/info</code> = <code>Ubuntu 24.04 LabKita 0.5 \"Noble Numbat\" - Release amd64 (20261122)</code> memulihkan penulisan <code>telemetry</code> dan membuat installer GUI berjalan penuh hingga selesai.",
        body_style
    ))
    story.append(Paragraph(
        "3. <b>Prosedur Instalasi Resmi 0.5 = GUI, TUI Sebagai Cadangan:</b> Karena installer GUI berfungsi penuh pada build WSL 0.5, prosedur instalasi resmi ditetapkan ke <b>installer GUI <code>ubuntu-desktop-bootstrap</code></b>, sedangkan <code>subiquity.cmd.tui</code> menjadi cadangan (dan tetap prosedur utama arsip 0.1–0.4). Faktor lingkungan Cubic di luar <code>.disk/info</code> belum diisolasi ulang di Cubic.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # BAB V: PENUTUP
    # =========================================================================
    story.append(Paragraph("BAB V. PENUTUP", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("5.1 Kesimpulan", h2_style))
    story.append(Paragraph(
        "Berdasarkan hasil perancangan, implementasi, dan pengujian empiris pascainstalasi yang telah dilakukan, dapat disimpulkan bahwa:",
        body_style
    ))
    story.append(Paragraph("1. <b>Keluaran Produk 0.5 Tercapai (Tag <code>v0.5-iso</code>):</b> Berkas citra bootable <code>labkita-linux-0.5-amd64.iso</code> (~6,19 GiB, SHA256 <code>d0dae277...46f5f1c</code>) berhasil dibangun via <code>tools/build_v05.py</code> (WSL, resep Bisect #3), lolos verifikasi <code>md5sum</code> 1016/1016 OK, autologin live <code>ubuntu</code> lancar, serta terinstal penuh melalui <b>installer GUI normal</b>.", bullet_style))
    story.append(Paragraph("2. <b>Autologin &amp; Installer GUI Pulih + Fitur Praktikum Terbukti:</b> Panduan 0.5 di <code>~/Dokumen/Panduan-LabKita</code> terbaca Firefox Snap, <code>labkita-check</code> lulus seluruhnya, <code>labkita-postinstall</code> grup <code>labkita-praktikum</code> berjalan tanpa error, dan label 0.5 tampil konsisten.", bullet_style))
    story.append(Paragraph("3. <b>Visi Pemrograman Offline &amp; Isolasi Terpenuhi:</b> Pengujian memverifikasi compiler GCC, Python 3, multiprocessing, isolasi <code>0700</code>, akun non-sudo (grup <code>labkita-praktikum</code>), serta tmpfs <code>/run/labkita</code> <code>1777</code> aktif.", bullet_style))
    story.append(Paragraph("4. <b>Integritas Data Empiris 5x Ukur &amp; Variabel Kernel:</b> Dalam 5x pengukuran per versi di VM identik, konsumsi RAM 0.5 rata-rata tercatat 1.042,8 MiB (1.031–1.054 MiB) dan waktu boot rata-rata 9,036s (8,349–9,515s), bertumpang tindih dengan 0.1–0.4 serta terdapat perbedaan kernel (<code>7.0.0-31-generic</code> pada 0.1/0.2 vs <code>7.0.0-43-generic</code> pada 0.3/0.4/0.5) sehingga tidak ada perbedaan yang dapat dibuktikan.", bullet_style))

    story.append(Paragraph("5.2 Keterbatasan Terbuka &amp; Perbandingan Build Cubic vs WSL", h2_style))
    story.append(Paragraph(
        "Berdasarkan pengujian nyata pada rilis 0.1–0.5, catatan teknis berikut tetap dilaporkan secara jujur:",
        body_style
    ))
    story.append(Paragraph("• <b>Perbedaan Lapisan Cubic (0.1–0.4) vs WSL (0.5):</b> Installer GUI gagal pada seluruh build Cubic 0.1–0.4 dan berfungsi penuh pada build WSL 0.5. Meski penyebab langsung kegagalan <code>ProductService</code> (<code>.disk/info</code> tanpa tanda kutip) telah teridentifikasi dan diatasi di 0.5, isolasi komponen Cubic lain (seperti state snapd di <code>custom-live</code>) belum diuji ulang di Cubic karena pipeline 0.5 dibangun melalui WSL.", bullet_style))
    story.append(Paragraph("• <b>Flag Tmpfs Noexec:</b> Partisi sistem <code>/run</code> tetap berflag <code>noexec</code> sehingga biner hasil kompilasi C praktikan dieksekusi dari <code>~/Praktikum</code>, sedangkan <code>/run/labkita</code> dipakai sebagai ruang scratch data temporer.", bullet_style))

    story.append(Paragraph("5.3 Saran Pengembangan Rilis Selanjutnya (0.6+)", h2_style))
    story.append(Paragraph(
        "Untuk pengembangan rilis berikutnya, disarankan perbaikan terfokus berikut:",
        body_style
    ))
    story.append(Paragraph("1. <b>Pipeline Build Berbasis Container CI:</b> Membungkus <code>tools/build_v05.py</code> ke dalam Dockerfile/GitHub Actions atau LXC agar build reproducible tidak bergantung pada WSL lokal.", bullet_style))
    story.append(Paragraph("2. <b>Penyelarasan Tema Dock WhiteSur:</b> Memeriksa ulang cache ikon tema WhiteSur agar seluruh ikon favorit dock tampil konsisten.", bullet_style))
    story.append(Paragraph("3. <b>Opsi Desktop Lebih Ringan:</b> Mengevaluasi XFCE4 atau Openbox bila distro akan dipasang di komputer laboratorium dengan RAM terbatas.", bullet_style))
    story.append(Paragraph("4. <b>Mode Ujian Lab (Kiosk Profile):</b> Menyediakan profil login khusus yang mengunci jaringan dan antarmuka saat sesi ujian praktikum.", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # DAFTAR PUSTAKA DAN LAMPIRAN
    # =========================================================================
    story.append(Paragraph("DAFTAR PUSTAKA DAN LAMPIRAN", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Daftar Pustaka", h2_style))
    refs = [
        "Canonical Ltd. (2024). <i>Ubuntu 24.04 LTS (Noble Numbat) Release Notes & Documentation</i>. Diakses dari: https://ubuntu.com/download/desktop",
        "Love, Robert. (2013). <i>Linux System Programming: Talking Directly to the Kernel and C Library</i> (2nd ed.). O'Reilly Media.",
        "Poettering, Lennart. (2023). <i>systemd System and Service Manager Manual</i>. freedesktop.org.",
        "Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). <i>Operating System Concepts</i> (10th ed.). John Wiley & Sons.",
        "Singh, PJ. (2024). <i>Cubic (Custom Ubuntu ISO Creator) Documentation & Terminal Page</i>. Diakses dari: https://github.com/PJ-Singh-001/Cubic",
        "Tanenbaum, A. S., & Bos, H. (2015). <i>Modern Operating Systems</i> (4th ed.). Pearson."
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('Ref_Custom', parent=body_style, leftIndent=20, firstLineIndent=-15, spaceAfter=4)))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Lampiran 1: Tautan Repositori Kode Sumber dan Berkas ISO", h2_style))
    story.append(Paragraph(
        "• <b>Repositori GitHub Resmi:</b> <font color='#1E3A8A'><u>https://github.com/luvices/labkita</u></font> (memuat skrip build WSL <code>tools/build_v05.py</code>, kustomisasi, paket, dokumen pengujian, generator laporan, dan bukti tangkapan layar; rilis 0.5 dibangun dari tag <code>v0.5-iso</code>).<br/>"
        "• <b>Berkas Citra ISO Resmi (0.5):</b> <code>labkita-linux-0.5-amd64.iso</code> (Ukuran: 6.643.179.520 bytes / ~6,19 GiB / 6,64 GB).<br/>"
        "• <b>Tautan Unduhan ISO 0.5:</b> <code>[LINK-DRIVE-ISO-0.5]</code> *(arsip ISO 0.4 Cubic tetap tersedia di Google Drive)*<br/>"
        "• <b>Verifikasi SHA256 (0.5):</b> <code>d0dae277d140decd3e1ecaff9b908c551109a10efd069b1472acd34b046f5f1c</code><br/>"
        "• <b>Verifikasi MD5 (0.5):</b> <code>b73178250b61cdfd900e3a3f8bdca660</code><br/>"
        "• <b>Metode Build 0.5:</b> Skrip WSL <code>tools/build_v05.py</code> (resep Bisect #3, tag <code>v0.5-iso</code>)",
        body_style
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Lampiran 2: Naskah dan Tautan Video Demonstrasi (3–5 Menit)", h2_style))
    story.append(Paragraph(
        "Sesuai ketentuan Bagian 5 Poin 4, video demonstrasi berdurasi 4 menit 30 detik disiapkan dengan struktur alur kerja: "
        "(1) Pembukaan, booting GRUB 0.5 Bahasa Indonesia, autologin live <code>ubuntu</code> &amp; installer GUI penuh hingga <i>Instalasi selesai</i> (plus catatan arsip Cubic 0.1–0.4 &amp; TUI cadangan), (2) Desktop 0.5 terinstal (sambutan 0.5, tema WhiteSur, dock, os-release), "
        "(3) Eksekusi labkita-check SEMUA LULUS (termasuk uji baca sandbox Firefox Snap AppArmor OK) dan pembukaan panduan 0.5 di Firefox Snap, "
        "(4) Pembuktian offline total tanpa jaringan (GCC di ~/Praktikum &amp; multiprocessing Python), (5) Eksekusi labkita-postinstall (grup labkita-praktikum), isolasi folder 0700 dan akun praktikan non-sudo, "
        "serta (6) Perbandingan empiris 5x pengukuran RAM free -m dan boot time systemd-analyze (0.1–0.5 terinstal beserta variabel kernel).<br/>"
        "<i>Tautan Video Demo (YouTube Unlisted / Google Drive):</i> [Tautan disematkan oleh mahasiswa]",
        body_style
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Lampiran 3: Pernyataan Kejujuran Akademik dan Penggunaan AI", h2_style))
    story.append(Paragraph(
        "Sesuai Ketentuan Akademik Poin 8.2 dokumen pedoman Final Project Sistem Operasi Ganjil 2026/2027: "
        "<i>'Alat bantu AI generatif boleh digunakan sebagai pendukung, dengan mencantumkan bagian yang dibantu AI di laporan. Setiap anggota tetap harus memahami dan mampu menjelaskan seluruh bagian produk.'</i><br/><br/>"
        "Dengan ini kami menyatakan secara transparan kontribusi alat bantu kecerdasan buatan (AI coding assistant) dalam proyek ini meliputi: "
        "(a) Membantu otomatisasi eksekusi & capture layar VMware Workstation via protokol VNC (tanpa menyimpan kata sandi di kode), "
        "(b) Membantu penyusunan skrip pengujian dan penghitungan rata-rata benchmark, serta "
        "(c) Membantu pemformatan ulang dokumen laporan PDF dan slide presentasi berdasarkan data pengukuran riil.<br/>"
        "Seluruh perancangan konsep sistem operasi (manajemen memori, hak akses Linux DAC, pemisahan hak istimewa, pembuatan layanan systemd, dan analisis tolok ukur empiris) dipelajari, diuji, dipahami secara mendalam, dan dapat dipertanggungjawabkan sepenuhnya oleh setiap anggota tim pada sesi presentasi dan tanya jawab UAS.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report PDF built successfully: {filename}")

if __name__ == "__main__":
    build_pdf()
