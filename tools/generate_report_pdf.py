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
        self.drawString(54, 800, "Laporan Final Project Sistem Operasi — LabKita Linux 0.3")
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
    story.append(Paragraph("LABKITA LINUX 0.3", title_style))
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
        ["", "4.3 Pengukuran Kinerja dan Tolok Ukur Empiris (0.1 vs 0.2 vs 0.3)", "8"],
        ["", "4.4 Pembahasan Temuan Teknis: Perbaikan 0.3 & Kegagalan GUI Installer", "9"],
        ["BAB V", "PENUTUP", "10"],
        ["", "5.1 Kesimpulan", "10"],
        ["", "5.2 Keterbatasan dan Kegagalan Terbuka pada Rilis 0.3", "10"],
        ["", "5.3 Saran Pengembangan Rilis Selanjutnya (LabKita Linux 0.4)", "10"],
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
        "Ruang lingkup pengerjaan LabKita Linux versi 0.3 dibatasi pada:",
        body_style
    ))
    story.append(Paragraph("1. Basis distribusi menggunakan Ubuntu Desktop 24.04.5 LTS (Noble Numbat) arsitektur x86_64 dengan kernel Linux 7.0.0-43-generic pada sistem 0.3 terinstal (dibanding 7.0.0-31-generic pada instalasi bersih versi 0.1 dan 0.2).", bullet_style))
    story.append(Paragraph("2. Perangkat lunak pemrograman mencakup GCC 13.3.0, G++ 13.3.0, Make 4.3, Python 3.12.3, Geany 2.0, Git 2.43, Nano, dan pustaka manpages-dev.", bullet_style))
    story.append(Paragraph("3. Kustomisasi sistem dilakukan melalui Cubic (Custom Ubuntu ISO Creator) versi 2026.09.110-release~202609120048~ubuntu24.04.1 beserta regenerasi md5sum.txt pasca-remastering.", bullet_style))
    story.append(Paragraph("4. Pengujian dilakukan secara empiris pada hypervisor VMware Workstation 25 mencakup verifikasi integritas ISO, uji GUI installer vs TUI fallback, labkita-check (termasuk tes baca Firefox Snap), labkita-postinstall, pengujian offline, serta 5 kali tolok ukur RAM dan waktu boot per versi.", bullet_style))

    story.append(Paragraph("1.5 Pembagian Tugas dan Kontribusi Anggota Kelompok", h2_style))
    story.append(Paragraph(
        "Sesuai dengan ketentuan rubrik final project, tim kelompok terdiri atas mahasiswa dengan pembagian peran yang terukur dan adil:",
        body_style
    ))

    team_data = [
        ["No", "Nama", "NPM", "Peran", "Rincian Tugas dan Kontribusi"],
        ["1", "Dafa Zahran", "257006111188", "Ketua Kelompok, Manajer Proyek & Integrasi (Build/Integrasi)", "Mengoordinasikan pembagian modul tim, pipeline build Cubic, regenerasi manifest md5sum & mastering ISO (labkita-linux-0.3-amd64.iso), manajemen repositori GitHub (https://github.com/luvices/labkita), dan keselarasan luaran tugas."],
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
    story.append(Paragraph("1. <b>Lapisan Kernel & Driver:</b> Kernel 7.0.0-43-generic (0.3 terinstal; 7.0.0-31-generic pada 0.1/0.2 bersih) dengan open-vm-tools.", bullet_style))
    story.append(Paragraph("2. <b>Lapisan Inisialisasi & Runtime:</b> Systemd yang memuat layanan <code>labkita-runtime.service</code> untuk mount tmpfs <code>/run/labkita</code>.", bullet_style))
    story.append(Paragraph("3. <b>Lapisan Toolchain Praktikum:</b> Compiler C/C++ (GCC/G++), Python 3, debugger, dan editor Geany di <code>/usr/bin</code>.", bullet_style))
    story.append(Paragraph("4. <b>Lapisan Keamanan & Pengguna:</b> <code>labkita-postinstall</code> (fix <code>printf --</code>) mengatur akun non-sudo, <code>0700</code>, & salinan <code>~/Dokumen/Panduan-LabKita</code>.", bullet_style))
    story.append(Paragraph("5. <b>Lapisan Antarmuka Pengguna:</b> GNOME Shell 46 via <code>dconf</code> untuk tema WhiteSur, wallpaper LabKita, dan dock aplikasi.", bullet_style))

    story.append(Paragraph("3.2 Alur Kerja Pembuatan ISO dengan Cubic", h2_style))
    story.append(Paragraph(
        "Pembuatan citra ISO kustom LabKita Linux menggunakan <b>Cubic</b> versi <code>2026.09.110-release~202609120048~ubuntu24.04.1</code> dengan tahapan:",
        body_style
    ))
    story.append(Paragraph("• <b>Tahap 1 (ISO Source Verification):</b> Memverifikasi ISO sumber resmi Ubuntu 24.04.5 LTS Desktop amd64 via SHA256 (<code>4da4a0c9...</code>).", bullet_style))
    story.append(Paragraph("• <b>Tahap 2 (SquashFS Extraction):</b> Mengekstrak <code>filesystem.squashfs</code> ke lingkungan container <code>systemd-nspawn</code>.", bullet_style))
    story.append(Paragraph("• <b>Tahap 3 (Chroot Customization):</b> Mengekstrak <code>labkita-kit.tar.gz</code> dan menjalankan <code>customize.sh</code> (paket, systemd, <code>/etc/skel/Dokumen/Panduan-LabKita</code>, metadata 0.3).", bullet_style))
    story.append(Paragraph("• <b>Tahap 4 (Recompression, md5sum & Mastering):</b> Setelah squashfs, kernel, initrd, dan <code>install-sources.yaml</code> final terbentuk, <code>md5sum.txt</code> diregenerasi (tanpa <code>eltorito.img</code>) lalu <code>xorriso</code> memproduksi hybrid ISO.", bullet_style))

    story.append(Paragraph("3.3 Rancangan Antarmuka dan Pengalaman Pengguna (UI/UX)", h2_style))
    story.append(Paragraph(
        "Antarmuka versi 0.3 memakai tema open source <b>WhiteSur GTK/Icon/Cursors</b>, font <b>Inter</b>, tombol jendela di kiri, dock bawah terpusat, dan lokalisasi Bahasa Indonesia penuh (<code>id_ID.UTF-8</code>, <code>Asia/Jakarta</code>) tanpa aset proprietary Apple. Panduan lokal ditaruh di <code>~/Dokumen/Panduan-LabKita/</code> agar lolos AppArmor Firefox Snap.",
        body_style
    ))

    story.append(Paragraph("3.4 Spesifikasi Perangkat Keras dan Perangkat Lunak", h2_style))
    story.append(Paragraph("Tabel berikut merangkum spesifikasi lingkungan pengembangan dan target mesin virtual pengujian:", body_style))

    specs_data = [
        ["Komponen", "Lingkungan Host Pembuat", "Spesifikasi Target VM Pengujian"],
        ["Sistem Operasi", "Windows 11 64-bit", "LabKita 0.1 & 0.2 (7.0.0-31), 0.3 (7.0.0-43)"],
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
    story.append(Paragraph("2. <b>Eksekusi Kustomisasi & Regenerasi Checksum:</b> Kit diterapkan di lingkungan Cubic <code>2026.09.110-release~202609120048~ubuntu24.04.1</code>, seluruh metadata rilis diubah menjadi 0.3, dan <code>md5sum.txt</code> pada <code>custom-disk</code> diregenerasi setelah berkas squashfs/kernel/initrd final selesai (terverifikasi 957/957 OK pada ISO terpasang loop).", bullet_style))
    story.append(Paragraph("3. <b>Mastering ISO 0.3:</b> Xorriso menghasilkan berkas <code>labkita-linux-0.3-amd64.iso</code> berukuran 6.520.272.896 bytes (~6,07 GiB / 6,52 GB) dengan SHA256 terverifikasi <code>21f38dc158a010e6f80920274dd7b8cd8f3e0d7f5e91283a310e98e53f045387</code> dan MD5 <code>521f315f62a6c7cd08a31d40ad8c9fb5</code>.", bullet_style))
    story.append(Paragraph("4. <b>Pengujian Mesin Virtual (VM Test):</b> VM uji bersih <code>build/test-vm/labkita-test.vmx</code> dengan disk kosong 40 GB diinstal ulang penuh secara bergantian untuk versi 0.1, 0.2, dan 0.3 guna menjamin perbandingan 5x run per versi yang setara.", bullet_style))

    story.append(Paragraph("4.2 Skenario dan Hasil Pengujian Fungsional", h2_style))
    story.append(Paragraph("Pengujian fungsional, integritas media ISO, instalasi disk kosong, dan keamanan dijalankan nyata pada VM uji. Item yang tetap gagal pada 0.3 dilaporkan apa adanya:", body_style))

    test_matrix = [
        ["No", "Skenario Uji", "Hasil yang Diharapkan", "Hasil Aktual di VM 0.3", "Status"],
        ["1", "Integritas md5sum.txt & Casper", "957/957 berkas OK & md5check pass", "Loop ISO: 957/957 OK (exit 0); VM live: casper-md5check result 'pass'", "LULUS"],
        ["2", "GRUB & Live Autologin", "Boot ID 0.3 langsung masuk desktop", "GRUB 0.3 ID tampil; sesi live tetap masuk wizard gnome-initial-setup", "GAGAL"],
        ["3", "Installer GUI Bootstrap", "Wizard grafis selesai instalasi", "Masih gagal dialog 'Ada yang salah' meski md5sum pass & server WAITING", "GAGAL"],
        ["4", "Instalasi Disk (TUI)", "Instalasi penuh ke /dev/sda 40 GB", "Sumber tampil 'LabKita Linux 0.3'; sukses via fallback subiquity.cmd.tui", "LULUS*"],
        ["5", "Konsistensi Metadata 0.3", "Tidak ada sisa label 0.1 / 0.2", "os-release, lsb-release, sambutan, Tentang, & panduan tampil 0.3", "LULUS"],
        ["6", "Desktop WhiteSur & ID", "WhiteSur, dock tengah, UI Indonesia", "Tema WhiteSur, tombol kiri, dock, wallpaper, & Berkas ID (slot ikon dock redup)", "LULUS"],
        ["7", "Suite labkita-check (Snap)", "Menguji baca HTML di Firefox Snap", "Semua [LULUS] termasuk ~/Dokumen/Panduan-LabKita & snap run firefox (AppArmor OK)", "LULUS"],
        ["8", "Peluncur labkita-guide", "Panduan terbuka di Firefox Snap", "Firefox Snap merender ~/Dokumen/Panduan-LabKita/index.html tanpa blokir", "LULUS"],
        ["9", "Fix labkita-postinstall", "Cetak ringkasan tanpa error printf", "sudo labkita-postinstall praktikan [SUKSES] 0 error; panduan tersalin", "LULUS"],
        ["10", "Isolasi 0700 & Non-Sudo", "Izin 0700 & akun tanpa sudo", "stat 700, akses ls ditolak ('Ijin ditolak'), sudo praktikan ditolak", "LULUS"],
        ["11", "Offline GCC/Python & Tmpfs", "Jalan saat nmcli off; /run/labkita 1777", "nmcli off: gcc hello.c (~/Praktikum), hello.py, processes.py sukses; tmpfs 1777", "LULUS"]
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
    story.append(Paragraph("<i>*Catatan: Lulus melalui jalur fallback subiquity.cmd.tui karena installer GUI tetap gagal dengan 'Ada yang salah'.</i>", caption_style))
    story.append(Spacer(1, 8))

    # Evidence Images (100% genuine VM captures)
    story.append(Paragraph("Bukti Tangkapan Layar Pengujian Nyata 0.3 (Capture VM Asli):", h3_style))
    ev_dir = Path("docs/evidence")

    img1_path = str(ev_dir / "07-v03-installed-desktop-whitesur-id.png")
    img2_path = str(ev_dir / "09-v03-installed-labkita-check.png")
    img3_path = str(ev_dir / "10-v03-installed-guide-firefox-snap.png")
    img4_path = str(ev_dir / "02-v03-gui-installer-error.png")

    if os.path.exists(img1_path) and os.path.exists(img2_path) and os.path.exists(img3_path) and os.path.exists(img4_path):
        img_table_data = [
            [Image(img1_path, width=230, height=144), Image(img2_path, width=230, height=144)],
            [Paragraph("Gambar 4.1: Desktop Terinstal 0.3 (WhiteSur, Dock, & Berkas ~/Dokumen/Panduan-LabKita)", caption_style),
             Paragraph("Gambar 4.2: labkita-check 0.3 (Lulus Uji Baca Sandbox Firefox Snap / AppArmor OK)", caption_style)],
            [Image(img3_path, width=230, height=144), Image(img4_path, width=230, height=144)],
            [Paragraph("Gambar 4.3: Panduan ~/Dokumen/Panduan-LabKita/index.html Terbuka Normal di Firefox Snap", caption_style),
             Paragraph("Gambar 4.4: Bukti Kegagalan Nyata Installer GUI 0.3 ('Ada yang salah' Meski md5sum Lulus)", caption_style)]
        ]
        t_img = Table(img_table_data, colWidths=[240, 240])
        t_img.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
        story.append(t_img)
        story.append(Spacer(1, 10))

    story.append(Paragraph("4.3 Pengukuran Kinerja dan Tolok Ukur Empiris (0.1 vs 0.2 vs 0.3, 5x per Versi)", h2_style))
    story.append(Paragraph(
        "Pengukuran dilakukan ulang pada VM yang sama (RAM 4.096 MB / 3.911 MiB terdeteksi, 2 vCPU, disk kosong 40 GB SCSI yang diinstal ulang bersih untuk setiap versi), sebanyak <b>5 kali cold boot bersih per versi</b> (settle 20 detik setelah desktop siap). "
        "<b>Variabel pembeda kernel:</b> 0.1 dan 0.2 bersih memakai kernel Linux <code>7.0.0-31-generic</code>, sedangkan 0.3 memakai <code>7.0.0-43-generic</code>.",
        body_style
    ))

    # Benchmark Table
    bench_data = [
        ["Parameter Uji", "LabKita 0.1 (5x)\n[Kernel 7.0.0-31]", "LabKita 0.2 (5x)\n[Kernel 7.0.0-31]", "LabKita 0.3 (5x)\n[Kernel 7.0.0-43]"],
        ["Memori Used\n(free -m, MiB)", "1052 / 1018 / 1056 /\n1049 / 1016 MiB\nRata2: 1.038,2 MiB\nRentang: 1.016–1.056\n(Avail avg: 2.872,6)", "1072 / 1080 / 1072 /\n1059 / 1058 MiB\nRata2: 1.068,2 MiB\nRentang: 1.058–1.080\n(Avail avg: 2.842,2)", "1049 / 1067 / 1067 /\n1062 / 1046 MiB\nRata2: 1.058,2 MiB\nRentang: 1.046–1.067\n(Avail avg: 2.852,0)"],
        ["Waktu Boot Total\n(systemd-analyze)", "8,359 / 8,403 / 8,676 /\n8,434 / 8,426 s\nRata2: 8,460s\nRentang: 8,359–8,676s\n(Kernel 3,205 + User 5,255s)", "9,437 / 9,401 / 9,458 /\n9,218 / 9,072 s\nRata2: 9,317s\nRentang: 9,072–9,458s\n(Kernel 3,330 + User 5,987s)", "8,840 / 8,938 / 8,788 /\n8,460 / 9,014 s\nRata2: 8,808s\nRentang: 8,460–9,014s\n(Kernel 3,197 + User 5,610s)"],
        ["graphical.target\n(userspace)", "Rata2: 5,180s\n(5,084s–5,371s)", "Rata2: 5,918s\n(5,786s–6,057s)", "Rata2: 5,532s\n(5,215s–5,717s)"],
        ["Layanan Boot Terlama", "plymouth-quit-wait: 2,18–2,50s\nsnapd.seeded: ~1,02s", "plymouth-quit-wait: 2,61–2,85s\nsnapd.seeded: ~1,12s", "plymouth-quit-wait: 2,21–2,70s\nsnapd.seeded: ~1,05s"]
    ]
    t_bench = Table(bench_data, colWidths=[90, 130, 130, 130])
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
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Kesimpulan Empiris Benchmark (Tanpa Klaim Lebih Ringan/Cepat):</b> Rentang konsumsi RAM 0.3 (1.046–1.067 MiB) bertumpang tindih dengan 0.1 (1.016–1.056 MiB) dan 0.2 (1.058–1.080 MiB), sehingga tidak ada perbedaan yang dapat dibuktikan. Pada waktu boot, rentang 0.3 (8,460–9,014s; rata-rata 8,808s) bertumpang tindih dengan 0.1 (8,359–8,676s; rata-rata 8,460s); meski seluruh 5 run 0.3 lebih singkat dari seluruh 5 run 0.2 (9,072–9,458s), adanya perbedaan kernel (<code>7.0.0-43-generic</code> vs <code>7.0.0-31-generic</code>) membuat selisih tidak dapat dikaitkan dengan LabKita (kesimpulan: tidak ada perbedaan yang dapat dibuktikan).",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.4 Pembahasan Temuan Teknis: Perbaikan 0.3 & Kegagalan GUI Installer", h2_style))
    story.append(Paragraph(
        "Pengujian menyeluruh pada LabKita Linux 0.3 memvalidasi keberhasilan tiga perbaikan sekaligus mencatat kegagalan yang masih bertahan:",
        body_style
    ))
    story.append(Paragraph(
        "1. <b>Perbaikan yang Terbukti Lulus di 0.3:</b> (a) Regenerasi <code>md5sum.txt</code> pada <code>custom-disk</code> berhasil membuat <code>casper-md5check</code> di live VM berstatus <code>pass</code> (957/957 berkas OK di loop ISO), (b) Pemindahan panduan ke folder non-dotfolder <code>~/Dokumen/Panduan-LabKita/</code> lolos kebijakan sandbox AppArmor Firefox Snap dan benar-benar diuji baca oleh <code>labkita-check</code> lewat <code>snap run --shell firefox</code>, serta (c) Perbaikan <code>printf --</code> di <code>labkita-postinstall</code> dan sinkronisasi metadata <code>0.3</code> tampil konsisten pada <code>os-release</code>, dialog sambutan, dan menu Pengaturan Tentang.",
        body_style
    ))
    story.append(Paragraph(
        "2. <b>Kegagalan GUI Installer (<code>ubuntu-desktop-bootstrap</code>) & Live Autologin yang Masih Bertahan:</b> Meskipun <code>casper-md5check</code> sudah lulus dan backend <code>subiquity-server</code> mencapai status <code>ApplicationState.WAITING</code> dengan daftar sumber <code>LabKita Linux 0.3</code> termuat benar, antarmuka grafis Flutter <code>ubuntu-desktop-bootstrap</code> tetap berhenti di dialog <i>'Ada yang salah'</i>. Log <code>ubuntu_bootstrap.log</code> berhenti setelah <code>Inhibiting Gnome session</code>, sementara <code>journalctl -b</code> dan stderr langsung mencatat error library GTK/Flutter (<code>im-ibus.so: undefined symbol</code>, <code>libEGL warning: DRI3 error</code> pada SVGA virtual, dan assertion <code>fl_view_set_textures</code> saat penutupan), ditambah ketiadaan user autologin <code>NOPASSWD:ALL</code> akibat jatuhnya sesi live ke <code>gnome-initial-setup</code>. Fallback <code>subiquity.cmd.tui</code> tetap sukses menuntaskan instalasi.",
        body_style
    ))
    story.append(Paragraph("3. <b>Eksperimen Kontrol:</b> Pada VMX yang sama, ISO Ubuntu 24.04.5.1 asli menyelesaikan instalasi GUI, sedangkan LabKita 0.3 tetap gagal baik dengan 3D acceleration mati maupun hidup, sehingga 3D bukan penyebab. Penyebab kegagalan belum ditemukan. Kernel 0.2 kini <code>7.0.0-31</code> (audit lama <code>7.0.0-43</code>): ISO selalu berisi -31; -43 kemungkinan dari langkah update online installer pada 16 Nov yang tidak tampak pada 19 Nov (alasan tidak terbukti). Spot-check 9 screenshot benchmark tidak menemukan selisih angka. Detail: docs/CONTROL-EXPERIMENT.md.", body_style))
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
    story.append(Paragraph("1. <b>Keluaran Produk Tercapai:</b> Berkas citra bootable <code>labkita-linux-0.3-amd64.iso</code> (~6,07 GiB, SHA256 <code>21f38dc1...</code>) berhasil dibangun, lolos verifikasi <code>md5sum</code> 957/957 dan <code>casper-md5check</code>, serta diinstal ke disk virtual melalui <code>subiquity.cmd.tui</code>.", bullet_style))
    story.append(Paragraph("2. <b>Perbaikan Utama 0.3 Terbukti Berhasil:</b> Panduan lokal di <code>~/Dokumen/Panduan-LabKita</code> berhasil dibuka langsung oleh Firefox Snap dan diverifikasi pembacaannya oleh <code>labkita-check</code>, bug <code>printf --</code> pada <code>labkita-postinstall</code> tuntas, dan seluruh label rilis 0.3 konsisten di <code>os-release</code>, sambutan, serta Pengaturan Tentang.", bullet_style))
    story.append(Paragraph("3. <b>Visi Pemrograman Offline & Isolasi Terpenuhi:</b> Pengujian dengan jaringan dimatikan total (<code>nmcli networking off</code>) membuktikan compiler GCC (<code>~/Praktikum</code>), Python 3, multiprocessing, isolasi <code>0700</code>, akun non-sudo, serta tmpfs <code>/run/labkita</code> <code>1777</code> aktif.", bullet_style))
    story.append(Paragraph("4. <b>Integritas Data Empiris 5x Ukur & Variabel Kernel:</b> Dalam 5x pengukuran per versi di VM identik, konsumsi RAM 0.3 rata-rata tercatat 1.058,2 MiB (rentang 1.046–1.067 MiB) dibanding 0.1 (1.038,2 MiB; 1.016–1.056) dan 0.2 (1.068,2 MiB; 1.058–1.080), serta waktu boot 0.3 rata-rata 8,808s (rentang 8,460–9,014s) dibanding 0.1 (8,460s; 8,359–8,676s) dan 0.2 (9,317s; 9,072–9,458s). Karena perbedaan kernel (<code>7.0.0-43-generic</code> vs <code>7.0.0-31-generic</code>) dan tumpang tindih rentang, tidak ada klaim lebih ringan maupun lebih cepat.", bullet_style))

    story.append(Paragraph("5.2 Keterbatasan dan Kegagalan Terbuka pada Rilis 0.3", h2_style))
    story.append(Paragraph(
        "Berdasarkan pengujian nyata pada ISO 0.3, terdapat kendala terbuka yang tetap dilaporkan apa adanya:",
        body_style
    ))
    story.append(Paragraph("• <b>Installer Grafis GUI (<code>ubuntu-desktop-bootstrap</code>):</b> Meski <code>casper-md5check</code> sudah lulus (<code>pass</code>), antarmuka grafis bootstrap tetap gagal menampilkan dialog <i>'Ada yang salah'</i> saat live boot, sehingga instalasi memerlukan fallback <code>subiquity.cmd.tui</code>.", bullet_style))
    story.append(Paragraph("• <b>Autologin Sesi Live:</b> Sesi live belum langsung masuk pengguna autologin tanpa wizard, melainkan membuka <code>gnome-initial-setup</code> untuk pembuatan pengguna live tanpa <code>NOPASSWD:ALL</code>.", bullet_style))
    story.append(Paragraph("• <b>Detail Minor Ikon Dock & Tmpfs Noexec:</b> Pada tema WhiteSur 0.3, slot ikon Terminal & Berkas di dock terlihat redup saat tidak aktif, dan flag <code>noexec</code> pada <code>/run</code> mengharuskan eksekusi biner C di <code>~/Praktikum</code>.", bullet_style))

    story.append(Paragraph("5.3 Saran Pengembangan Rilis Selanjutnya (LabKita Linux 0.4)", h2_style))
    story.append(Paragraph(
        "Untuk pengembangan rilis berikutnya, disarankan perbaikan terfokus berikut:",
        body_style
    ))
    story.append(Paragraph("1. <b>Perbaikan Konfigurasi Live Autologin & Bootstrap GUI:</b> Mengembalikan konfigurasi sesi live autologin <code>casper</code> standar Ubuntu 24.04 tanpa memicu <code>gnome-initial-setup</code> dan menguji kompatibilitas grafis <code>ubuntu-desktop-bootstrap</code>.", bullet_style))
    story.append(Paragraph("2. <b>Audit Ikon Dock WhiteSur:</b> Menyelaraskan daftar aplikasi favorit dock (<code>firefox_firefox.desktop</code> & cache ikon tema WhiteSur) agar seluruh ikon dock tampil tajam sejak login pertama.", bullet_style))
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
        "• <b>Berkas Citra ISO Resmi:</b> <code>labkita-linux-0.3-amd64.iso</code> (Ukuran: 6.520.272.896 bytes / ~6,07 GiB).<br/>"
        "• <b>Verifikasi SHA256:</b> <code>21f38dc158a010e6f80920274dd7b8cd8f3e0d7f5e91283a310e98e53f045387</code><br/>"
        "• <b>Verifikasi MD5:</b> <code>521f315f62a6c7cd08a31d40ad8c9fb5</code><br/>"
        "• <b>Versi Cubic:</b> <code>2026.09.110-release~202609120048~ubuntu24.04.1</code>",
        body_style
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Lampiran 2: Naskah dan Tautan Video Demonstrasi (3–5 Menit)", h2_style))
    story.append(Paragraph(
        "Sesuai ketentuan Bagian 5 Poin 4, video demonstrasi berdurasi 4 menit 30 detik disiapkan dengan struktur alur kerja: "
        "(1) Pembukaan, booting GRUB 0.3 Bahasa Indonesia & penjelasan jujur installer GUI gagal + fallback subiquity TUI, (2) Desktop 0.3 terinstal (tema WhiteSur, dock, Berkas & Tentang LabKita Linux 0.3), "
        "(3) Eksekusi labkita-check (termasuk uji baca sandbox Firefox Snap AppArmor OK) dan pembukaan panduan di Firefox Snap, "
        "(4) Pembuktian offline total tanpa jaringan (GCC di ~/Praktikum & multiprocessing Python) serta fix printf -- pada labkita-postinstall, (5) Isolasi folder 0700 dan akun praktikan non-sudo, "
        "serta (6) Perbandingan empiris 5x pengukuran RAM free -m dan boot time systemd-analyze (0.1 vs 0.2 vs 0.3 terinstal beserta variabel kernel).<br/>"
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
