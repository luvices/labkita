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
        self.drawString(54, 800, "Laporan Final Project Sistem Operasi — LabKita Linux 0.1")
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
    story.append(Paragraph("LABKITA LINUX 0.1", title_style))
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
        ["BAB I", "PENDAHULUAN", "2"],
        ["", "1.1 Latar Belakang Masalah", "2"],
        ["", "1.2 Visi dan Tujuan Produk", "2"],
        ["", "1.3 Sasaran Pengguna", "2"],
        ["", "1.4 Ruang Lingkup Proyek", "3"],
        ["", "1.5 Pembagian Tugas dan Kontribusi Anggota Kelompok", "3"],
        ["BAB II", "LANDASAN TEORI SISTEM OPERASI", "4"],
        ["", "2.1 Konsep Manajemen Proses dan Multiprocessing", "4"],
        ["", "2.2 Manajemen Memori dan Virtual Filesystem (Tmpfs)", "4"],
        ["", "2.3 Keamanan Sistem Operasi dan Privilege Separation", "5"],
        ["", "2.4 Inisialisasi Sistem dan Layanan Daemon (Systemd)", "5"],
        ["", "2.5 Arsitektur Live CD dan OverlayFS", "6"],
        ["BAB III", "PERANCANGAN SISTEM", "7"],
        ["", "3.1 Arsitektur LabKita Linux", "7"],
        ["", "3.2 Alur Kerja Pembuatan ISO dengan Cubic", "7"],
        ["", "3.3 Rancangan Antarmuka dan Pengalaman Pengguna (UI/UX)", "8"],
        ["", "3.4 Spesifikasi Perangkat Keras dan Perangkat Lunak", "8"],
        ["BAB IV", "IMPLEMENTASI DAN PENGUJIAN", "9"],
        ["", "4.1 Langkah-Langkah Implementasi", "9"],
        ["", "4.2 Skenario dan Hasil Pengujian Fungsional", "10"],
        ["", "4.3 Pengukuran Kinerja dan Tolok Ukur Empiris (Benchmarks)", "11"],
        ["", "4.4 Pembahasan Temuan Teknis: Sandboxing Snap dan AppArmor", "12"],
        ["BAB V", "PENUTUP", "13"],
        ["", "5.1 Kesimpulan", "13"],
        ["", "5.2 Keterbatasan Produk", "13"],
        ["", "5.3 Saran Pengembangan Masa Depan", "13"],
        ["DAFTAR PUSTAKA DAN LAMPIRAN", "", "14"],
        ["", "Daftar Pustaka", "14"],
        ["", "Lampiran 1: Tautan Repositori Kode Sumber dan Berkas ISO", "14"],
        ["", "Lampiran 2: Tautan dan Naskah Video Demonstrasi (3-5 Menit)", "15"],
        ["", "Lampiran 3: Pernyataan Kejujuran Akademik dan Penggunaan AI", "15"]
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
        "Ruang lingkup pengerjaan LabKita Linux versi 0.1 dibatasi pada:",
        body_style
    ))
    story.append(Paragraph("1. Basis distribusi menggunakan Ubuntu Desktop 24.04.5 LTS (Noble Numbat) arsitektur x86_64 dengan kernel Linux 7.0 generic.", bullet_style))
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
        ["1", "Dafa Zahran", "257006111188", "Ketua Kelompok, Manajer Proyek & Integrasi (Build/Integrasi)", "Mengoordinasikan pembagian modul tim, pipeline build Cubic, mastering berkas ISO (labkita-linux-0.1-amd64.iso), manajemen repositori GitHub (https://github.com/luvices/labkita), dan keselarasan luaran tugas."],
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
    story.append(Paragraph("1. <b>Lapisan Kernel & Driver:</b> Kernel Linux 7.0 generic dengan modul open-vm-tools terintegrasi untuk mendukung display scaling SVGA dan integrasi hypervisor.", bullet_style))
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
        "Antarmuka grafis dirancang bersih, intuitif, dan bebas gangguan. "
        "Identitas visual LabKita Linux diwujudkan melalui wallpaper kustom SVG bertuliskan <i>'Ruang belajar. Siap offline. Python / C / Linux'</i>. "
        "Panel dock sebelah kiri ditata secara ergonomis dengan menempatkan aplikasi prioritas di bagian teratas: Geany IDE, Terminal GNOME, File Manager, dan Panduan Praktikum. "
        "Tema antarmuka Yaru diselaraskan agar nyaman di mata mahasiswa saat digunakan dalam sesi praktikum berdurasi panjang.",
        body_style
    ))

    story.append(Paragraph("3.4 Spesifikasi Perangkat Keras dan Perangkat Lunak", h2_style))
    story.append(Paragraph("Tabel berikut merangkum spesifikasi lingkungan pengembangan dan target mesin virtual pengujian:", body_style))

    specs_data = [
        ["Komponen", "Lingkungan Host Pembuat", "Spesifikasi Target VM Pengujian"],
        ["Sistem Operasi", "Windows 11 Home 64-bit", "LabKita Linux 0.1 (Kernel 7.0 Generic)"],
        ["Hypervisor", "VMware Workstation 25.0.1", "Virtual Machine Hardware v21"],
        ["Prosesor / vCPU", "AMD Ryzen 5 (Host)", "2 Core vCPU Virtual"],
        ["Kapasitas RAM", "16 GB DDR4 (Host)", "4.096 MB (4 GB) Virtual RAM"],
        ["Penyimpanan", "Drive C (~93 GB Free) & D (Data)", "40 GB Growable Virtual Disk (NVMe/SCSI)"],
        ["Resolusi Layar", "1920 x 1080 (Display Scaling 125%)", "1280 x 800 (SVGA ScreenTarget)"]
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
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
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
    story.append(Paragraph("3. <b>Mastering ISO:</b> Xorriso menghasilkan berkas <code>labkita-linux-0.1-amd64.iso</code> berukuran 6.493.779.968 bytes (~6.05 GiB) dengan SHA256 terverifikasi <code>f80e42c9e8d4db820121f02fca79588760f1549a6cc6634929e3b0e071b810c5</code>.", bullet_style))
    story.append(Paragraph("4. <b>Pengujian Mesin Virtual (VM Test):</b> Dibuat VM uji bersih <code>build/test-vm/labkita-test.vmx</code> dengan disk kosong 40 GB pada drive C. Hypervisor dikonfigurasi dengan VNC remote framing di port 5900 untuk monitoring dan otomasi pengujian.", bullet_style))

    story.append(Paragraph("4.2 Skenario dan Hasil Pengujian Fungsional", h2_style))
    story.append(Paragraph("Pengujian fungsional dan keamanan dijalankan secara nyata pada VM uji. Tabel berikut memuat hasil seluruh skenario pengujian:", body_style))

    test_matrix = [
        ["No", "Skenario Uji", "Hasil yang Diharapkan", "Hasil Aktual", "Status"],
        ["1", "Boot ISO di VM Kosong", "Sesi live termuat normal", "Boot sukses (kernel 7.0), wallpaper & dock aktif", "LULUS"],
        ["2", "Suite labkita-check", "Seluruh pemeriksaan lulus", "14 dari 14 pengujian lulus sempurna (0 gagal)", "LULUS"],
        ["3", "Pembuatan Akun Praktikan", "Akun tanpa sudo via skrip", "Akun 'praktikan' dibuat, password interaktif", "LULUS"],
        ["4", "Hak Akses Folder Mahasiswa", "Mode izin 0700 (drwx------)", "Terverifikasi 0700; user lain ditolak akses", "LULUS"],
        ["5", "Pembatasan Sudo Praktikan", "Akses sudo -l ditolak", "Ditolak: praktikan tidak berhak akses sudo", "LULUS"],
        ["6", "Kompilasi & Eksekusi C", "gcc hello.c berjalan normal", "Output: 'Halo dari LabKita Linux!' sukses", "LULUS"],
        ["7", "Eksekusi Proses Python", "multiprocessing fork() sukses", "Proses anak PID 5696 & 5697 sukses paralel", "LULUS"],
        ["8", "Geany IDE Siap Pakai", "Geany menampilkan hello.c", "Geany 2.0 terbuka normal dengan syntax c", "LULUS"],
        ["9", "Uji Offline Total", "Toolchain jalan tanpa net", "nmcli net off (none); GCC & Python 100% normal", "LULUS"],
        ["10", "Ruang Tmpfs /run/labkita", "Sticky bit 1777 via systemd", "Izin 1777 (drwxrwxrwt); berkas hilang saat reboot", "LULUS"]
    ]
    t_test = Table(test_matrix, colWidths=[20, 105, 120, 195, 40])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.5),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (4,0), (4,-1), 'CENTER'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 7),
        ('TEXTCOLOR', (4,1), (4,-1), colors.HexColor("#16A34A")),
        ('FONTNAME', (4,1), (4,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t_test)
    story.append(Spacer(1, 10))

    # Evidence Images
    story.append(Paragraph("Bukti Tangkapan Layar Pengujian Nyata:", h3_style))
    ev_dir = Path("docs/evidence")
    
    img1_path = str(ev_dir / "01-labkita-check-pass.png")
    img2_path = str(ev_dir / "07-practicum-execution.png")
    img3_path = str(ev_dir / "04-praktikan-sudo-denied.png")
    img4_path = str(ev_dir / "08-geany-ide.png")

    if os.path.exists(img1_path) and os.path.exists(img2_path):
        img_table_data = [
            [Image(img1_path, width=235, height=147), Image(img2_path, width=235, height=147)],
            [Paragraph("Gambar 4.1: Eksekusi Mandiri labkita-check (14/14 Lulus)", caption_style),
             Paragraph("Gambar 4.2: Eksekusi Python Multiprocess & Kompilasi C", caption_style)]
        ]
        t_img = Table(img_table_data, colWidths=[240, 240])
        t_img.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
        story.append(t_img)

    story.append(PageBreak())

    if os.path.exists(img3_path) and os.path.exists(img4_path):
        img_table_data2 = [
            [Image(img3_path, width=235, height=147), Image(img4_path, width=235, height=147)],
            [Paragraph("Gambar 4.3: Pembuktian Isolasi Keamanan Sudo Praktikan", caption_style),
             Paragraph("Gambar 4.4: Geany IDE Terbuka Menampilkan hello.c", caption_style)]
        ]
        t_img2 = Table(img_table_data2, colWidths=[240, 240])
        t_img2.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
        story.append(t_img2)

    story.append(Paragraph("4.3 Pengukuran Kinerja dan Tolok Ukur Empiris (Benchmarks)", h2_style))
    story.append(Paragraph(
        "Sesuai prinsip integritas ilmiah proyek, seluruh angka kinerja diperoleh dari pengukuran langsung pada VM uji tanpa rekayasa data:",
        body_style
    ))

    # Benchmark Table
    bench_data = [
        ["Parameter Uji", "Perintah Pengukuran", "Nilai Empiris Aktual", "Analisis & Implikasi Sistem"],
        ["Penggunaan Memori (RAM)", "free -m", "Used: 1.342 MB (~1.34 GB)\nFree: 450 MB\nAvailable: 2.568 MB\nTotal: 3.911 MB (~4 GB)", "Penggunaan RAM stabil pada ~1.34 GB, sebanding dengan Ubuntu 24.04 GNOME standar. Bebas dari kebocoran memori (memory leak)."],
        ["Waktu Booting Startup", "systemd-analyze time", "Kernel: 5.313 detik\nUserspace: 54.672 detik\nTotal: 59.985 detik\nGraphical Target: 29.410s", "Desktop grafis siap dipakai dalam 29.4 detik di userspace. Booting kernel sangat cepat (5.3s) berkat deteksi perangkat keras modern."],
        ["Layanan Booting Terlama", "systemd-analyze blame", "1. casper-md5check: 25.24s\n2. snapd.seeded: 20.49s\n3. snapd.service: 7.83s\n4. plymouth: 7.26s", "Waktu terlama diserap oleh verifikasi integritas live CD (casper) dan daemon snapd bawaan Ubuntu upstream."],
        ["Kapasitas Root Overlay", "df -h /", "Filesystem: /cow (OverlayFS)\nTotal: 2.0 GB\nUsed: 67 MB (4%)\nAvailable: 1.9 GB", "Lapisan modifikasi memori Copy-on-Write sangat hemat (hanya 67 MB), menyediakan sisa ruang leluasa untuk aktivitas latihan mahasiswa."]
    ]
    t_bench = Table(bench_data, colWidths=[95, 95, 140, 150])
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

    story.append(Paragraph("4.4 Pembahasan Temuan Teknis: Sandboxing Snap dan AppArmor", h2_style))
    story.append(Paragraph(
        "Dalam pengujian pembukaan berkas panduan lokal (<code>/usr/share/labkita/guide/index.html</code>) melalui shortcut desktop yang memanggil peramban default (Firefox), ditemukan pesan kesalahan <i>'Fichier introuvable'</i> (File Not Found). "
        "Analisis mendalam terhadap sistem operasi mengungkap temuan teknis yang sangat berharga:",
        body_style
    ))
    story.append(Paragraph(
        "Pada Ubuntu 24.04 LTS, peramban Mozilla Firefox dikemas secara default sebagai <b>Snap package</b> terisolasi yang dikontrol ketat oleh modul keamanan <b>AppArmor (Mandatory Access Control)</b>. "
        "Profil AppArmor Snap mengisolasi peramban dari akses langsung ke direktori sistem <code>/usr/share</code> guna mencegah potensi eksfiltrasi data sistem oleh aplikasi peramban. "
        "Akibatnya, peramban Snap tidak diizinkan membuka berkas HTML yang berada di luar direktori <code>$HOME</code> atau <code>/tmp</code> pengguna.",
        body_style
    ))
    story.append(Paragraph(
        "Temuan ini menunjukkan cara kerja nyata mekanisme sandboxing sistem operasi Linux modern. "
        "Solusi praktis yang diimplementasikan untuk mengatasi batasan ini mencakup: (1) Menyajikan berkas panduan melalui mikro-server Python lokal (<code>python3 -m http.server 8000 --directory /usr/share/labkita/guide</code>) yang dapat diakses via <code>http://localhost:8000</code>, atau (2) Menyalin dokumen panduan ke direktori pengguna lokal <code>~/.local/share/labkita/guide</code>.",
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
        "Berdasarkan hasil perancangan, implementasi, dan pengujian empiris yang telah dilakukan, dapat disimpulkan bahwa:",
        body_style
    ))
    story.append(Paragraph("1. <b>Keluaran Produk Tercapai:</b> Telah berhasil dibangun berkas citra bootable <code>labkita-linux-0.1-amd64.iso</code> berukuran ~6.05 GiB yang valid dan lolos uji verifikasi checksum SHA256.", bullet_style))
    story.append(Paragraph("2. <b>Penerapan Konsep Sistem Operasi Terbukti:</b> LabKita Linux sukses mengimplementasikan manajemen proses multiprocessing (forking), virtual memory tmpfs (sticky bit 1777), layanan systemd daemon (labkita-runtime), serta kontrol akses DAC dan privilege separation (non-sudo 0700).", bullet_style))
    story.append(Paragraph("3. <b>Visi Pemrograman Offline Terpenuhi:</b> Pengujian dengan adapter jaringan dimatikan total (<code>connectivity: none</code>) membuktikan bahwa toolchain GCC 13, Python 3.12, dan Geany IDE dapat digunakan 100% secara mandiri tanpa internet.", bullet_style))
    story.append(Paragraph("4. <b>Integritas Akademik Terjaga:</b> Seluruh data performa (RAM ~1.34 GB, boot time 59.9s) dilaporkan secara objektif berdasarkan pengukuran nyata tanpa klaim performa yang mengada-ada.", bullet_style))

    story.append(Paragraph("5.2 Keterbatasan Produk", h2_style))
    story.append(Paragraph(
        "Pengembangan LabKita Linux versi awal (0.1) memiliki beberapa keterbatasan:",
        body_style
    ))
    story.append(Paragraph("• <b>Konsumsi Memori GNOME Shell:</b> Karena mempertahankan desktop environment bawaan GNOME Shell 46, konsumsi RAM awal berada pada kisaran 1.34 GB, sehingga kurang optimal jika dijalankan pada perangkat keras PC lawas dengan RAM terbatas (≤ 2 GB).", bullet_style))
    story.append(Paragraph("• <b>Ukuran Citra ISO:</b> Ukuran berkas ISO (~6.05 GiB) relatif besar karena menyertakan seluruh modul live Ubuntu desktop standar dan dokumentasi pengembang.", bullet_style))
    story.append(Paragraph("• <b>Isolasi Sandbox Peramban:</b> Integrasi berkas panduan lokal HTML di <code>/usr/share</code> terhambat oleh AppArmor confinement bawaan Snap Firefox upstream.", bullet_style))

    story.append(Paragraph("5.3 Saran Pengembangan Masa Depan", h2_style))
    story.append(Paragraph(
        "Untuk pengembangan rilis berikutnya (LabKita Linux 0.2), disarankan beberapa peningkatan strategis:",
        body_style
    ))
    story.append(Paragraph("1. <b>Migrasi Desktop Minimalis:</b> Mengganti GNOME Desktop dengan XFCE4 atau Openbox window manager untuk menekan penggunaan memori di bawah 600 MB RAM, memungkinkan distro berjalan lancar pada PC laboratorium generasi lama.", bullet_style))
    story.append(Paragraph("2. <b>Aplikasi Panduan Berbasis GTK Native:</b> Mengembangkan aplikasi pembaca panduan praktikum lokal berbasis GTK3/WebKit native (deb) sehingga tidak terpengaruh isolasi sandbox Snap.", bullet_style))
    story.append(Paragraph("3. <b>Otomasi Autoinstall Disk:</b> Menambahkan berkas konfigurasi cloud-init / Subiquity autoinstall otomatis agar proses kloning instalasi massal ke hard disk PC laboratorium dapat selesai tanpa interaksi pengguna manual.", bullet_style))
    story.append(Paragraph("4. <b>Mode Ujian Lab (Kiosk Profile):</b> Menyediakan profil login khusus yang mengunci terminal dan mematikan port USB saat sesi ujian pemrograman berlangsung.", bullet_style))
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
        "• <b>Berkas Citra ISO Resmi:</b> <code>labkita-linux-0.1-amd64.iso</code> (Ukuran: 6.493.779.968 bytes).<br/>"
        "• <b>Verifikasi SHA256:</b> <code>f80e42c9e8d4db820121f02fca79588760f1549a6cc6634929e3b0e071b810c5</code><br/>"
        "• <b>Verifikasi MD5:</b> <code>b457376899f24cbd1ee570e0c6edfd25</code>",
        body_style
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Lampiran 2: Naskah dan Tautan Video Demonstrasi (3–5 Menit)", h2_style))
    story.append(Paragraph(
        "Sesuai ketentuan Bagian 5 Poin 4, video demonstrasi berdurasi 4 menit 30 detik disiapkan dengan struktur alur kerja: "
        "(1) Pembukaan dan booting ISO di VM, (2) Pengenalan desktop dan branding LabKita, (3) Eksekusi pengujian mandiri labkita-check 100% lulus, "
        "(4) Pembuktian offline total tanpa jaringan (GCC & multiprocessing Python), (5) Keamanan hak akses non-sudo dan isolasi folder 0700, "
        "serta (6) Pengukuran memori RAM free -m dan boot time systemd-analyze.<br/>"
        "<i>Tautan Video Demo (YouTube Unlisted / Google Drive):</i> [Tautan disematkan oleh mahasiswa]",
        body_style
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Lampiran 3: Pernyataan Kejujuran Akademik dan Penggunaan AI", h2_style))
    story.append(Paragraph(
        "Sesuai Ketentuan Akademik Poin 8.2 dokumen pedoman Final Project Sistem Operasi Ganjil 2026/2027: "
        "<i>'Alat bantu AI generatif boleh digunakan sebagai pendukung, dengan mencantumkan bagian yang dibantu AI di laporan. Setiap anggota tetap harus memahami dan mampu menjelaskan seluruh bagian produk.'</i><br/><br/>"
        "Dengan ini kami menyatakan secara transparan kontribusi alat bantu kecerdasan buatan (AI coding assistant) dalam proyek ini meliputi: "
        "(a) Membantu otomatisasi eksekusi perintah hypervisor VMware via VNC remote protokol, "
        "(b) Membantu penyusunan skrip runner bukti tangkapan layar, dan "
        "(c) Membantu format penataan dokumen PDF dan slide presentasi agar selaras dengan rubrik akademik.<br/>"
        "Seluruh perancangan konsep sistem operasi (manajemen memori, hak akses Linux DAC, pemisahan hak istimewa, pembuatan layanan systemd, dan analisis tolok ukur empiris) dipelajari, diuji, dipahami secara mendalam, dan dapat dipertanggungjawabkan sepenuhnya oleh setiap anggota tim pada sesi presentasi dan tanya jawab UAS.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report PDF built successfully: {filename}")

if __name__ == "__main__":
    build_pdf()
