import os
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# Page and typography constants matched strictly to the reference UNSIL academic layout
PAGE_SIZE = (595.44, 841.68)  # 8.27 x 11.69 inch (A4)
LEFT_MARGIN = 113.4           # 4.0 cm
RIGHT_MARGIN = 85.04          # 3.0 cm
TOP_MARGIN = 112.6            # Top frame edge at y = 729.08
BOTTOM_MARGIN = 85.04         # 3.0 cm
CONTENT_WIDTH = PAGE_SIZE[0] - LEFT_MARGIN - RIGHT_MARGIN  # 397.0 pt
FRAME_HEIGHT = PAGE_SIZE[1] - TOP_MARGIN - BOTTOM_MARGIN   # 644.04 pt

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSET_LOGO = ROOT_DIR / "docs" / "assets" / "unsil-logo.png"
EVIDENCE_DIR = ROOT_DIR / "docs" / "evidence"
OUTPUT_PDF = ROOT_DIR / "docs" / "LAPORAN-PROYEK-LABKITA.pdf"

DRIVE_ISO_URL = "https://drive.google.com/drive/folders/10ZI4s-CYWAKA8GsHbTBCZm-p0QArp8lM?usp=sharing"


def register_report_fonts():
    """Register LiberationSerif (preferred) or metrically equivalent serif fallback."""
    candidates = [
        (
            Path("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"),
            Path("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"),
        ),
        (
            Path("/usr/share/fonts/liberation/LiberationSerif-Regular.ttf"),
            Path("/usr/share/fonts/liberation/LiberationSerif-Bold.ttf"),
        ),
        (
            Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "times.ttf",
            Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "timesbd.ttf",
        ),
    ]
    for reg_path, bold_path in candidates:
        if reg_path.exists() and bold_path.exists():
            pdfmetrics.registerFont(TTFont("BodySerif", str(reg_path)))
            pdfmetrics.registerFont(TTFont("BodySerif-Bold", str(bold_path)))
            pdfmetrics.registerFontFamily(
                "BodySerif",
                normal="BodySerif",
                bold="BodySerif-Bold",
                italic="BodySerif",
                boldItalic="BodySerif-Bold",
            )
            return "BodySerif", "BodySerif-Bold"
    return "Times-Roman", "Times-Bold"


FONT_REGULAR, FONT_BOLD = register_report_fonts()


def build_styles():
    styles = {}
    styles["CoverTitleLarge"] = ParagraphStyle(
        "CoverTitleLarge",
        fontName=FONT_BOLD,
        fontSize=16,
        leading=22.7,
        alignment=TA_CENTER,
    )
    styles["CoverBold"] = ParagraphStyle(
        "CoverBold",
        fontName=FONT_BOLD,
        fontSize=12,
        leading=13.8,
        alignment=TA_CENTER,
    )
    styles["CoverRegular"] = ParagraphStyle(
        "CoverRegular",
        fontName=FONT_REGULAR,
        fontSize=12,
        leading=13.8,
        alignment=TA_CENTER,
    )
    styles["CoverMediumBold"] = ParagraphStyle(
        "CoverMediumBold",
        fontName=FONT_BOLD,
        fontSize=14,
        leading=17.4,
        alignment=TA_CENTER,
    )
    styles["ChapterHeading"] = ParagraphStyle(
        "ChapterHeading",
        fontName=FONT_BOLD,
        fontSize=12,
        leading=13.8,
        alignment=TA_CENTER,
        spaceAfter=16.0,
    )
    styles["SubHeading"] = ParagraphStyle(
        "SubHeading",
        fontName=FONT_BOLD,
        fontSize=12,
        leading=13.8,
        leftIndent=32.7,
        firstLineIndent=-14.7,
        spaceBefore=6.0,
        spaceAfter=3.2,
    )
    styles["LampiranHeading"] = ParagraphStyle(
        "LampiranHeading",
        fontName=FONT_BOLD,
        fontSize=12,
        leading=13.8,
        leftIndent=18.0,
        spaceBefore=6.0,
        spaceAfter=3.2,
    )
    styles["Body"] = ParagraphStyle(
        "Body",
        fontName=FONT_REGULAR,
        fontSize=12,
        leading=13.8,
        firstLineIndent=35.4,
        alignment=TA_JUSTIFY,
        spaceAfter=4.9,
    )
    styles["BodyKeepNext"] = ParagraphStyle(
        "BodyKeepNext",
        parent=styles["Body"],
        keepWithNext=True,
    )
    styles["BodyNoIndent"] = ParagraphStyle(
        "BodyNoIndent",
        fontName=FONT_REGULAR,
        fontSize=12,
        leading=13.8,
        alignment=TA_JUSTIFY,
        spaceAfter=4.9,
    )
    styles["Numbered"] = ParagraphStyle(
        "Numbered",
        fontName=FONT_REGULAR,
        fontSize=12,
        leading=13.8,
        leftIndent=53.4,
        bulletIndent=35.4,
        alignment=TA_JUSTIFY,
        spaceAfter=4.9,
    )
    styles["BibItem"] = ParagraphStyle(
        "BibItem",
        fontName=FONT_REGULAR,
        fontSize=12,
        leading=13.8,
        leftIndent=36.0,
        firstLineIndent=-36.0,
        alignment=TA_LEFT,
        spaceAfter=6.0,
    )
    styles["Caption"] = ParagraphStyle(
        "Caption",
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=11.5,
        alignment=TA_CENTER,
        spaceBefore=4.0,
        spaceAfter=6.0,
    )
    styles["TblHdr"] = ParagraphStyle(
        "TblHdr",
        fontName=FONT_BOLD,
        fontSize=10,
        leading=11.5,
        alignment=TA_CENTER,
    )
    styles["TblCellCenter"] = ParagraphStyle(
        "TblCellCenter",
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=11.5,
        alignment=TA_CENTER,
    )
    styles["TblCellLeft"] = ParagraphStyle(
        "TblCellLeft",
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=11.5,
        alignment=TA_LEFT,
    )
    styles["BenchHdr"] = ParagraphStyle(
        "BenchHdr",
        fontName=FONT_BOLD,
        fontSize=8.5,
        leading=10.0,
        alignment=TA_CENTER,
    )
    styles["BenchCellCenter"] = ParagraphStyle(
        "BenchCellCenter",
        fontName=FONT_REGULAR,
        fontSize=8.5,
        leading=10.0,
        alignment=TA_CENTER,
    )
    styles["BenchCellLeft"] = ParagraphStyle(
        "BenchCellLeft",
        fontName=FONT_REGULAR,
        fontSize=8.5,
        leading=10.0,
        alignment=TA_LEFT,
    )
    return styles


class TOCMarker(Flowable):
    """Zero-height marker recording the rendered page number for a TOC entry."""

    def __init__(self, key):
        super().__init__()
        self.key = key
        self.width = 0
        self.height = 0

    def draw(self):
        pass


class TocEntryFlowable(Flowable):
    """Single TOC entry with optional sub-indent, word wrapping, dot leader, and page number."""

    def __init__(self, title, page_num, level=0, font_name=FONT_REGULAR, font_size=12, row_height=17.8):
        super().__init__()
        self.title = title
        self.page_str = str(page_num)
        self.indent = 10.8 if level > 0 else 0.0
        self.font_name = font_name
        self.font_size = font_size
        self.line_height = 13.8
        self.row_height = row_height
        self.lines = self._wrap_lines()
        self.width = CONTENT_WIDTH
        self.height = self.row_height if len(self.lines) == 1 else (len(self.lines) * self.line_height + 4.0)

    def _wrap_lines(self):
        max_w = CONTENT_WIDTH - self.indent - 34.0
        words = self.title.split()
        lines = []
        current = ""
        for w in words:
            trial = f"{current} {w}".strip()
            if not current or stringWidth(trial, self.font_name, self.font_size) <= max_w:
                current = trial
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)
        return lines or [""]

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFont(self.font_name, self.font_size)
        c.setFillColor(colors.black)
        y_top = self.height - 12.0
        for idx, line in enumerate(self.lines):
            y = y_top - idx * self.line_height
            c.drawString(self.indent, y, line)
            if idx == len(self.lines) - 1:
                text_end = self.indent + stringWidth(line, self.font_name, self.font_size)
                page_w = stringWidth(self.page_str, self.font_name, self.font_size)
                page_x = CONTENT_WIDTH - page_w
                dot_w = stringWidth(".", self.font_name, self.font_size)
                start_x = text_end + 3.0
                avail = (page_x - 4.0) - start_x
                if avail > dot_w:
                    num_dots = int(avail // dot_w)
                    c.drawString(start_x, y, "." * num_dots)
                c.drawString(page_x, y, self.page_str)
        c.restoreState()


class ReportDocTemplate(BaseDocTemplate):
    """Two-pass capable document template collecting TOC page numbers cleanly."""

    def __init__(self, filename, toc_map, **kwargs):
        super().__init__(filename, **kwargs)
        self.toc_map = toc_map
        frame = Frame(
            LEFT_MARGIN,
            BOTTOM_MARGIN,
            CONTENT_WIDTH,
            FRAME_HEIGHT,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id="main",
        )
        self.addPageTemplates([PageTemplate(id="main", frames=[frame])])

    def afterFlowable(self, flowable):
        if isinstance(flowable, TOCMarker):
            self.toc_map[flowable.key] = self.page


def make_grid_table(data, col_widths, pad_lr=5.4, repeat_rows=1):
    tbl = Table(data, colWidths=col_widths, repeatRows=repeat_rows)
    tbl.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), pad_lr),
                ("RIGHTPADDING", (0, 0), (-1, -1), pad_lr),
                ("TOPPADDING", (0, 0), (-1, -1), 3.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ]
        )
    )
    return tbl


def num_item(num_str, html_text, style):
    return Paragraph(f"<bullet>{num_str}</bullet>{html_text}", style)


def evidence_figure(img_name, caption_text, styles):
    img_path = EVIDENCE_DIR / img_name
    img = Image(str(img_path), width=290.0, height=181.25)
    img.hAlign = "CENTER"
    return KeepTogether([Spacer(1, 6.0), img, Paragraph(caption_text, styles["Caption"])])


def build_story(styles, toc_pages):
    story = []

    def p_body(text):
        return Paragraph(text, styles["Body"])

    def toc_row(key, label, level=0):
        return TocEntryFlowable(label, toc_pages.get(key, "?"), level=level)

    # =========================================================================
    # PAGE 1: COVER
    # =========================================================================
    story.append(Spacer(1, 1.0))
    story.append(Paragraph("LAPORAN AKHIR FINAL PROJECT", styles["CoverTitleLarge"]))
    story.append(Paragraph("MATA KULIAH SISTEM OPERASI", styles["CoverTitleLarge"]))
    story.append(Spacer(1, 1.5))
    story.append(
        Paragraph(
            "LabKita Linux 0.5: Pengembangan Distribusi Linux<br/>"
            "Turunan Ubuntu 24.04 LTS untuk Praktikum Pemrograman<br/>"
            "Dasar Mandiri Tanpa Ketergantungan Internet",
            styles["CoverBold"],
        )
    )
    story.append(Spacer(1, 3.0))
    story.append(
        Paragraph(
            "Laporan ini disusun untuk memenuhi salah satu tugas mata kuliah<br/>Sistem Operasi",
            styles["CoverRegular"],
        )
    )
    story.append(Spacer(1, 14.0))
    story.append(Paragraph("Semester Ganjil Tahun Akademik 2026/2027", styles["CoverMediumBold"]))
    story.append(Spacer(1, 11.0))
    story.append(Paragraph("Dosen Pengampu : Muhammad Sidik Asyaky, S.T., M.T.", styles["CoverBold"]))
    story.append(
        Paragraph("Kategori Proyek : Kategori A \u2014 Distro Linux dengan Visi Tertentu", styles["CoverBold"])
    )
    story.append(Spacer(1, 12.0))
    story.append(Paragraph("Oleh:", styles["CoverBold"]))
    story.append(
        Paragraph(
            "Dafa Zahran (257006111188)<br/>"
            "Rafly Fauzi Pratama (257006111152)<br/>"
            "Muhammad Ilham Rizky (257006111154)<br/>"
            "Vadien Athallah Lukman (257006111160)",
            styles["CoverBold"],
        )
    )
    story.append(Spacer(1, 15.0))
    if ASSET_LOGO.exists():
        logo = Image(str(ASSET_LOGO), width=153.0, height=153.0)
        logo.hAlign = "CENTER"
        story.append(logo)
    story.append(Spacer(1, 75.0))
    story.append(
        Paragraph(
            "PROGRAM STUDI INFORMATIKA<br/>"
            "FAKULTAS TEKNIK<br/>"
            "UNIVERSITAS SILIWANGI<br/>"
            "TASIKMALAYA<br/>"
            "2026",
            styles["CoverMediumBold"],
        )
    )
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: DAFTAR ISI
    # =========================================================================
    story.append(Paragraph("DAFTAR ISI", styles["ChapterHeading"]))
    toc_entries = [
        ("bab1", "BAB I PENDAHULUAN", 0),
        ("bab1a", "A. Latar Belakang Masalah", 1),
        ("bab1b", "B. Visi dan Tujuan Produk", 1),
        ("bab1c", "C. Sasaran Pengguna", 1),
        ("bab1d", "D. Ruang Lingkup Proyek", 1),
        ("bab1e", "E. Pembagian Tugas dan Kontribusi Anggota Kelompok", 1),
        ("bab2", "BAB II LANDASAN TEORI SISTEM OPERASI", 0),
        ("bab2a", "A. Konsep Manajemen Proses dan Multiprocessing", 1),
        ("bab2b", "B. Manajemen Memori dan Virtual Filesystem (Tmpfs)", 1),
        ("bab2c", "C. Keamanan Sistem Operasi dan Privilege Separation", 1),
        ("bab2d", "D. Inisialisasi Sistem dan Layanan Daemon (Systemd)", 1),
        ("bab2e", "E. Arsitektur Live CD dan OverlayFS", 1),
        ("bab3", "BAB III PERANCANGAN SISTEM", 0),
        ("bab3a", "A. Arsitektur LabKita Linux", 1),
        ("bab3b", "B. Alur Kerja Pembuatan ISO (Build WSL 0.5 & Arsip Cubic)", 1),
        ("bab3c", "C. Rancangan Antarmuka dan Pengalaman Pengguna (UI/UX)", 1),
        ("bab3d", "D. Spesifikasi Perangkat Keras dan Perangkat Lunak", 1),
        ("bab4", "BAB IV IMPLEMENTASI DAN PENGUJIAN", 0),
        ("bab4a", "A. Langkah-Langkah Implementasi", 1),
        ("bab4b", "B. Skenario dan Hasil Pengujian Fungsional", 1),
        ("bab4c", "C. Pengukuran Kinerja dan Tolok Ukur Empiris (0.1 vs 0.2 vs 0.3 vs 0.4 vs 0.5)", 1),
        ("bab4d", "D. Pembahasan Temuan Teknis: Fix Autologin, Installer GUI 0.5 & Verifikasi Build", 1),
        ("bab5", "BAB V PENUTUP", 0),
        ("bab5a", "A. Kesimpulan", 1),
        ("bab5b", "B. Keterbatasan dan Catatan Jujur Rilis 0.5", 1),
        ("bab5c", "C. Saran Pengembangan Lanjutan", 1),
        ("dafpus", "DAFTAR PUSTAKA", 0),
        ("lamp", "LAMPIRAN", 0),
        ("lamp1", "Lampiran 1: Tautan Repositori Kode Sumber dan Berkas ISO", 1),
        ("lamp2", "Lampiran 2: Naskah dan Tautan Video Demonstrasi", 1),
        ("lamp3", "Lampiran 3: Pernyataan Kejujuran Akademik dan Penggunaan AI", 1),
    ]
    for key, label, lvl in toc_entries:
        story.append(toc_row(key, label, lvl))
    story.append(PageBreak())

    # =========================================================================
    # BAB I PENDAHULUAN
    # =========================================================================
    story.append(TOCMarker("bab1"))
    story.append(Paragraph("BAB I<br/>PENDAHULUAN", styles["ChapterHeading"]))

    story.append(TOCMarker("bab1a"))
    story.append(Paragraph("A. Latar Belakang Masalah", styles["SubHeading"]))
    story.append(
        p_body(
            "Praktikum pemrograman dasar dan sistem operasi merupakan mata kuliah fundamental dalam kurikulum "
            "ilmu komputer dan teknik informatika. Pada pelaksanaannya di laboratorium komputer kampus, "
            "kelancaran sesi praktikum seringkali menghadapi kendala infrastruktur jaringan internet. "
            "Ketergantungan terhadap koneksi internet untuk mengunduh pustaka (library), compiler, paket "
            "perangkat lunak, maupun modul dokumentasi kerap memicu hambatan teknis saat bandwidth kampus "
            "mengalami penurunan performa atau gangguan mendadak."
        )
    )
    story.append(
        p_body(
            "Di sisi lain, ketersediaan koneksi internet terbuka di komputer praktikum sering kali menjadi "
            "sumber distraksi bagi mahasiswa. Akses web yang tidak terbatas memudahkan mahasiswa membuka media "
            "sosial, video streaming, atau platform permainan daring saat sesi penyampaian materi berlangsung. "
            "Selain itu, asisten laboratorium dibebani oleh tugas administratif berulang untuk melakukan "
            "instalasi perangkat lunak (seperti GCC, Python, dan text editor) di puluhan unit komputer setiap "
            "semester baru dimulai."
        )
    )

    story.append(TOCMarker("bab1b"))
    story.append(Paragraph("B. Visi dan Tujuan Produk", styles["SubHeading"]))
    story.append(
        p_body(
            "Proyek LabKita Linux hadir sebagai wujud nyata penerapan prinsip-prinsip sistem operasi dalam "
            "menyelesaikan permasalahan di lingkungan akademik. Visi dari LabKita Linux adalah menghadirkan "
            "sistem operasi praktikum mandiri (self-contained) yang siap pakai sejak detik pertama booting "
            "tanpa membutuhkan koneksi internet sama sekali (Ruang belajar. Siap offline.)."
        )
    )
    story.append(p_body("Tujuan utama pengembangan LabKita Linux meliputi:"))
    story.append(
        num_item(
            "1.",
            "Kemandirian Offline Total: Mengintegrasikan seluruh compiler (GCC, G++), interpreter (Python 3), "
            "build automation (Make), debugger, editor kode (Geany), serta manual sistem (man-db) langsung di "
            "dalam berkas citra ISO bootable.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "2.",
            "Keamanan dan Isolasi Hak Akses: Mengimplementasikan pembatasan hak akses berbasis pengguna "
            "(privilege separation) di mana akun praktikan tidak memiliki izin administratif (non-sudo) dan "
            "folder kerja mahasiswa terlindungi secara ketat.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "3.",
            "Efisiensi Penyimpanan Sesi: Menyediakan area kerja temporer berbasis memori virtual (tmpfs) "
            "dengan mekanisme sticky bit yang otomatis bersih saat restart, menjaga integritas dan kebersihan "
            "sistem lab komputer.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "4.",
            "Kemudahan Distribusi: Menyajikan format berkas ISO hibrida standar yang dapat dijalankan secara "
            "langsung via Live USB, instalasi fisik, maupun mesin virtual (VMware Workstation dan VirtualBox).",
            styles["Numbered"],
        )
    )

    story.append(TOCMarker("bab1c"))
    story.append(Paragraph("C. Sasaran Pengguna", styles["SubHeading"]))
    story.append(p_body("Sasaran pengguna produk LabKita Linux terbagi atas dua kelompok utama:"))
    story.append(
        num_item(
            "1.",
            "Mahasiswa Praktikan: Memperoleh lingkungan belajar yang seragam, stabil, bebas distraksi, dan "
            "siap digunakan untuk menulis kode C, C++, algoritma struktur data, serta simulasi multiproses "
            "sistem operasi.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "2.",
            "Asisten Laboratorium dan Dosen: Mengeliminasi waktu persiapan perangkat lunak di awal semester, "
            "menjamin kepatuhan akademik selama praktikum/ujian, serta memudahkan standardisasi evaluasi "
            "penilaian praktikum.",
            styles["Numbered"],
        )
    )

    story.append(TOCMarker("bab1d"))
    story.append(Paragraph("D. Ruang Lingkup Proyek", styles["SubHeading"]))
    story.append(p_body("Ruang lingkup pengerjaan LabKita Linux versi 0.5 dibatasi pada:"))
    story.append(
        num_item(
            "1.",
            "Basis distribusi menggunakan Ubuntu Desktop 24.04.5 LTS (Noble Numbat) arsitektur x86_64; "
            "instalasi bersih rilis 0.1 dan 0.2 berjalan pada kernel Linux 7.0.0-31-generic, sedangkan 0.3, "
            "0.4, dan 0.5 berjalan pada 7.0.0-43-generic.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "2.",
            "Perangkat lunak pemrograman mencakup GCC 13.3.0, G++ 13.3.0, Make 4.3, Python 3.12.3, "
            "Geany 2.0, Git 2.43, Nano, dan pustaka manpages-dev.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "3.",
            "Rilis final 0.5 (tag v0.5-iso) dibangun secara reproducible di WSL melalui skrip "
            "tools/build_v05.py (berbasis resep Bisect #3, non-Cubic) dengan normalisasi LF dan format "
            ".disk/info bertanda kutip \"Noble Numbat\", beserta regenerasi md5sum.txt pasca-remastering "
            "(sementara arsip 0.1\u20130.4 sebelumnya dibangun melalui Cubic versi "
            "2026.09.110-release~202609120048~ubuntu24.04.1).",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "4.",
            "Pengujian dilakukan secara empiris pada hypervisor VMware Workstation 25 (disk kosong 40 GB, "
            "akselerasi 3D dimatikan) mencakup verifikasi integritas ISO 0.5 (1016/1016 OK), autologin live "
            "ubuntu & instalasi GUI normal (ubuntu-desktop-bootstrap) selesai hingga restart (plus TUI "
            "sebagai cadangan), labkita-check (termasuk uji baca Firefox Snap AppArmor OK), "
            "labkita-postinstall (grup labkita-praktikum), pengujian offline, serta 5 kali tolok ukur RAM dan "
            "waktu boot per versi (0.1\u20130.5).",
            styles["Numbered"],
        )
    )

    story.append(TOCMarker("bab1e"))
    story.append(Paragraph("E. Pembagian Tugas dan Kontribusi Anggota Kelompok", styles["SubHeading"]))
    story.append(
        p_body(
            "Sesuai dengan ketentuan rubrik final project, tim kelompok terdiri atas mahasiswa dengan "
            "pembagian peran yang terukur dan adil:"
        )
    )
    # Bab I.E table preserved 100% verbatim unchanged as requested
    team_rows = [
        [
            Paragraph("No", styles["TblHdr"]),
            Paragraph("Nama", styles["TblHdr"]),
            Paragraph("NPM", styles["TblHdr"]),
            Paragraph("Peran", styles["TblHdr"]),
            Paragraph("Rincian Tugas dan Kontribusi", styles["TblHdr"]),
        ],
        [
            Paragraph("1", styles["TblCellCenter"]),
            Paragraph("Dafa Zahran", styles["TblCellLeft"]),
            Paragraph("257006111188", styles["TblCellCenter"]),
            Paragraph(
                "Ketua Kelompok, Manajer Proyek & Integrasi (Build/Integrasi)",
                styles["TblCellLeft"],
            ),
            Paragraph(
                "Mengoordinasikan pembagian modul tim, build WSL (tools/build_v05.py untuk 0.5; Cubic untuk "
                "arsip 0.1\u20130.4), regenerasi manifest md5sum & mastering ISO (labkita-linux-0.5-amd64.iso), "
                "manajemen repositori GitHub (https://github.com/luvices/labkita), dan keselarasan luaran tugas.",
                styles["TblCellLeft"],
            ),
        ],
        [
            Paragraph("2", styles["TblCellCenter"]),
            Paragraph("Rafly Fauzi Pratama", styles["TblCellLeft"]),
            Paragraph("257006111152", styles["TblCellCenter"]),
            Paragraph("Pengembang Inti (Core Developer) & Toolchain", styles["TblCellLeft"]),
            Paragraph(
                "Mengembangkan skrip kustomisasi Cubic (scripts/customize.sh), instalasi dan konfigurasi "
                "toolchain pemrograman (GCC, G++, Python, Geany), serta perancangan dan pengujian suite "
                "diagnostik labkita-check.",
                styles["TblCellLeft"],
            ),
        ],
        [
            Paragraph("3", styles["TblCellCenter"]),
            Paragraph("Muhammad Ilham Rizky", styles["TblCellLeft"]),
            Paragraph("257006111154", styles["TblCellCenter"]),
            Paragraph("Sistem, Keamanan & Penguji Kualitas (Sys, Sec & QA)", styles["TblCellLeft"]),
            Paragraph(
                "Merancang unit systemd labkita-runtime.service, otomasi skrip labkita-postinstall, isolasi "
                "izin 0700, pembatasan non-sudo, serta menjalankan pengujian tolok ukur (RAM free -m dan "
                "boot time systemd-analyze).",
                styles["TblCellLeft"],
            ),
        ],
        [
            Paragraph("4", styles["TblCellCenter"]),
            Paragraph("Vadien Athallah Lukman", styles["TblCellLeft"]),
            Paragraph("257006111160", styles["TblCellCenter"]),
            Paragraph("Pengembang Antarmuka, Dokumentasi & Media (UI/UX & Docs)", styles["TblCellLeft"]),
            Paragraph(
                "Mendesain identitas visual (wallpaper SVG LabKita, konfigurasi dconf), modul materi panduan "
                "praktikum dan contoh kode (C & Python multiprocessing), penyusunan Laporan Proyek Akhir "
                "(Bab I-V PDF), slide presentasi (PPTX), dan naskah video demo.",
                styles["TblCellLeft"],
            ),
        ],
    ]
    story.append(make_grid_table(team_rows, [26.0, 62.0, 72.0, 82.0, 155.0], pad_lr=5.4, repeat_rows=1))
    story.append(PageBreak())

    # =========================================================================
    # BAB II LANDASAN TEORI SISTEM OPERASI (unchanged)
    # =========================================================================
    story.append(TOCMarker("bab2"))
    story.append(Paragraph("BAB II<br/>LANDASAN TEORI SISTEM OPERASI", styles["ChapterHeading"]))

    story.append(TOCMarker("bab2a"))
    story.append(Paragraph("A. Konsep Manajemen Proses dan Multiprocessing", styles["SubHeading"]))
    story.append(
        p_body(
            "Proses adalah sebuah program yang sedang dieksekusi di dalam memori utama oleh CPU. Di dalam "
            "sistem operasi modern berbasis Unix/Linux, setiap proses memiliki Process Identifier (PID) unik, "
            "status eksekusi (Running, Ready, Blocked), program counter, stack, serta ruang alamat memori "
            "sendiri. Penciptaan proses baru pada Linux menggunakan system call fork() yang menduplikasi "
            "address space proses induk (parent process) ke proses anak (child process). LabKita Linux "
            "menyertakan modul praktikum processes.py yang memanfaatkan modul multiprocessing Python untuk "
            "mendemonstrasikan pembagian beban komputasi secara paralel antar proses anak independen dengan "
            "PID berbeda."
        )
    )

    story.append(TOCMarker("bab2b"))
    story.append(Paragraph("B. Manajemen Memori dan Virtual Filesystem (Tmpfs)", styles["SubHeading"]))
    story.append(
        p_body(
            "Memori utama (RAM) adalah sumber daya kritis yang dikelola oleh kernel melalui mekanisme virtual "
            "memory management dan paging. Linux menyediakan antarmuka tmpfs (temporary filesystem), yaitu "
            "sebuah virtual filesystem yang memetakan direktori tertentu langsung ke dalam memori RAM dinamis "
            "dan swap, alih-alih menyimpannya pada media disk persisten. Karakteristik utama tmpfs adalah "
            "kecepatan operasi I/O yang sangat tinggi mendekati throughput RAM fisik, serta sifatnya yang "
            "sepenuhnya volatil (seluruh data akan terhapus seketika saat daya sistem mati). LabKita Linux "
            "memanfaatkan konsep ini pada direktori /run/labkita yang dialokasikan sebagai ruang kerja "
            "sementara praktikum dengan atribut keamanan sticky bit (izin 1777), memungkinkan setiap praktikan "
            "menulis berkas sementara tanpa risiko memenuhi media disk persisten."
        )
    )

    story.append(TOCMarker("bab2c"))
    story.append(Paragraph("C. Keamanan Sistem Operasi dan Privilege Separation", styles["SubHeading"]))
    story.append(
        p_body(
            "Keamanan sistem operasi bertumpu pada prinsip pembatasan hak istimewa (Principle of Least "
            "Privilege), yaitu setiap entitas pengguna hanya diberikan izin minimum yang diperlukan untuk "
            "menyelesaikan tugasnya. Pada Linux, hak akses dibedakan antara administrator sistem (super-user "
            "root dengan UID 0) dan pengguna biasa (unprivileged user dengan UID \u2265 1000). Mekanisme "
            "kontrol akses diskresioner (Discretionary Access Control - DAC) menerapkan bit perizinan: Read "
            "(r=4), Write (w=2), dan Execute (x=1) untuk pemilik (User), grup (Group), dan pengguna lain "
            "(Others). LabKita Linux menerapkan DAC ketat mode 0700 (drwx------) pada folder /home/praktikan "
            "guna mengisolasi pekerjaan mahasiswa, serta mengecualikan praktikan dari file konfigurasi "
            "/etc/sudoers untuk mencegah eskalasi hak akses."
        )
    )

    story.append(TOCMarker("bab2d"))
    story.append(Paragraph("D. Inisialisasi Sistem dan Layanan Daemon (Systemd)", styles["SubHeading"]))
    story.append(
        p_body(
            "Setelah kernel Linux selesai melakukan bootstrap hardware, kernel akan mengeksekusi proses "
            "inisialisasi pertama yaitu systemd (PID 1). Systemd bertindak sebagai init system dan service "
            "manager yang mengatur siklus hidup daemon, dependensi layanan, serta target sistem (seperti "
            "multi-user.target dan graphical.target). Pada LabKita Linux, dibuat sebuah unit layanan kustom "
            "labkita-runtime.service bertipe oneshot yang diinisialisasi otomatis saat boot untuk memastikan "
            "direktori memori virtual /run/labkita selalu tercipta dengan kepemilikan dan hak akses yang "
            "benar sebelum pengguna login ke sesi grafis."
        )
    )

    story.append(TOCMarker("bab2e"))
    story.append(Paragraph("E. Arsitektur Live CD dan OverlayFS", styles["SubHeading"]))
    story.append(
        p_body(
            "Distribusi Linux Live berjalan di atas media read-only (citra ISO 9660) menggunakan mekanisme "
            "kompresi SquashFS dan penyatuan sistem berkas OverlayFS. OverlayFS menggabungkan dua lapisan "
            "direktori: lapisan bawah (lowerdir) yang bersifat read-only terkompresi dari file ISO, dan "
            "lapisan atas (upperdir) berupa writable layer di dalam memori RAM (dikenal sebagai /cow atau "
            "Copy-on-Write). Setiap modifikasi berkas yang dilakukan oleh pengguna saat menjalankan sesi live "
            "hanya akan dicatat pada lapisan RAM tanpa mengubah berkas citra asli pada media penyimpanan fisik."
        )
    )
    story.append(PageBreak())

    # =========================================================================
    # BAB III PERANCANGAN SISTEM
    # =========================================================================
    story.append(TOCMarker("bab3"))
    story.append(Paragraph("BAB III<br/>PERANCANGAN SISTEM", styles["ChapterHeading"]))

    story.append(TOCMarker("bab3a"))
    story.append(Paragraph("A. Arsitektur LabKita Linux", styles["SubHeading"]))
    story.append(
        p_body(
            "LabKita Linux dirancang dengan struktur berlapis yang mengedepankan isolasi dan keandalan operasional:"
        )
    )
    story.append(
        num_item(
            "1.",
            "Lapisan Kernel & Driver: Kernel 7.0.0-43-generic (0.3, 0.4, dan 0.5 terinstal; 7.0.0-31-generic "
            "pada 0.1 dan 0.2 bersih) dengan open-vm-tools.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "2.",
            "Lapisan Inisialisasi & Runtime: Systemd yang memuat layanan labkita-runtime.service untuk mount "
            "tmpfs /run/labkita dengan sticky bit 1777.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "3.",
            "Lapisan Toolchain Praktikum: Compiler C/C++ (GCC/G++), Python 3, debugger, dan editor Geany di /usr/bin.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "4.",
            "Lapisan Keamanan & Pengguna: labkita-postinstall mengatur akun non-sudo pada grup sistem "
            "labkita-praktikum (tanpa bentrok grup live labkita), izin 0700, & salinan "
            "~/Dokumen/Panduan-LabKita; pada live session 0.5, .disk/info diawali \"Ubuntu\" agar autologin "
            "memakai user standar ubuntu.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "5.",
            "Lapisan Antarmuka Pengguna: GNOME Shell 46 via dconf untuk tema WhiteSur, wallpaper LabKita, "
            "bahasa Indonesia penuh, dan dock aplikasi terpusat.",
            styles["Numbered"],
        )
    )

    story.append(TOCMarker("bab3b"))
    story.append(
        Paragraph("B. Alur Kerja Pembuatan ISO (Build WSL 0.5 & Arsip Cubic)", styles["SubHeading"])
    )
    story.append(
        p_body(
            "Setelah arsip 0.1\u20130.4 dibangun menggunakan Cubic "
            "(2026.09.110-release~202609120048~ubuntu24.04.1), rilis final LabKita Linux 0.5 (tag v0.5-iso) "
            "dibangun secara reproducible di WSL memakai skrip tools/build_v05.py (resep Bisect #3) dengan tahapan:"
        )
    )
    story.append(
        p_body(
            "Tahap 1 (ISO Source Verification): Memverifikasi ISO sumber resmi Ubuntu 24.04.5 LTS Desktop amd64 "
            "via SHA256 serta menyiapkan lapisan minimal.squashfs / minimal.standard.live.squashfs."
        )
    )
    story.append(
        p_body(
            "Tahap 2 (Payload Injection & CRLF Normalization): Memasukkan berkas kustomisasi LabKita 0.5 "
            "(grup sistem labkita-praktikum, systemd runtime, tema WhiteSur, /etc/skel/Dokumen/Panduan-LabKita, "
            "serta label os-release/labkita-release 0.5) dengan normalisasi akhiran baris CRLF ke LF melalui "
            ".gitattributes dan tools/build_v05.py."
        )
    )
    story.append(
        p_body(
            "Tahap 3 (.disk/info & Metadata Konfigurasi): Menulis .disk/info = Ubuntu 24.04 LabKita 0.5 "
            "\"Noble Numbat\" - Release amd64 (20261122) dan install-sources.yaml 0.5 agar kata pertama "
            "menjaga autologin live ubuntu dan tanda kutip codename terbaca normal oleh installer GUI."
        )
    )
    story.append(
        p_body(
            "Tahap 4 (Recompression, md5sum & Mastering): Setelah squashfs dan manifest final terbentuk, "
            "md5sum.txt diregenerasi untuk seluruh berkas (1016 berkas, mengecualikan boot.catalog dan "
            "eltorito.img) lalu xorriso memproduksi citra hybrid labkita-linux-0.5-amd64.iso."
        )
    )

    story.append(TOCMarker("bab3c"))
    story.append(
        Paragraph("C. Rancangan Antarmuka dan Pengalaman Pengguna (UI/UX)", styles["SubHeading"])
    )
    story.append(
        p_body(
            "Antarmuka versi 0.5 memakai tema open source WhiteSur GTK/Icon/Cursors, font Inter, tombol "
            "jendela di kiri, dock bawah terpusat, dan lokalisasi Bahasa Indonesia penuh (id_ID.UTF-8, "
            "Asia/Jakarta) tanpa aset proprietary Apple. Panduan lokal ditaruh di "
            "~/Dokumen/Panduan-LabKita/ agar lolos sandbox AppArmor Firefox Snap."
        )
    )

    story.append(TOCMarker("bab3d"))
    story.append(
        Paragraph("D. Spesifikasi Perangkat Keras dan Perangkat Lunak", styles["SubHeading"])
    )
    story.append(
        p_body(
            "Tabel berikut merangkum spesifikasi lingkungan pengembangan dan target mesin virtual pengujian:"
        )
    )
    spec_rows = [
        [
            Paragraph("Komponen", styles["TblHdr"]),
            Paragraph("Lingkungan Host Pembuat", styles["TblHdr"]),
            Paragraph("Spesifikasi Target VM Pengujian", styles["TblHdr"]),
        ],
        [
            Paragraph("Sistem Operasi", styles["TblCellCenter"]),
            Paragraph("Windows 11 64-bit & WSL Ubuntu (Build 0.5)", styles["TblCellLeft"]),
            Paragraph("LabKita 0.1 & 0.2 (7.0.0-31), 0.3\u20130.5 (7.0.0-43)", styles["TblCellLeft"]),
        ],
        [
            Paragraph("Hypervisor", styles["TblCellCenter"]),
            Paragraph("VMware Workstation 25.0.1", styles["TblCellLeft"]),
            Paragraph("Virtual Machine Hardware v21 (3D Off)", styles["TblCellLeft"]),
        ],
        [
            Paragraph("Prosesor / vCPU", styles["TblCellCenter"]),
            Paragraph("Prosesor Host x86_64", styles["TblCellLeft"]),
            Paragraph("2 Core vCPU Virtual", styles["TblCellLeft"]),
        ],
        [
            Paragraph("Kapasitas RAM", styles["TblCellCenter"]),
            Paragraph("16 GB RAM Host", styles["TblCellLeft"]),
            Paragraph("4.096 MB / 3.911 MiB Terbaca Linux", styles["TblCellLeft"]),
        ],
        [
            Paragraph("Penyimpanan", styles["TblCellCenter"]),
            Paragraph("SSD NVMe Host", styles["TblCellLeft"]),
            Paragraph("40 GB Growable Virtual Disk (SCSI, Disk Kosong)", styles["TblCellLeft"]),
        ],
        [
            Paragraph("Resolusi Layar", styles["TblCellCenter"]),
            Paragraph("1920 x 1080", styles["TblCellLeft"]),
            Paragraph("1280 x 800 (SVGA ScreenTarget)", styles["TblCellLeft"]),
        ],
    ]
    story.append(make_grid_table(spec_rows, [95.0, 130.0, 172.0], pad_lr=5.4, repeat_rows=1))
    story.append(PageBreak())

    # =========================================================================
    # BAB IV IMPLEMENTASI DAN PENGUJIAN
    # =========================================================================
    story.append(TOCMarker("bab4"))
    story.append(Paragraph("BAB IV<br/>IMPLEMENTASI DAN PENGUJIAN", styles["ChapterHeading"]))

    story.append(TOCMarker("bab4a"))
    story.append(Paragraph("A. Langkah-Langkah Implementasi", styles["SubHeading"]))
    story.append(
        p_body("Implementasi proyek LabKita Linux 0.5 diselesaikan melalui serangkaian tindakan terukur:")
    )
    story.append(
        num_item(
            "1.",
            "Normalisasi Payload & Konfigurasi 0.5: Seluruh skrip kustomisasi, paket bahasa Indonesia, unit "
            "systemd, aset SVG, panduan non-dotfolder, dan label 0.5 (os-release, labkita-release, "
            "install-sources.yaml, layar sambutan) diseragamkan memakai line ending LF via .gitattributes dan "
            "tools/build_v05.py (mengatasi kegagalan shebang CRLF yang sempat ditemukan di build #2).",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "2.",
            "Build Reproducible di WSL (tools/build_v05.py, Tag v0.5-iso): Memakai resep Bisect #3 (non-Cubic) "
            "ditambah grup sistem labkita-praktikum dan .disk/info bertanda kutip \"Noble Numbat\" "
            "(Ubuntu 24.04 LabKita 0.5 \"Noble Numbat\" - Release amd64 (20261122)), lalu meregenerasi "
            "md5sum.txt pasca seluruh squashfs final selesai (1016/1016 OK pada loop mount ISO).",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "3.",
            "Mastering & Verifikasi ISO 0.5: Xorriso memproduksi labkita-linux-0.5-amd64.iso berukuran "
            "6.643.179.520 bytes (~6,19 GiB / 6,64 GB) dengan SHA256 terverifikasi (Linux sha256sum & Windows "
            "Get-FileHash identik) d0dae277d140decd3e1ecaff9b908c551109a10efd069b1472acd34b046f5f1c dan MD5 "
            "b73178250b61cdfd900e3a3f8bdca660.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "4.",
            "Pengujian Mesin Virtual (VM Test Identik): VM uji bersih build/test-vm/labkita-test.vmx (3D "
            "mati, disk kosong 40 GB baru) diuji penuh pada rilis 0.5 mulai dari live session, installer GUI "
            "hingga selesai restart, pemeriksaan pascainstalasi, serta 5x cold boot benchmark setara terhadap "
            "arsip 0.1, 0.2, 0.3, dan 0.4.",
            styles["Numbered"],
        )
    )

    story.append(TOCMarker("bab4b"))
    story.append(Paragraph("B. Skenario dan Hasil Pengujian Fungsional", styles["SubHeading"]))
    story.append(
        p_body(
            "Pengujian fungsional, integritas media ISO, live autologin, instalasi GUI ke disk kosong, dan "
            "keamanan dijalankan nyata pada VM uji untuk rilis 0.5 (tanpa parameter GRUB tambahan). Hasil "
            "lulus maupun catatan cadangan dilaporkan apa adanya:"
        )
    )
    test_rows = [
        [
            Paragraph("No", styles["TblHdr"]),
            Paragraph("Skenario Uji", styles["TblHdr"]),
            Paragraph("Hasil yang Diharapkan", styles["TblHdr"]),
            Paragraph("Hasil Aktual di VM 0.5", styles["TblHdr"]),
            Paragraph("Status", styles["TblHdr"]),
        ],
        [
            Paragraph("1", styles["TblCellCenter"]),
            Paragraph("Integritas md5sum.txt & Casper", styles["TblCellLeft"]),
            Paragraph("Seluruh berkas manifest valid", styles["TblCellLeft"]),
            Paragraph(
                "Loop ISO: 1016/1016 OK (exit 0; kecuali boot.catalog & eltorito.img); casper-md5check pass",
                styles["TblCellLeft"],
            ),
            Paragraph("LULUS", styles["TblCellCenter"]),
        ],
        [
            Paragraph("2", styles["TblCellCenter"]),
            Paragraph("GRUB & Live Autologin", styles["TblCellLeft"]),
            Paragraph("Boot ID 0.5 langsung desktop tanpa GIS", styles["TblCellLeft"]),
            Paragraph(
                "whoami = ubuntu (uid=1000); casper.log bersih; telemetry Media = Ubuntu 24.04 LabKita 0.5",
                styles["TblCellLeft"],
            ),
            Paragraph("LULUS", styles["TblCellCenter"]),
        ],
        [
            Paragraph("3", styles["TblCellCenter"]),
            Paragraph("Installer GUI Bootstrap (Resmi 0.5)", styles["TblCellLeft"]),
            Paragraph("Wizard grafis selesai instalasi ke /dev/sda", styles["TblCellLeft"]),
            Paragraph(
                "Melewati bahasa ID, disk 40 GB, labadmin, Asia/Jakarta hingga 'Instalasi selesai'",
                styles["TblCellLeft"],
            ),
            Paragraph("LULUS (Resmi)", styles["TblCellCenter"]),
        ],
        [
            Paragraph("4", styles["TblCellCenter"]),
            Paragraph("Installer TUI (Cadangan)", styles["TblCellLeft"]),
            Paragraph("Jalur cadangan & arsip 0.1\u20130.4 Cubic", styles["TblCellLeft"]),
            Paragraph(
                "subiquity.cmd.tui tetap tersedia sebagai prosedur cadangan (utama pada arsip 0.1\u20130.4)",
                styles["TblCellLeft"],
            ),
            Paragraph("CADANGAN", styles["TblCellCenter"]),
        ],
        [
            Paragraph("5", styles["TblCellCenter"]),
            Paragraph("Konsistensi Metadata 0.5", styles["TblCellLeft"]),
            Paragraph("Tidak ada sisa label 0.1\u20130.4", styles["TblCellLeft"]),
            Paragraph(
                "/etc/os-release, /etc/labkita-release, sambutan, & panduan HTML tampil 0.5",
                styles["TblCellLeft"],
            ),
            Paragraph("LULUS", styles["TblCellCenter"]),
        ],
        [
            Paragraph("6", styles["TblCellCenter"]),
            Paragraph("Desktop WhiteSur & ID", styles["TblCellLeft"]),
            Paragraph("WhiteSur, dock tengah, UI Indonesia", styles["TblCellLeft"]),
            Paragraph(
                "Tema WhiteSur, tombol kiri, dock bawah, wallpaper LabKita, & UI Bahasa Indonesia",
                styles["TblCellLeft"],
            ),
            Paragraph("LULUS", styles["TblCellCenter"]),
        ],
        [
            Paragraph("7", styles["TblCellCenter"]),
            Paragraph("Suite labkita-check (Snap)", styles["TblCellLeft"]),
            Paragraph("Menguji seluruh komponen & Firefox Snap", styles["TblCellLeft"]),
            Paragraph(
                "SEMUA PEMERIKSAAN LULUS termasuk ~/Dokumen/Panduan-LabKita & snap run firefox (AppArmor OK)",
                styles["TblCellLeft"],
            ),
            Paragraph("LULUS", styles["TblCellCenter"]),
        ],
        [
            Paragraph("8", styles["TblCellCenter"]),
            Paragraph("Peluncur labkita-guide", styles["TblCellLeft"]),
            Paragraph("Panduan terbuka di Firefox Snap", styles["TblCellLeft"]),
            Paragraph(
                "Firefox Snap merender ~/Dokumen/Panduan-LabKita/index.html (badge LabKita Linux 0.5)",
                styles["TblCellLeft"],
            ),
            Paragraph("LULUS", styles["TblCellCenter"]),
        ],
        [
            Paragraph("9", styles["TblCellCenter"]),
            Paragraph("Postinstall & Grup Praktikum", styles["TblCellLeft"]),
            Paragraph("Akun praktikan 0 error, grup labkita-praktikum", styles["TblCellLeft"]),
            Paragraph(
                "sudo labkita-postinstall praktikan [SUKSES] 0 error; uid=1001, grup labkita-praktikum",
                styles["TblCellLeft"],
            ),
            Paragraph("LULUS", styles["TblCellCenter"]),
        ],
        [
            Paragraph("10", styles["TblCellCenter"]),
            Paragraph("Isolasi 0700 & Non-Sudo", styles["TblCellLeft"]),
            Paragraph("Izin 0700 & akun tanpa sudo", styles["TblCellLeft"]),
            Paragraph(
                "stat -c '%a' /home/praktikan = 700; tanpa hak sudo; akses lintas user diblokir",
                styles["TblCellLeft"],
            ),
            Paragraph("LULUS", styles["TblCellCenter"]),
        ],
        [
            Paragraph("11", styles["TblCellCenter"]),
            Paragraph("Offline GCC/Python & Tmpfs", styles["TblCellLeft"]),
            Paragraph("Jalan offline; /run/labkita 1777", styles["TblCellLeft"]),
            Paragraph(
                "Eksekusi contoh C (~/Praktikum), Python 3 & fork/multiprocess, tmpfs /run/labkita 1777 sukses",
                styles["TblCellLeft"],
            ),
            Paragraph("LULUS", styles["TblCellCenter"]),
        ],
    ]
    story.append(make_grid_table(test_rows, [26.0, 74.0, 79.0, 148.0, 70.0], pad_lr=5.4, repeat_rows=1))
    story.append(Spacer(1, 4.0))
    story.append(
        p_body(
            "*Catatan: Pada rilis 0.5 build WSL, seluruh skenario fungsional termasuk installer GUI normal "
            "(Skenario 3) lulus penuh tanpa fallback, sedangkan kegagalan GUI pada arsip 0.1\u20130.4 build "
            "Cubic tetap dicatat jujur sebagai keterbatasan build arsip sebelumnya."
        )
    )

    intro_img_p = Paragraph(
        "Bukti Tangkapan Layar Pengujian Nyata 0.5 &amp; Arsip 0.4 (Capture VM Asli):",
        styles["Body"],
    )
    fig1 = evidence_figure(
        "0.5-07-gui-install-complete.png",
        "Gambar 4.1: Installer GUI ubuntu-desktop-bootstrap LabKita Linux 0.5 Selesai Penuh Hingga "
        "\u2018Instalasi selesai\u2019",
        styles,
    )
    story.append(KeepTogether([intro_img_p, *fig1._content]))
    story.append(
        evidence_figure(
            "0.5-12-os-release-and-labkita-check.png",
            "Gambar 4.2: Hasil labkita-check 0.5 Terinstal: SEMUA PEMERIKSAAN LULUS (Termasuk Firefox Snap "
            "AppArmor OK)",
            styles,
        )
    )
    story.append(
        evidence_figure(
            "0.5-14-labkita-guide-firefox.png",
            "Gambar 4.3: Panduan Offline LabKita Linux 0.5 Terbuka Normal di Firefox Snap "
            "(~/Dokumen/Panduan-LabKita)",
            styles,
        )
    )
    story.append(
        evidence_figure(
            "0.4-02-gui-installer-error.png",
            "Gambar 4.4: Arsip Bukti Kegagalan Installer GUI pada Rilis 0.1\u20130.4 Build Cubic (\u2018Ada yang salah\u2019)",
            styles,
        )
    )

    # =========================================================================
    # BAB IV.C BENCHMARK 5x (0.1 vs 0.2 vs 0.3 vs 0.4 vs 0.5)
    # =========================================================================
    story.append(TOCMarker("bab4c"))
    story.append(
        Paragraph(
            "C. Pengukuran Kinerja dan Tolok Ukur Empiris (0.1 vs 0.2 vs 0.3 vs 0.4 vs 0.5, 5x per Versi)",
            styles["SubHeading"],
        )
    )
    story.append(
        p_body(
            "Pengukuran dilakukan ulang pada VM yang sama (RAM 4.096 MB / 3.911 MiB terdeteksi, 2 vCPU, disk "
            "kosong 40 GB SCSI yang diinstal ulang bersih untuk setiap versi), sebanyak 5 kali cold boot bersih "
            "per versi (settle 20 detik setelah desktop siap). Variabel pembeda kernel: 0.1 dan 0.2 bersih "
            "memakai kernel Linux 7.0.0-31-generic, sedangkan 0.3, 0.4, dan 0.5 memakai 7.0.0-43-generic."
        )
    )
    bench_rows = [
        [
            Paragraph("Parameter Uji", styles["BenchHdr"]),
            Paragraph("LabKita 0.1 (5x)<br/>[7.0.0-31]", styles["BenchHdr"]),
            Paragraph("LabKita 0.2 (5x)<br/>[7.0.0-31]", styles["BenchHdr"]),
            Paragraph("LabKita 0.3 (5x)<br/>[7.0.0-43]", styles["BenchHdr"]),
            Paragraph("LabKita 0.4 (5x)<br/>[7.0.0-43]", styles["BenchHdr"]),
            Paragraph("LabKita 0.5 (5x)<br/>[7.0.0-43]", styles["BenchHdr"]),
        ],
        [
            Paragraph("Memori Used<br/>(free -m, MiB)", styles["BenchCellCenter"]),
            Paragraph(
                "1052 / 1018 /<br/>1056 / 1049 /<br/>1016 MiB<br/>Avg: 1.038,2<br/>(1.016\u20131.056)<br/>Avail: 2.872,6",
                styles["BenchCellLeft"],
            ),
            Paragraph(
                "1072 / 1080 /<br/>1072 / 1059 /<br/>1058 MiB<br/>Avg: 1.068,2<br/>(1.058\u20131.080)<br/>Avail: 2.842,2",
                styles["BenchCellLeft"],
            ),
            Paragraph(
                "1049 / 1067 /<br/>1067 / 1062 /<br/>1046 MiB<br/>Avg: 1.058,2<br/>(1.046\u20131.067)<br/>Avail: 2.852,0",
                styles["BenchCellLeft"],
            ),
            Paragraph(
                "1043 / 1051 /<br/>1075 / 1071 /<br/>1073 MiB<br/>Avg: 1.062,6<br/>(1.043\u20131.075)<br/>Avail: 2.847,8",
                styles["BenchCellLeft"],
            ),
            Paragraph(
                "1041 / 1039 /<br/>1049 / 1054 /<br/>1031 MiB<br/>Avg: 1.042,8<br/>(1.031\u20131.054)<br/>Avail: 2.867,6",
                styles["BenchCellLeft"],
            ),
        ],
        [
            Paragraph("Waktu Boot Total<br/>(systemd-analyze)", styles["BenchCellCenter"]),
            Paragraph(
                "8,359 / 8,403 /<br/>8,676 / 8,434 /<br/>8,426 s<br/>Avg: 8,460s<br/>(8,359\u20138,676s)<br/>K 3,205+U 5,255",
                styles["BenchCellLeft"],
            ),
            Paragraph(
                "9,437 / 9,401 /<br/>9,458 / 9,218 /<br/>9,072 s<br/>Avg: 9,317s<br/>(9,072\u20139,458s)<br/>K 3,330+U 5,987",
                styles["BenchCellLeft"],
            ),
            Paragraph(
                "8,840 / 8,938 /<br/>8,788 / 8,460 /<br/>9,014 s<br/>Avg: 8,808s<br/>(8,460\u20139,014s)<br/>K 3,197+U 5,610",
                styles["BenchCellLeft"],
            ),
            Paragraph(
                "10,713 / 8,520 /<br/>8,726 / 8,967 /<br/>9,000 s<br/>Avg: 9,185s<br/>(8,520\u201310,713s)<br/>K 3,363+U 5,822",
                styles["BenchCellLeft"],
            ),
            Paragraph(
                "9,515 / 9,444 /<br/>9,370 / 8,349 /<br/>8,502 s<br/>Avg: 9,036s<br/>(8,349\u20139,515s)<br/>K 3,287+U 5,749",
                styles["BenchCellLeft"],
            ),
        ],
        [
            Paragraph("graphical.target<br/>(userspace)", styles["BenchCellCenter"]),
            Paragraph("Avg: 5,180s<br/>(5,084\u20135,371s)", styles["BenchCellLeft"]),
            Paragraph("Avg: 5,918s<br/>(5,786\u20136,057s)", styles["BenchCellLeft"]),
            Paragraph("Avg: 5,532s<br/>(5,215\u20135,717s)", styles["BenchCellLeft"]),
            Paragraph("Avg: 5,779s<br/>(5,202\u20136,823s)", styles["BenchCellLeft"]),
            Paragraph("Avg: 5,686s<br/>(5,132\u20136,100s)", styles["BenchCellLeft"]),
        ],
        [
            Paragraph("Layanan Terlama", styles["BenchCellCenter"]),
            Paragraph("plymouth-quit:<br/>2,18\u20132,50s<br/>snapd: ~1,02s", styles["BenchCellLeft"]),
            Paragraph("plymouth-quit:<br/>2,61\u20132,85s<br/>snapd: ~1,12s", styles["BenchCellLeft"]),
            Paragraph("plymouth-quit:<br/>2,21\u20132,70s<br/>snapd: ~1,05s", styles["BenchCellLeft"]),
            Paragraph("plymouth-quit:<br/>2,21\u20133,04s<br/>snapd: 1,06\u20131,16s", styles["BenchCellLeft"]),
            Paragraph("plymouth-quit:<br/>2,10\u20132,87s<br/>snapd: 1,06\u20131,24s", styles["BenchCellLeft"]),
        ],
    ]
    story.append(make_grid_table(bench_rows, [72.0, 65.0, 65.0, 65.0, 65.0, 65.0], pad_lr=2.5, repeat_rows=1))
    story.append(Spacer(1, 5.0))
    story.append(
        p_body(
            "Kesimpulan Empiris Benchmark (Tanpa Klaim Lebih Ringan/Cepat): Rentang konsumsi RAM 0.5 "
            "(1.031\u20131.054 MiB; rata-rata 1.042,8 MiB; avail rata-rata 2.867,6 MiB) bertumpang tindih "
            "dengan 0.1 (1.016\u20131.056 MiB), 0.2 (1.058\u20131.080 MiB), 0.3 (1.046\u20131.067 MiB), dan "
            "0.4 (1.043\u20131.075 MiB). Rentang waktu boot 0.5 (8,349\u20139,515s; rata-rata 9,036s) juga "
            "bertumpang tindih dengan seluruh versi sebelumnya, disertai perbedaan kernel (7.0.0-43-generic "
            "pada 0.3/0.4/0.5 vs 7.0.0-31-generic pada 0.1/0.2). Oleh karena itu, tidak ada perbedaan yang "
            "dapat dibuktikan antarversi."
        )
    )

    # =========================================================================
    # BAB IV.D PEMBAHASAN TEMUAN TEKNIS
    # =========================================================================
    story.append(TOCMarker("bab4d"))
    story.append(
        Paragraph(
            "D. Pembahasan Temuan Teknis: Fix Autologin, Installer GUI 0.5 & Verifikasi Build",
            styles["SubHeading"],
        )
    )
    story.append(
        p_body(
            "Rangkaian eksperimen kontrol (bisect #1\u2013#4), uji GRUB username=ubuntu pada 0.4, serta build "
            "dan pengujian rilis 0.5 di WSL menghasilkan temuan teknis terverifikasi berikut:"
        )
    )
    story.append(
        num_item(
            "1.",
            "Bukti Penyebab Kegagalan Autologin (Bisect #3 vs #4): Pada VMX uji identik (3D mati), "
            "Ubuntu 24.04.5 asli lulus sedangkan arsip 0.1\u20130.3 gagal autologin. Pada bisect manual di WSL: "
            "Bisect #3 (tanpa grup labkita) lulus, sementara Bisect #4 (identik #3 + .disk/info \"LabKita "
            "Linux 0.3\" + groupadd --system labkita) gagal autologin dengan casper.log: fatal: The group "
            "\u2018labkita\u2019 already exists. Penggantian nama grup menjadi labkita-praktikum sejak 0.4 "
            "terbukti memulihkan autologin secara tuntas.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "2.",
            "Kegagalan Installer GUI pada Arsip Cubic 0.4 & Uji Hipotesis username=ubuntu: Meskipun autologin "
            "pulih di 0.4, installer GUI pada ISO 0.4 build Cubic tetap gagal (\u2018Ada yang salah\u2019) "
            "bahkan saat parameter GRUB username=ubuntu hostname=ubuntu ditambahkan (whoami=ubuntu, "
            "casper.log bersih, tetapi berhenti di DEBUG desktop: Inhibiting Gnome session). Hal ini "
            "menggugurkan hipotesis bahwa perubahan USERNAME=labkita saja memicu error GUI pada build Cubic.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "3.",
            "Pemulihan Penuh Installer GUI pada Build WSL 0.5 (.disk/info Bertanda Kutip): Saat membangun 0.5 "
            "di WSL dengan tools/build_v05.py (resep Bisect #3 + grup labkita-praktikum + label 0.5), "
            "percobaan #1 yang memakai .disk/info tanpa tanda kutip ganda (\") masih gagal GUI dan strace "
            "memperlihatkan proses berhenti pasca openat(\"/cdrom/.disk/info\") tanpa menulis "
            "/var/log/installer/telemetry. Ketika satu variabel .disk/info diubah memakai tanda kutip codename "
            "(Ubuntu 24.04 LabKita 0.5 \"Noble Numbat\" - Release amd64 (20261122)) pada build final 0.5, "
            "telemetry tertulis normal dan installer GUI berjalan penuh hingga \u2018Instalasi selesai\u2019. "
            "Berdasarkan inspeksi sumber hulu canonical/ubuntu-desktop-provision "
            "(ProductService._extractIsoInfo), kondisi tersebut bersesuaian dengan hipotesis/inferensi bahwa "
            "pemanggilan isoName.substring(0, isoName.indexOf('\"') - 1) melempar RangeError ketika tanda "
            "kutip ganda tidak ditemukan; sementara itu, faktor lapisan Cubic 0.1\u20130.4 di luar .disk/info "
            "belum diisolasi ulang karena 0.5 memakai pipeline WSL.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "4.",
            "Kejujuran Penanganan CRLF pada Build #2 & Prosedur Resmi 0.5: Pengujian internal build #2 di WSL "
            "sempat menemukan kegagalan shebang (/usr/bin/env: 'python3\\r' dan 'bash\\r') pada "
            "labkita-check, labkita-postinstall, serta labkita-guide akibat checkout Git Windows berformat "
            "CRLF. Masalah ini diselesaikan lewat penambahan .gitattributes dan normalisasi LF di "
            "tools/build_v05.py sebelum build final 0.5 (SHA256 d0dae277...) dirilis. Dengan lulusnya "
            "installer GUI pada build WSL 0.5, prosedur instalasi resmi 0.5 ditetapkan memakai installer GUI "
            "(ubuntu-desktop-bootstrap), sedangkan jalur TUI (subiquity.cmd.tui) dijadikan cadangan.",
            styles["Numbered"],
        )
    )
    story.append(PageBreak())

    # =========================================================================
    # BAB V PENUTUP
    # =========================================================================
    story.append(TOCMarker("bab5"))
    story.append(Paragraph("BAB V<br/>PENUTUP", styles["ChapterHeading"]))

    story.append(TOCMarker("bab5a"))
    story.append(Paragraph("A. Kesimpulan", styles["SubHeading"]))
    story.append(
        p_body(
            "Berdasarkan hasil perancangan, implementasi, dan pengujian empiris pascainstalasi yang telah "
            "dilakukan hingga rilis final LabKita Linux 0.5, dapat disimpulkan bahwa:"
        )
    )
    story.append(
        num_item(
            "1.",
            "Keluaran Produk Final 0.5 Tercapai: Berkas citra bootable labkita-linux-0.5-amd64.iso "
            "(6.643.179.520 bytes / ~6,19 GiB, SHA256 d0dae277...046f5f1c) berhasil dibangun reproducible di "
            "WSL dari tag v0.5-iso, lolos verifikasi md5sum 1016/1016 OK, autologin live ubuntu berjalan "
            "bersih, dan installer GUI ubuntu-desktop-bootstrap selesai penuh hingga terinstal di disk kosong "
            "40 GB.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "2.",
            "Fitur Praktikum, Keamanan & Sandbox Snap Terbukti: Seluruh pemeriksaan labkita-check [LULUS] "
            "(termasuk uji baca ~/Dokumen/Panduan-LabKita melalui Firefox Snap AppArmor OK), panduan 0.5 "
            "terbuka normal, sudo labkita-postinstall praktikan membentuk akun non-sudo pada grup "
            "labkita-praktikum dengan isolasi direktori /home/praktikan mode 0700, serta tmpfs /run/labkita "
            "(1777) aktif lewat systemd.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "3.",
            "Kejujuran Penelusuran Bug Autologin & Installer GUI: Bentrok grup labkita terbukti menyebabkan "
            "kegagalan autologin (Bisect #3 vs #4) dan tuntas lewat labkita-praktikum; pada build WSL, "
            ".disk/info bertanda kutip \"Noble Numbat\" memulihkan installer GUI penuh pada rilis 0.5 "
            "(sehingga GUI menjadi prosedur resmi 0.5 dan TUI sebagai cadangan).",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "4.",
            "Integritas Tolok Ukur Empiris 5x Ukur: Pada pengujian VM identik, RAM rata-rata 0.5 tercatat "
            "1.042,8 MiB (1.031\u20131.054 MiB) dibanding 0.1 (1.038,2 MiB), 0.2 (1.068,2 MiB), 0.3 (1.058,2 MiB), "
            "dan 0.4 (1.062,6 MiB), sedangkan waktu boot 0.5 rata-rata 9,036s (8,349\u20139,515s) dibanding 0.1 "
            "(8,460s), 0.2 (9,317s), 0.3 (8,808s), dan 0.4 (9,185s). Karena tumpang tindih rentang serta "
            "perbedaan kernel (7.0.0-43 vs 7.0.0-31), tidak ada perbedaan yang dapat dibuktikan antarversi.",
            styles["Numbered"],
        )
    )

    story.append(TOCMarker("bab5b"))
    story.append(Paragraph("B. Keterbatasan dan Catatan Jujur Rilis 0.5", styles["SubHeading"]))
    story.append(
        p_body(
            "Meskipun rilis final LabKita Linux 0.5 telah lulus seluruh pengujian fungsional, kendala dan "
            "batasan investigasi berikut tetap dicatat apa adanya:"
        )
    )
    story.append(
        num_item(
            "1.",
            "Perbedaan Lapisan Build Cubic (0.1\u20130.4) Belum Diisolasi Ulang: Keberhasilan installer GUI di "
            "0.5 diperoleh lewat pipeline build WSL (tools/build_v05.py, resep Bisect #3) dan penambahan tanda "
            "kutip pada .disk/info. Penjelasan RangeError pada ProductService._extractIsoInfo() merupakan hasil "
            "analisis/inferensi dari pembacaan sumber upstream ubuntu-desktop-provision dan trace strace, "
            "sedangkan variabel lingkungan lain milik Cubic pada arsip 0.1\u20130.4 belum diuji ulang terpisah "
            "di Cubic.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "2.",
            "Catatan Perbaikan Build #2 (CRLF) & Flag Tmpfs Noexec: Build #2 WSL sempat gagal shebang "
            "python3\\r / bash\\r akibat checkout Windows CRLF sebelum diperbaiki lewat .gitattributes dan "
            "normalisasi LF pada build final 0.5 (d0dae277...). Selain itu, partisi sistem /run tetap berflag "
            "noexec sehingga biner kompilasi C praktikan dieksekusi dari ~/Praktikum sementara /run/labkita "
            "digunakan sebagai ruang scratch data sementara.",
            styles["Numbered"],
        )
    )

    story.append(TOCMarker("bab5c"))
    story.append(
        Paragraph("C. Saran Pengembangan Lanjutan", styles["SubHeading"])
    )
    story.append(
        p_body("Sebagai catatan pengembangan lanjutan di luar cakupan rilis final 0.5, perbaikan terfokus yang dapat dieksplorasi meliputi:")
    )
    story.append(
        num_item(
            "1.",
            "Isolasi Ulang Pipeline Cubic vs WSL: Menguji injeksi format .disk/info bertanda kutip serta "
            "membandingkan manifest/snap seed pada pipeline Cubic untuk mengonfirmasi konsistensi build di "
            "kedua metode.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "2.",
            "Penyelarasan Tema Dock WhiteSur: Memeriksa ulang cache dan asosiasi ikon dock (khususnya slot "
            "Terminal/aplikasi bawaan) agar seluruh ikon tampil tajam pada kondisi aktif maupun diam.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "3.",
            "Opsi Desktop Lebih Ringan: Mengevaluasi XFCE4 atau Openbox bila distro akan dipasang di komputer "
            "laboratorium dengan RAM terbatas.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "4.",
            "Mode Ujian Lab (Kiosk Profile): Menyediakan profil login khusus yang mengunci jaringan dan "
            "antarmuka saat sesi ujian praktikum.",
            styles["Numbered"],
        )
    )
    story.append(PageBreak())

    # =========================================================================
    # DAFTAR PUSTAKA (preserved format & references)
    # =========================================================================
    story.append(TOCMarker("dafpus"))
    story.append(Paragraph("DAFTAR PUSTAKA", styles["ChapterHeading"]))
    bib_entries = [
        "Canonical Ltd. (2024). Ubuntu 24.04 LTS (Noble Numbat) Release Notes &amp; Documentation. Diakses dari: https://ubuntu.com/download/desktop",
        "Love, Robert. (2013). Linux System Programming: Talking Directly to the Kernel and C Library (2nd ed.). O\u2019Reilly Media.",
        "Poettering, Lennart. (2023). systemd System and Service Manager Manual. freedesktop.org.",
        "Silberschatz, A., Galvin, P. B., &amp; Gagne, G. (2018). Operating System Concepts (10th ed.). John Wiley &amp; Sons.",
        "Singh, PJ. (2024). Cubic (Custom Ubuntu ISO Creator) Documentation &amp; Terminal Page. Diakses dari: https://github.com/PJ-Singh-001/Cubic",
        "Tanenbaum, A. S., &amp; Bos, H. (2015). Modern Operating Systems (4th ed.). Pearson.",
    ]
    for entry in bib_entries:
        story.append(Paragraph(entry, styles["BibItem"]))
    story.append(PageBreak())

    # =========================================================================
    # LAMPIRAN
    # =========================================================================
    story.append(TOCMarker("lamp"))
    story.append(Paragraph("LAMPIRAN", styles["ChapterHeading"]))

    story.append(TOCMarker("lamp1"))
    story.append(Paragraph("Lampiran 1: Tautan Repositori Kode Sumber dan Berkas ISO", styles["LampiranHeading"]))
    story.append(
        num_item(
            "1.",
            "Repositori GitHub Resmi: https://github.com/luvices/labkita (memuat skrip build tools/build_v05.py, "
            "skrip kustomisasi, payload, dokumen pengujian, generator laporan, dan bukti tangkapan layar; tag "
            "rilis: v0.5-iso).",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "2.",
            "Berkas Citra ISO Resmi: labkita-linux-0.5-amd64.iso (Ukuran: 6.643.179.520 bytes / ~6,19 GiB / 6,64 GB). "
            "Arsip 0.1\u20130.4 tetap tersimpan sebagai riwayat rilis.",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "3.",
            f"Tautan Unduhan ISO 0.5: {DRIVE_ISO_URL}",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "4.",
            "Verifikasi SHA256: d0dae277d140decd3e1ecaff9b908c551109a10efd069b1472acd34b046f5f1c",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "5.",
            "Verifikasi MD5: b73178250b61cdfd900e3a3f8bdca660",
            styles["Numbered"],
        )
    )
    story.append(
        num_item(
            "6.",
            "Metode Build: Skrip WSL tools/build_v05.py (resep Bisect #3, tag v0.5-iso); arsip 0.1\u20130.4 "
            "memakai Cubic 2026.09.110-release~202609120048~ubuntu24.04.1.",
            styles["Numbered"],
        )
    )

    story.append(TOCMarker("lamp2"))
    story.append(Paragraph("Lampiran 2: Naskah dan Tautan Video Demonstrasi", styles["LampiranHeading"]))
    story.append(
        p_body(
            "Video demonstrasi disiapkan dengan struktur alur kerja nyata pada VM uji: (1) Pembukaan, booting "
            "GRUB 0.5 Bahasa Indonesia, autologin live ubuntu bersih, dan jalannya installer GUI normal "
            "ubuntu-desktop-bootstrap hingga \u2018Instalasi selesai\u2019 (beserta catatan jujur perbedaan arsip "
            "0.1\u20130.4 Cubic + jalur cadangan subiquity TUI), (2) Desktop 0.5 terinstal (sambutan 0.5, tema "
            "WhiteSur, dock bawah, os-release), (3) Eksekusi labkita-check seluruh pemeriksaan LULUS (termasuk "
            "uji baca sandbox Firefox Snap AppArmor OK) dan pembukaan panduan 0.5 di Firefox Snap, (4) Pembuktian "
            "offline total tanpa jaringan (GCC di ~/Praktikum & multiprocessing Python), (5) Eksekusi "
            "labkita-postinstall (grup labkita-praktikum), isolasi folder 0700 dan akun praktikan non-sudo, serta "
            "(6) Perbandingan empiris 5x pengukuran RAM free -m dan boot time systemd-analyze (0.1 vs 0.2 vs 0.3 "
            "vs 0.4 vs 0.5 terinstal beserta variabel kernel)."
        )
    )
    story.append(p_body("Tautan Video Demo (YouTube Unlisted / Google Drive): [LINK-VIDEO-DEMO]"))

    story.append(TOCMarker("lamp3"))
    story.append(Paragraph("Lampiran 3: Pernyataan Kejujuran Akademik dan Penggunaan AI", styles["LampiranHeading"]))
    story.append(
        p_body(
            "Sesuai Ketentuan Akademik Poin 8.2 dokumen pedoman Final Project Sistem Operasi Ganjil 2026/2027: "
            "\u2018Alat bantu AI generatif boleh digunakan sebagai pendukung, dengan mencantumkan bagian yang "
            "dibantu AI di laporan. Setiap anggota tetap harus memahami dan mampu menjelaskan seluruh bagian "
            "produk.\u2019"
        )
    )
    story.append(
        p_body(
            "Dengan ini kami menyatakan secara transparan kontribusi alat bantu kecerdasan buatan (AI coding "
            "assistant) dalam proyek ini meliputi: (a) Membantu otomatisasi eksekusi dan capture layar VMware "
            "Workstation via protokol VNC (tanpa menyimpan kata sandi di kode), (b) Membantu penulisan dan "
            "penyempurnaan skrip build serta kustomisasi (tools/build_v05.py, normalisasi LF, dan penyesuaian "
            "skrip payload), (c) Membantu analisis log sistem (casper.log, ubuntu_bootstrap.log, serta trace "
            "strace) dan debugging kegagalan installer maupun shebang, (d) Membantu penyusunan skrip pengujian "
            "dan penghitungan rata-rata tolok ukur benchmark, serta (e) Membantu penyusunan draf dan "
            "pemformatan ulang dokumen laporan PDF dan slide presentasi berdasarkan data pengukuran riil."
        )
    )
    story.append(
        p_body(
            "Seluruh perancangan konsep sistem operasi (manajemen memori, hak akses Linux DAC, pemisahan hak "
            "istimewa, pembuatan layanan systemd, struktur remastering ISO, dan analisis tolok ukur empiris) "
            "dipelajari, diuji langsung, dipahami secara mendalam, dan dapat dipertanggungjawabkan sepenuhnya "
            "oleh setiap anggota tim pada sesi presentasi dan tanya jawab UAS."
        )
    )

    return story


def generate():
    styles = build_styles()
    toc_pages = {}

    # Pass 1: discover real page numbers for every TOCMarker
    doc1 = ReportDocTemplate(str(OUTPUT_PDF), toc_pages, pagesize=PAGE_SIZE)
    doc1.build(build_story(styles, toc_pages))

    # Pass 2: rebuild with synchronized page numbers in DAFTAR ISI
    toc_final = dict(toc_pages)
    doc2 = ReportDocTemplate(str(OUTPUT_PDF), toc_final, pagesize=PAGE_SIZE)
    doc2.build(build_story(styles, toc_pages))
    print(f"Generated {OUTPUT_PDF} ({doc2.page} pages) using fonts: {FONT_REGULAR} / {FONT_BOLD}")


if __name__ == "__main__":
    generate()
