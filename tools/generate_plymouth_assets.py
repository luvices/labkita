#!/usr/bin/env python3
"""Generate transparent LabKita Linux boot splash (Plymouth) PNG assets."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[1]
SPINNER_DIR = REPO_ROOT / "payload" / "usr" / "share" / "plymouth" / "themes" / "spinner"


def load_font(size: int):
    candidates = [
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]
    for path in candidates:
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def draw_emblem(draw: ImageDraw.ImageDraw, cx: int, cy: int, radius: int):
    """Draw a minimal rounded hexagon/circle LabKita terminal emblem."""
    r = radius
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(14, 116, 144, 255), outline=(56, 189, 248, 255), width=max(2, r // 12))
    # Inner prompt glyph ">_"
    font = load_font(int(r * 0.95))
    text = ">_"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), text, font=font, fill=(255, 255, 255, 255))


def generate_watermark(out_path: Path):
    """Generate 248x87 transparent PNG matching Ubuntu's spinner watermark.png."""
    w, h = 248, 87
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw_emblem(draw, 32, h // 2, 20)

    font_main = load_font(23)
    font_sub = load_font(12)
    draw.text((62, 21), "LabKita", font=font_main, fill=(248, 250, 252, 255))
    draw.text((156, 21), "Linux", font=font_main, fill=(56, 189, 248, 255))
    draw.text((63, 52), "Praktikum Mandiri Offline", font=font_sub, fill=(148, 163, 184, 255))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG")
    print(f"Saved {out_path} ({w}x{h})")


def generate_bgrt_fallback(out_path: Path):
    """Generate 128x128 transparent PNG matching Ubuntu's bgrt-fallback.png."""
    size = 128
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw_emblem(draw, size // 2, 46, 36)
    font = load_font(20)
    text = "LabKita"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((size - tw) / 2 - bbox[0], 92), text, font=font, fill=(248, 250, 252, 255))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG")
    print(f"Saved {out_path} ({size}x{size})")


def main():
    generate_watermark(SPINNER_DIR / "watermark.png")
    generate_bgrt_fallback(SPINNER_DIR / "bgrt-fallback.png")


if __name__ == "__main__":
    main()
