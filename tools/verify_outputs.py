from pypdf import PdfReader
from pptx import Presentation

r = PdfReader("docs/LAPORAN-PROYEK-LABKITA.pdf")
print("PDF PAGES:", len(r.pages))
for i, pg in enumerate(r.pages, 1):
    txt = pg.extract_text() or ""
    headings = [
        ln.strip() for ln in txt.splitlines()
        if any(ln.strip().startswith(prefix) for prefix in (
            "LABKITA LINUX", "DAFTAR ISI", "BAB ", "1.", "2.", "3.", "4.", "5.", "Daftar Pustaka", "Lampiran"
        ))
    ]
    print(f"Page {i} ({len(txt)} chars):", " | ".join(headings[:10]))

p = Presentation("docs/presentation/labkita-presentation.pptx")
print("\nPPTX SLIDES:", len(p.slides))
for idx, s in enumerate(p.slides, 1):
    pics = sum(1 for sh in s.shapes if sh.shape_type == 13)
    texts = [sh.text_frame.text.splitlines()[0] for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    print(f"Slide {idx}: pics={pics} | texts={texts[:4]}")
