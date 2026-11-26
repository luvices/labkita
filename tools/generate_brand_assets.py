#!/usr/bin/env python3
"""Generate crisp 4x-supersampled LabKita Linux Keystone LK brand PNG assets for Plymouth, GDM, and docs."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[1]
SPINNER_DIR = REPO_ROOT / "payload" / "usr" / "share" / "plymouth" / "themes" / "spinner"
PIXMAPS_DIR = REPO_ROOT / "payload" / "usr" / "share" / "pixmaps"
BRAND_DIR = REPO_ROOT / "assets" / "brand"


def load_font(size: int, bold: bool = True):
    candidates = (
        [
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ]
        if bold
        else [
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arial.ttf",
        ]
    )
    for path in candidates:
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def draw_mark(draw: ImageDraw.ImageDraw, x0: float, y0: float, size: float, dark_bg: bool = True):
    """Draw the architectural Keystone LK two-polygon mark matching assets/brand/labkita-mark*.svg."""
    scale = size / 256.0
    l_color = (241, 245, 249, 255) if dark_bg else (15, 23, 42, 255)    # #F1F5F9 / #0F172A
    k_color = (56, 189, 248, 255) if dark_bg else (29, 78, 216, 255)    # #38BDF8 / #1D4ED8

    def pt(px, py):
        return (x0 + px * scale, y0 + py * scale)

    # L polygon
    l_pts = [pt(32, 32), pt(72, 32), pt(72, 184), pt(184, 184), pt(224, 224), pt(32, 224)]
    draw.polygon(l_pts, fill=l_color)

    # K polygon
    k_pts = [
        pt(96, 32), pt(132, 32), pt(132, 72), pt(172, 32), pt(224, 32),
        pt(160, 96), pt(224, 160), pt(172, 160), pt(132, 120), pt(132, 160), pt(96, 160),
    ]
    draw.polygon(k_pts, fill=k_color)


def render_wordmark(width: int, height: int, dark_bg: bool, out_path: Path):
    """Render transparent wordmark PNG at 4x supersampling."""
    scale = 4
    W, H = width * scale, height * scale
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    mark_size = int(H * 0.72)
    mark_x = int(W * 0.02)
    mark_y = (H - mark_size) // 2
    draw_mark(draw, mark_x, mark_y, mark_size, dark_bg=dark_bg)

    text_x = mark_x + mark_size + int(W * 0.035)
    title_font = load_font(int(H * 0.28), bold=True)
    sub_font = load_font(int(H * 0.145), bold=False)

    title_primary = (241, 245, 249, 255) if dark_bg else (15, 23, 42, 255)
    title_accent = (56, 189, 248, 255) if dark_bg else (29, 78, 216, 255)
    sub_color = (148, 163, 184, 255) if dark_bg else (71, 85, 105, 255)

    y_title = int(H * 0.22)
    draw.text((text_x, y_title), "LabKita", font=title_font, fill=title_primary)
    bbox = draw.textbbox((text_x, y_title), "LabKita ", font=title_font)
    draw.text((bbox[2], y_title), "Linux", font=title_font, fill=title_accent)
    draw.text((text_x + int(scale * 0.5), int(H * 0.59)), "Praktikum Mandiri Offline", font=sub_font, fill=sub_color)

    final = img.resize((width, height), Image.Resampling.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    final.save(out_path, "PNG")
    print(f"Saved {out_path} ({width}x{height})")


def render_fallback(out_path: Path):
    """Render 128x128 transparent Plymouth bgrt-fallback PNG at 4x supersampling."""
    size = 128
    scale = 4
    S = size * scale
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    mark_size = int(S * 0.62)
    draw_mark(draw, (S - mark_size) // 2, int(S * 0.06), mark_size, dark_bg=True)

    font = load_font(int(S * 0.155), bold=True)
    text = "LabKita"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((S - tw) / 2 - bbox[0], int(S * 0.72)), text, font=font, fill=(241, 245, 249, 255))

    final = img.resize((size, size), Image.Resampling.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    final.save(out_path, "PNG")
    print(f"Saved {out_path} ({size}x{size})")


def render_mark_png(size: int, out_path: Path):
    scale = 4
    S = size * scale
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_mark(draw, 0, 0, S, dark_bg=False)
    final = img.resize((size, size), Image.Resampling.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    final.save(out_path, "PNG")
    print(f"Saved {out_path} ({size}x{size})")


def main():
    render_wordmark(248, 87, dark_bg=True, out_path=SPINNER_DIR / "watermark.png")
    render_fallback(SPINNER_DIR / "bgrt-fallback.png")
    render_wordmark(256, 89, dark_bg=True, out_path=PIXMAPS_DIR / "labkita-gdm-logo.png")
    render_mark_png(256, BRAND_DIR / "labkita-mark.png")
    render_wordmark(512, 178, dark_bg=True, out_path=BRAND_DIR / "labkita-wordmark-dark.png")
    render_wordmark(512, 178, dark_bg=False, out_path=BRAND_DIR / "labkita-wordmark-light.png")


if __name__ == "__main__":
    main()
