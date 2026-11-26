#!/usr/bin/env python3
"""Generate crisp 4x-supersampled LabKita Linux brand PNG assets for Plymouth, GDM, and docs."""

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


def draw_mark(draw: ImageDraw.ImageDraw, x0: float, y0: float, size: float):
    """Draw the geometric cobalt-slate LabKita mark matching assets/brand/labkita-mark.svg."""
    s = size
    radius = s * (24.0 / 112.0)
    stroke = max(2, int(round(s * (4.0 / 112.0))))
    draw.rounded_rectangle(
        (x0, y0, x0 + s, y0 + s),
        radius=radius,
        fill=(30, 58, 95, 255),       # #1E3A5F
        outline=(56, 189, 248, 255),  # #38BDF8
        width=stroke,
    )
    # Prompt chevron ">"
    p1 = (x0 + s * 0.25, y0 + s * 0.305)
    p2 = (x0 + s * 0.50, y0 + s * 0.50)
    p3 = (x0 + s * 0.25, y0 + s * 0.695)
    cw = max(2, int(round(s * 0.105)))
    draw.line([p1, p2, p3], fill=(56, 189, 248, 255), width=cw, joint="curve")
    # Rounded endcaps on chevron tips
    r_cap = cw / 2.0
    for px, py in (p1, p2, p3):
        draw.ellipse((px - r_cap, py - r_cap, px + r_cap, py + r_cap), fill=(56, 189, 248, 255))

    # Underscore "_"
    draw.rounded_rectangle(
        (x0 + s * 0.515, y0 + s * 0.61, x0 + s * 0.77, y0 + s * 0.70),
        radius=max(1, int(round(s * 0.045))),
        fill=(248, 250, 252, 255),
    )
    # Top-right lab status node
    draw.rounded_rectangle(
        (x0 + s * 0.68, y0 + s * 0.23, x0 + s * 0.79, y0 + s * 0.34),
        radius=max(1, int(round(s * 0.025))),
        fill=(56, 189, 248, 255),
    )


def render_wordmark(width: int, height: int, dark_bg: bool, out_path: Path):
    """Render transparent wordmark PNG at 4x supersampling."""
    scale = 4
    W, H = width * scale, height * scale
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    mark_size = int(H * 0.62)
    mark_x = int(W * 0.03)
    mark_y = (H - mark_size) // 2
    draw_mark(draw, mark_x, mark_y, mark_size)

    text_x = mark_x + mark_size + int(W * 0.045)
    title_font = load_font(int(H * 0.28), bold=True)
    sub_font = load_font(int(H * 0.145), bold=False)

    title_primary = (248, 250, 252, 255) if dark_bg else (15, 23, 42, 255)
    title_accent = (56, 189, 248, 255) if dark_bg else (2, 132, 199, 255)
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

    mark_size = int(S * 0.56)
    draw_mark(draw, (S - mark_size) // 2, int(S * 0.08), mark_size)

    font = load_font(int(S * 0.16), bold=True)
    text = "LabKita"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((S - tw) / 2 - bbox[0], int(S * 0.72)), text, font=font, fill=(248, 250, 252, 255))

    final = img.resize((size, size), Image.Resampling.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    final.save(out_path, "PNG")
    print(f"Saved {out_path} ({size}x{size})")


def render_mark_png(size: int, out_path: Path):
    scale = 4
    S = size * scale
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = int(S * 0.06)
    draw_mark(draw, pad, pad, S - 2 * pad)
    final = img.resize((size, size), Image.Resampling.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    final.save(out_path, "PNG")
    print(f"Saved {out_path} ({size}x{size})")


def main():
    # Plymouth assets
    render_wordmark(248, 87, dark_bg=True, out_path=SPINNER_DIR / "watermark.png")
    render_fallback(SPINNER_DIR / "bgrt-fallback.png")
    # GDM login screen logo (matches Ubuntu's 256x89 ubuntu-logo-text-dark.png footprint)
    render_wordmark(256, 89, dark_bg=True, out_path=PIXMAPS_DIR / "labkita-gdm-logo.png")
    # Doc/README high-res exports if raster preview is needed
    render_mark_png(256, BRAND_DIR / "labkita-mark.png")
    render_wordmark(512, 178, dark_bg=True, out_path=BRAND_DIR / "labkita-wordmark-dark.png")
    render_wordmark(512, 178, dark_bg=False, out_path=BRAND_DIR / "labkita-wordmark-light.png")


if __name__ == "__main__":
    main()
