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
        self.drawString(54, 800, "Laporan Final Project Sistem Operasi — LabKita Linux 0.2")
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
    story.append(Paragraph("LABKITA LINUX 0.2", title_style))
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
        ["", "3.2 Alur Kerja Pembuatan ISO dengan Cubic", "6"],
        ["", "3.3 Rancangan Antarmuka dan Pengalaman Pengguna (UI/UX)", "6"],
        ["", "3.4 Spesifikasi Perangkat Keras dan Perangkat Lunak", "6"],
        ["BAB IV", "IMPLEMENTASI DAN PENGUJIAN", "7"],
        ["", "4.1 Langkah-Langkah Implementasi", "7"],
        ["", "4.2 Skenario dan Hasil Pengujian Fungsional", "7"],
        ["", "4.3 Pengukuran Kinerja dan Tolok Ukur Empiris (0.1 vs 0.2 Terinstal)", "8"],
        ["", "4.4 Pembahasan Temuan Teknis: Kegagalan Nyata Selama Audit", "9"],
        ["BAB V", "PENUTUP", "10"],
        ["", "5.1 Kesimpulan", "10"],
        ["", "5.2 Keterbatasan dan Kegagalan Terbuka pada Rilis 0.2", "10"],
        ["", "5.3 Saran Pengembangan Rilis Selanjutnya (LabKita Linux 0.3)", "10"],
        ["DAFTAR PUSTAKA DAN LAMPIRAN", "", "11"],
        ["", "Daftar Pustaka", "11"],
        ["", "Lampiran 1: Tautan Repositori Kode Sumber dan Berkas ISO", "11"],
        ["", "Lampiran 2: Naskah dan Tautan Video Demonstrasi (3-5 Menit)", "11"],
        ["", "Lampiran 3: Pernyataan Kejujuran Akademik dan Penggunaan AI", "11"]
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
        "Ruang lingkup pengerjaan LabKita Linux versi 0.2 dibatasi pada:",
        body_style
    ))
    story.append(Paragraph("1. Basis distribusi menggunakan Ubuntu Desktop 24.04.5 LTS (Noble Numbat) arsitektur x86_64 dengan kernel Linux 7.0.0-43-generic pada sistem 0.2 terinstal (dibanding 7.0.0-31-generic pada versi 0.1).", bullet_style))
    story.append(Paragraph("2. Perangkat lunak pemrograman mencakup GCC 13.3.0, G++ 13.3.0, Make 4.3, Python 3.12.3, Geany 2.0, Git 2.43, Nano, dan pustaka manpages-dev.", bullet_style))
    story.append(Paragraph("3. Kustomisasi sistem dilakukan melalui Cubic (Custom Ubuntu ISO Creator) dengan skrip kustomisasi bash termonitor.", bullet_style))
    story.append(Paragraph("4. Pengujian dilakukan secara empiris pada hypervisor VMware Workstation 25 mencakup uji diagnostik mandiri (labkita-check), pengujian offline tanpa jaringan, serta tolok ukur RAM dan waktu boot.", bullet_style))

    story.append(Paragraph("1.5 Pembagian Tugas dan Kontribusi Anggota Kelompok", h2_style))
    story.append(Paragraph(
        "Sesuai dengan ketentuan rubrik final project, tim kelompok terdiri atas mahasiswa dengan pembagian peran yang terukur dan adil:",
        body_style
    ))

    team_data = [
        ["No", "Nama", "NPM", "Peran", "Rincian Tugas dan Kontribusi"],
        ["1", "Dafa Zahran", "257006111188", "Ketua Kelompok, Manajer Proyek & Integrasi (Build/Integrasi)", "Mengoordinasikan pembagian modul tim, pipeline build Cubic, mastering berkas ISO (labkita-linux-0.2-amd64.iso), manajemen repositori GitHub (https://github.com/luvices/labkita), dan keselarasan luaran tugas."],
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
    story.append(Paragraph("1. <b>Lapisan Kernel & Driver:</b> Kernel Linux 7.0.0-43-generic (0.2 terinstal) dengan modul open-vm-tools terintegrasi untuk mendukung display scaling SVGA dan integrasi hypervisor.", bullet_style))
    story.append(Paragraph("2. <b>Lapisan Inisialisasi & Runtime:</b> Systemd init manager yang memuat layanan <code>labkita-runtime.service</code> dan mengelola mounting tmpfs.", bullet_style))
    story.append(Paragraph("3. <b>Lapisan Toolchain Praktikum:</b> Koleksi compiler C/C++ (GCC/G++), interpreter Python 3, debugger, dan editor Geany yang sepenuhnya mandiri di <code>/usr/bin</code>.", bullet_style))
    story.append(Paragraph("4. <b>Lapisan Keamanan & Pengguna:</b> Skrip pascainstalasi <code>labkita-postinstall</code> yang mengatur pembuatan akun non-sudo dan hak akses folder <code>0700</code>.", bullet_style))
    story.append(Paragraph("5. <b>Lapisan Antarmuka Pengguna:</b> GNOME Shell 46 yang dikonfigurasi melalui skema <code>dconf</code> untuk menampilkan wallpaper resmi LabKita dan pin dock aplikasi esensial.", bullet_style))

    story.append(Paragraph("3.2 Alur Kerja Pembuatan ISO dengan Cubic", h2_style))
    story.append(Paragraph(
        "Pembuatan berkas ISO kustom LabKita Linux memanfaatkan perangkat lunak <b>Cubic (Custom Ubuntu ISO Creator)</b>. "
        "Alur kerja integrasi terdiri atas tahapan berurutan berikut:",
        body_style
    ))
    story.append(Paragraph("• <b>Tahap 1 (ISO Source Verification):</b> Memverifikasi berkas sumber ISO resmi Ubuntu 24.04.5 LTS Desktop amd64 menggunakan checksum SHA256 (<code>4da4a0c9...</code>).", bullet_style))
    story.append(Paragraph("• <b>Tahap 2 (SquashFS Extraction):</b> Cubic mengekstrak berkas <code>filesystem.squashfs</code> ke dalam lingkungan virtualisasi container <code>systemd-nspawn</code>.", bullet_style))
    story.append(Paragraph("• <b>Tahap 3 (Chroot Customization):</b> Kit kustomisasi <code>labkita-kit.tar.gz</code> disalin ke lingkungan chroot. Skrip <code>customize.sh</code> dijalankan untuk menginstal paket, menyalin payload aset, mengaktifkan systemd service, dan menyusun template pengguna di <code>/etc/skel</code>.", bullet_style))
    story.append(Paragraph("• <b>Tahap 4 (Filesystem Recompression & ISO Mastering):</b> Cubic mengompresi ulang root filesystem menjadi SquashFS dengan kompresi gzip/xz, memperbarui kernel initrd, dan mengeksekusi <code>xorriso</code> untuk memproduksi citra bootable hybrid ISO.", bullet_style))

    story.append(Paragraph("3.3 Rancangan Antarmuka dan Pengalaman Pengguna (UI/UX)", h2_style))
    story.append(Paragraph(
        "Antarmuka grafis versi 0.2 dirancang bergaya modern menyerupai macOS tanpa aset proprietary Apple, dipadukan dengan lokalisasi penuh Bahasa Indonesia (<code>id_ID.UTF-8</code>, zona waktu <code>Asia/Jakarta</code>). "
        "Identitas visual diwujudkan melalui wallpaper gradien minimalis orisinal LabKita Linux. "
        "Panel dock (Dash-to-Dock) diposisikan terpusat di bagian bawah layar dengan tema GTK <b>WhiteSur</b>, set ikon & kursor WhiteSur, font <b>Inter</b>, serta posisi tombol jendela di sebelah kiri (<code>close,minimize,maximize:</code>).",
        body_style
    ))

    story.append(Paragraph("3.4 Spesifikasi Perangkat Keras dan Perangkat Lunak", h2_style))
    story.append(Paragraph("Tabel berikut merangkum spesifikasi lingkungan pengembangan dan target mesin virtual pengujian:", body_style))

    specs_data = [
        ["Komponen", "Lingkungan Host Pembuat", "Spesifikasi Target VM Pengujian"],
        ["Sistem Operasi", "Windows 11 64-bit", "LabKita 0.1 (7.0.0-31) & 0.2 (7.0.0-43)"],
        ["Hypervisor", "VMware Workstation 25.0.1", "Virtual Machine Hardware v21"],
        ["Prosesor / vCPU", "Prosesor Host x86_64", "2 Core vCPU Virtual"],
        ["Kapasitas RAM", "16 GB RAM Host", "4.096 MB / 3.911 MiB Terbaca Linux"],
        ["Penyimpanan", "SSD NVMe Host", "40 GB Growable Virtual Disk (SCSI, Disk Kosong)"],
        ["Resolusi Layar", "1920 x 1080", "1280 x 800 (SVGA ScreenTarget)"]
    ]
    t_specs = Table(specs_data, colWidths=[100, 190, 190])
    t_specs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 7.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
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
    story.append(Paragraph("1. <b>Penyusunan Kit Payload:</b> Skrip <code>tools/pack.py</code> mengemas skrip kustomisasi, konfigurasi paket, unit systemd, aset SVG, panduan lokal, dan skrip pengujian menjadi arsip <code>dist/labkita-kit.tar.gz</code>.", bullet_style))
    story.append(Paragraph("2. <b>Eksekusi Kustomisasi di Cubic:</b> Kit diekstrak pada container Cubic dan dieksekusi menggunakan <code>bash scripts/customize.sh --cubic</code>. Skrip menginstal paket build-essential, gcc, g++, python3, python3-doc, geany, git, man-db, manpages-dev, xdg-utils, dan dconf-cli, lalu menyusun profil <code>/etc/skel/Praktikum</code>.", bullet_style))
    story.append(Paragraph("3. <b>Mastering ISO:</b> Xorriso menghasilkan berkas <code>labkita-linux-0.2-amd64.iso</code> berukuran 6.519.777.280 bytes (~6.07 GiB / 6.52 GB) dengan SHA256 terverifikasi <code>ae6391a26d3497cb9d9aed4d9e967352e46adfd630202ac47c58b149d8000d19</code>.", bullet_style))
    story.append(Paragraph("4. <b>Pengujian Mesin Virtual (VM Test):</b> Dibuat VM uji bersih <code>build/test-vm/labkita-test.vmx</code> dengan disk kosong 40 GB yang diinstal ulang penuh untuk versi 0.1 dan 0.2 secara bergantian. Hypervisor dikonfigurasi dengan VNC port 5900 untuk otomasi & capture layar nyata VM.", bullet_style))

    story.append(Paragraph("4.2 Skenario dan Hasil Pengujian Fungsional", h2_style))
    story.append(Paragraph("Pengujian fungsional, instalasi disk kosong, dan keamanan dijalankan secara nyata pada VM uji. Kegagalan dan kendala yang ditemukan dilaporkan apa adanya:", body_style))

    test_matrix = [
        ["No", "Skenario Uji", "Hasil yang Diharapkan", "Hasil Aktual di VM", "Status"],
        ["1", "GRUB & Live Autologin", "Boot ID langsung masuk desktop", "GRUB berbahasa Indonesia; live gagal autologin 'labkita', masuk gnome-initial-setup", "GAGAL"],
        ["2", "Installer GUI Bootstrap", "Wizard grafis selesai instalasi", "Gagal di awal dialog 'Ada yang salah' (casper-md5check & snap info 500)", "GAGAL"],
        ["3", "Instalasi Disk (TUI)", "Instalasi penuh ke /dev/sda 40 GB", "Berhasil via fallback subiquity.cmd.tui hingga reboot ke OS terinstal", "LULUS*"],
        ["4", "Desktop WhiteSur & ID", "WhiteSur, dock tengah, UI Indonesia", "Tema WhiteSur, tombol kiri, dock bawah tengah, top bar & Berkas bhs Indonesia", "LULUS"],
        ["5", "Suite labkita-check", "21 cek terinstal lulus", "21/21 [LULUS] di sistem terinstal (hanya cek keberadaan file, bukan browser)", "LULUS"],
        ["6", "labkita-postinstall", "Buat praktikan tanpa error", "User & sandi terbuat [SUKSES], namun baris 45 error: printf: - : pilihan tidak valid", "PARSIAL"],
        ["7", "Isolasi Akun Praktikan", "Izin 0700 & tanpa hak sudo", "stat 700, akses ls ditolak ('Ijin ditolak'), grup sudo/adm hanya labkitaadmin", "LULUS"],
        ["8", "Kompilasi & Python Offline", "Toolchain jalan saat net mati", "nmcli networking off (disabled); gcc hello.c, hello.py, processes.py sukses", "LULUS"],
        ["9", "Peluncur labkita-guide", "Panduan HTML tampil di browser", "Disalin ke ~/.local/share/labkita/guide/, tetapi ditolak Firefox Snap", "GAGAL"],
        ["10", "Tmpfs & Sisa Label 0.2", "Tmpfs 1777 & label konsisten 0.2", "/run/labkita 1777 aktif; namun layar sambutan masih menyebut 'LabKita Linux 0.1'", "PARSIAL"]
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
        elif st in ("PARSIAL", "LULUS*"):
            clr = colors.HexColor("#D97706")
        else:
            clr = colors.HexColor("#16A34A")
        style_cmds.append(('TEXTCOLOR', (4, r_idx), (4, r_idx), clr))
    t_test.setStyle(TableStyle(style_cmds))
    story.append(t_test)
    story.append(Paragraph("<i>*Catatan: Lulus melalui jalur fallback subiquity.cmd.tui karena installer GUI gagal.</i>", caption_style))
    story.append(Spacer(1, 8))

    # Evidence Images (100% genuine VM captures)
    story.append(Paragraph("Bukti Tangkapan Layar Pengujian Nyata (Capture VM Asli):", h3_style))
    ev_dir = Path("docs/evidence")

    img1_path = str(ev_dir / "04-installed-desktop-whitesur-id.png")
    img2_path = str(ev_dir / "05-installed-labkita-check.png")
    img3_path = str(ev_dir / "09-installed-guide-firefox-snap-error.png")
    img4_path = str(ev_dir / "13-v02-installed-bench-r1.png")

    if os.path.exists(img1_path) and os.path.exists(img2_path) and os.path.exists(img3_path) and os.path.exists(img4_path):
        img_table_data = [
            [Image(img1_path, width=230, height=144), Image(img2_path, width=230, height=144)],
            [Paragraph("Gambar 4.1: Desktop Terinstal 0.2 (Tema WhiteSur, Dock Bawah, & Berkas Bahasa Indonesia)", caption_style),
             Paragraph("Gambar 4.2: Eksekusi labkita-check pada Sistem Terinstal (21/21 Lulus)", caption_style)],
            [Image(img3_path, width=230, height=144), Image(img4_path, width=230, height=144)],
            [Paragraph("Gambar 4.3: Bukti Kegagalan Nyata labkita-guide Diblokir Firefox Snap ('Akses terhadap berkas ditolak')", caption_style),
             Paragraph("Gambar 4.4: Pengukuran Benchmark Terinstal 0.2 Run 1 (free -m & systemd-analyze)", caption_style)]
        ]
        t_img = Table(img_table_data, colWidths=[240, 240])
        t_img.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
        story.append(t_img)
        story.append(Spacer(1, 10))

    story.append(Paragraph("4.3 Pengukuran Kinerja dan Tolok Ukur Empiris (0.1 vs 0.2 Terinstal)", h2_style))
    story.append(Paragraph(
        "Pengukuran dilakukan ulang pada VM yang sama (RAM 4.096 MB / 3.911 MiB terdeteksi, 2 vCPU, disk 40 GB SCSI) setelah instalasi penuh ke disk, sebanyak 3 kali reboot bersih per versi (settle 20 detik setelah desktop siap):",
        body_style
    ))

    # Benchmark Table
    bench_data = [
        ["Parameter Uji", "LabKita 0.1 Terinstal (3x)", "LabKita 0.2 Terinstal (3x)", "Selisih & Analisis Jujur"],
        ["Penggunaan Memori\n(free -m Used)", "Run 1: 1.025 MiB\nRun 2: 1.030 MiB\nRun 3: 1.040 MiB\nRata-rata: 1.031,7 MiB\n(Avail: 2.878,7 MiB)", "Run 1: 1.063 MiB\nRun 2: 1.053 MiB\nRun 3: 1.064 MiB\nRata-rata: 1.060,0 MiB\n(Avail: 2.850,7 MiB)", "+28,3 MiB (+2,7%) di 0.2.\nOverhead wajar dari tema WhiteSur & Dash-to-Dock; sisa RAM ~2,85 GiB sangat memadai."],
        ["Waktu Booting\n(systemd-analyze time)", "Run 1: 10,437s\nRun 2: 9,490s\nRun 3: 9,752s\nRata-rata: 9,893s\n(Kernel 3,451s + User 6,442s)", "Run 1: 9,578s\nRun 2: 13,662s\nRun 3: 11,121s\nRata-rata: 11,454s\n(Kernel 3,742s + User 7,711s)", "+1,561s (+15,8%) lebih lambat & lebih variatif di 0.2.\nTidak ada klaim 'lebih cepat' atas 0.1."],
        ["Layanan Boot Terlama\n(systemd-analyze blame)", "1. plymouth-quit-wait: 2,64-3,12s\n2. snapd.seeded: 1,10-1,40s\n3. snapd.service: 0,91-1,36s", "1. plymouth-quit-wait: 2,99-4,34s\n2. snapd.seeded: 1,08-1,72s\n3. snapd.service: 1,03-1,66s", "Bottleneck identik pada plymouth-quit-wait dan layanan snapd saat startup desktop."],
        ["Ruang Disk Terinstal\n(df -h /)", "11 GiB terpakai / 19 GiB LV (62%)", "12 GiB terpakai / 19 GiB LV (64%)", "Sisa 6,5 GiB pada root LV default subiquity dari total disk virtual 40 GB."]
    ]
    t_bench = Table(bench_data, colWidths=[95, 115, 115, 155])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.4 Pembahasan Temuan Teknis: Kegagalan Nyata Selama Audit", h2_style))
    story.append(Paragraph(
        "Pengujian menyeluruh pascainstalasi pada LabKita 0.2 mengungkap beberapa temuan teknis yang dilaporkan apa adanya:",
        body_style
    ))
    story.append(Paragraph(
        "1. <b>Sandbox Firefox Snap Memblokir Dotfolder Panduan:</b> Pada versi 0.1 berkas di <code>/usr/share/labkita/guide/</code> diblokir oleh AppArmor Snap Firefox. Di versi 0.2 peluncur <code>labkita-guide</code> memindahkan salinan HTML ke <code>~/.local/share/labkita/guide/</code>, namun hasil uji nyata membuktikan Firefox Snap <b>tetap menolak akses</b> dengan pesan <i>'Akses terhadap berkas ditolak'</i> karena profil keamanan <code>home</code> Snap melarang akses ke direktori tersembunyi berawalan titik (<code>~/.local</code>).",
        body_style
    ))
    story.append(Paragraph(
        "2. <b>Kegagalan Installer Grafis & Sisa Metadata:</b> Installer grafis <code>ubuntu-desktop-bootstrap</code> gagal saat live boot dengan dialog <i>'Ada yang salah'</i> akibat mismatch <code>casper-md5check</code> pasca-remastering dan kegagalan kueri info snap offline. Instalasi penuh tetap berhasil menggunakan <code>subiquity.cmd.tui</code>. Selain itu, skrip <code>labkita-postinstall</code> pada ISO 0.2 memiliki bug sintaks <code>printf: - : pilihan tidak valid</code> pada baris ke-45 (meski pembuatan akun & sandi <code>praktikan</code> sudah berhasil sebelum error cetak baris terakhir).",
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
    story.append(Paragraph("1. <b>Keluaran Produk Tercapai:</b> Berkas citra bootable <code>labkita-linux-0.2-amd64.iso</code> (~6.07 GiB, SHA256 <code>ae6391a2...</code>) berhasil dibangun, lolos verifikasi hash, dan dapat diinstal penuh ke disk virtual melalui <code>subiquity.cmd.tui</code>.", bullet_style))
    story.append(Paragraph("2. <b>Penerapan Konsep Sistem Operasi Terbukti:</b> LabKita Linux 0.2 terinstal mengimplementasikan manajemen proses multiprocessing (forking), virtual memory tmpfs (sticky bit 1777), layanan systemd daemon (<code>labkita-runtime</code>), kontrol akses 0700, serta isolasi akun non-sudo.", bullet_style))
    story.append(Paragraph("3. <b>Visi Pemrograman Offline Terpenuhi:</b> Pengujian dengan jaringan dimatikan total (<code>nmcli networking off</code>) membuktikan compiler GCC, Python 3, dan contoh program praktikum berjalan tanpa akses internet.", bullet_style))
    story.append(Paragraph("4. <b>Integritas Data Empiris & Pelaporan Jujur:</b> Dalam 3x pengukuran kondisi VM identik setelah instalasi, konsumsi RAM 0.2 rata-rata tercatat 1.060,0 MiB (+28,3 MiB vs 0.1 sebesar 1.031,7 MiB) dan waktu boot rata-rata 11,454 detik (+1,561s lebih lambat vs 0.1 sebesar 9,893 detik), sehingga tidak diklaim lebih ringan maupun lebih cepat.", bullet_style))

    story.append(Paragraph("5.2 Keterbatasan dan Kegagalan Terbuka pada Rilis 0.2", h2_style))
    story.append(Paragraph(
        "Berdasarkan audit pengujian nyata pada ISO 0.2, terdapat keterbatasan dan item gagal yang belum terselesaikan:",
        body_style
    ))
    story.append(Paragraph("• <b>Installer Grafis & Live Autologin:</b> <code>ubuntu-desktop-bootstrap</code> masih gagal (<i>'Ada yang salah'</i>) dan sesi live jatuh ke <code>gnome-initial-setup</code>.", bullet_style))
    story.append(Paragraph("• <b>Panduan Lokal & Firefox Snap:</b> Peluncur <code>labkita-guide</code> masih diblokir Firefox Snap karena menyalin HTML ke dotfolder <code>~/.local/share/labkita/guide/</code>.", bullet_style))
    story.append(Paragraph("• <b>Bug ISO 0.2 & Sisa Label:</b> <code>labkita-postinstall</code> di ISO 0.2 mengalami error baris 45 (<code>printf</code>; sudah diperbaiki ke <code>printf --</code> di source repo, menunggu rebuild ISO), dan welcome dialog masih membawa label <code>0.1</code>.", bullet_style))

    story.append(Paragraph("5.3 Saran Pengembangan Rilis Selanjutnya (LabKita Linux 0.3)", h2_style))
    story.append(Paragraph(
        "Untuk pengembangan rilis berikutnya (LabKita Linux 0.3), disarankan perbaikan terfokus berikut:",
        body_style
    ))
    story.append(Paragraph("1. <b>Perbaikan Jalur Panduan Non-Dotfolder:</b> Mengubah target salinan <code>labkita-guide</code> dari <code>~/.local/...</code> menjadi folder non-tersembunyi (misal <code>~/Panduan-LabKita</code>) atau server HTTP lokal <code>127.0.0.1</code> agar tidak ditolak Firefox Snap.", bullet_style))
    story.append(Paragraph("2. <b>Rebuild ISO dengan Perbaikan Skrip & Metadata:</b> Mengemas ulang perbaikan <code>printf --</code> pada <code>labkita-postinstall</code>, memperbarui metadata label rilis menjadi 0.3 di <code>.disk/info</code> dan <code>casper</code>, serta memperbaiki autologin & manifest checksum Cubic.", bullet_style))
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
        "• <b>Repositori GitHub Resmi:</b> <font color='#1E3A8A'><u>https://github.com/luvices/labkita</u></font> (memuat seluruh skrip kustomisasi, konfigurasi paket, dokumen pengujian, generator laporan, dan bukti tangkapan layar).<br/>"
        "• <b>Berkas Citra ISO Resmi:</b> <code>labkita-linux-0.2-amd64.iso</code> (Ukuran: 6.519.777.280 bytes).<br/>"
        "• <b>Verifikasi SHA256:</b> <code>ae6391a26d3497cb9d9aed4d9e967352e46adfd630202ac47c58b149d8000d19</code><br/>"
        "• <b>Verifikasi MD5:</b> <code>e0f73c691ffd65f1c0108f60834d15f4</code>",
        body_style
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Lampiran 2: Naskah dan Tautan Video Demonstrasi (3–5 Menit)", h2_style))
    story.append(Paragraph(
        "Sesuai ketentuan Bagian 5 Poin 4, video demonstrasi berdurasi 4 menit 30 detik disiapkan dengan struktur alur kerja: "
        "(1) Pembukaan, booting GRUB Bahasa Indonesia & instalasi ke disk via subiquity TUI, (2) Desktop 0.2 terinstal (tema WhiteSur, dock bawah, & Bahasa Indonesia), "
        "(3) Eksekusi labkita-check (21/21 lulus) dan pelaporan terbuka bug baris 45 postinstall & blokir Firefox Snap pada labkita-guide, "
        "(4) Pembuktian offline total tanpa jaringan (GCC & multiprocessing Python), (5) Isolasi folder 0700 dan akun praktikan non-sudo, "
        "serta (6) Perbandingan empiris 3x pengukuran RAM free -m dan boot time systemd-analyze (0.1 vs 0.2 terinstal).<br/>"
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
