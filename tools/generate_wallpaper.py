#!/usr/bin/env python3
"""Generate calm architectural Cobalt Slate desktop wallpaper (SVG 4K + PNG) matching Keystone LK brand."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[1]
BG_DIR = REPO_ROOT / "payload" / "usr" / "share" / "backgrounds"
BG_DIR.mkdir(parents=True, exist_ok=True)


def load_font(size: int, bold: bool = False):
    candidates = (
        [
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ]
        if bold
        else [
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
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


def build_svg():
    # 3840x2160 Cobalt Architectural Slate wallpaper (single neutral hue shift, no glowing blobs)
    grid_lines = []
    for gx in range(128, 3840, 128):
        grid_lines.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="2160"/>')
    for gy in range(128, 2160, 128):
        grid_lines.append(f'<line x1="0" y1="{gy}" x2="3840" y2="{gy}"/>')
    grid_markup = "\n    ".join(grid_lines)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3840 2160" width="3840" height="2160">
  <defs>
    <linearGradient id="slateTone" x1="0" y1="0" x2="0" y2="2160" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0C1220"/>
      <stop offset="100%" stop-color="#111A2E"/>
    </linearGradient>
  </defs>
  <rect width="3840" height="2160" fill="url(#slateTone)"/>
  <g stroke="#94A3B8" stroke-opacity="0.045" stroke-width="2">
    {grid_markup}
  </g>
  <line x1="2160" y1="0" x2="3840" y2="1680" stroke="#2563EB" stroke-opacity="0.28" stroke-width="4"/>
  <g transform="translate(1800, 816) scale(0.9375)">
    <path fill="#F1F5F9" d="M 32 32 H 72 V 184 H 184 L 224 224 H 32 Z"/>
    <path fill="#38BDF8" d="M 96 32 H 132 V 72 L 172 32 H 224 L 160 96 L 224 160 H 172 L 132 120 V 160 H 96 Z"/>
  </g>
  <text x="1920" y="1136" text-anchor="middle" font-family="Inter, Ubuntu, system-ui, sans-serif" font-size="68" font-weight="500" fill="#F1F5F9" letter-spacing="1">LabKita Linux</text>
  <text x="1920" y="1196" text-anchor="middle" font-family="Inter, Ubuntu, system-ui, sans-serif" font-size="30" font-weight="400" fill="#94A3B8" letter-spacing="2">Sistem Operasi Praktikum Offline</text>
</svg>
"""
    (BG_DIR / "labkita-gradient.svg").write_text(svg, encoding="utf-8")
    (BG_DIR / "labkita.svg").write_text(svg, encoding="utf-8")
    print(f"Saved SVG wallpapers in {BG_DIR}")


def build_png():
    W, H = 2560, 1440
    img = Image.new("RGBA", (W, H))
    draw = ImageDraw.Draw(img)

    # Single-hue tonal gradient (#0C1220 -> #111A2E)
    r1, g1, b1 = (12, 18, 32)
    r2, g2, b2 = (17, 26, 46)
    for y in range(H):
        t = y / (H - 1)
        draw.line([(0, y), (W, y)], fill=(int(r1 + (r2 - r1) * t), int(g1 + (g2 - g1) * t), int(b1 + (b2 - b1) * t), 255))

    # Composite subtle hairline grid + one quiet 45-degree cobalt structural line
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid)
    step = int(128 * (W / 3840.0))
    for gx in range(step, W, step):
        gdraw.line([(gx, 0), (gx, H)], fill=(148, 163, 184, 12), width=1)
    for gy in range(step, H, step):
        gdraw.line([(0, gy), (W, gy)], fill=(148, 163, 184, 12), width=1)
    gdraw.line([(int(2160 * (W / 3840.0)), 0), (W, int(1680 * (H / 2160.0)))], fill=(37, 99, 235, 72), width=3)
    img = Image.alpha_composite(img, grid)

    # Draw 4x supersampled Keystone LK centered emblem + crisp title
    mark_size = 176
    ss = Image.new("RGBA", (mark_size * 4, mark_size * 4), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(ss)
    k = (mark_size * 4) / 256.0
    sdraw.polygon([(32*k, 32*k), (72*k, 32*k), (72*k, 184*k), (184*k, 184*k), (224*k, 224*k), (32*k, 224*k)], fill=(241, 245, 249, 255))
    sdraw.polygon([
        (96*k, 32*k), (132*k, 32*k), (132*k, 72*k), (172*k, 32*k), (224*k, 32*k),
        (160*k, 96*k), (224*k, 160*k), (172*k, 160*k), (132*k, 120*k), (132*k, 160*k), (96*k, 160*k),
    ], fill=(56, 189, 248, 255))
    mark_img = ss.resize((mark_size, mark_size), Image.Resampling.LANCZOS)
    img.paste(mark_img, (W // 2 - mark_size // 2, int(H * 0.365)), mark_img)

    tdraw = ImageDraw.Draw(img)
    font_title = load_font(46, bold=True)
    font_sub = load_font(20, bold=False)
    tdraw.text((W // 2, int(H * 0.535)), "LabKita Linux", fill=(241, 245, 249, 245), font=font_title, anchor="mm")
    tdraw.text((W // 2, int(H * 0.578)), "Sistem Operasi Praktikum Offline", fill=(148, 163, 184, 215), font=font_sub, anchor="mm")

    out_png = BG_DIR / "labkita-gradient.png"
    img.convert("RGB").save(out_png, "PNG", optimize=True)
    print(f"Saved PNG wallpaper: {out_png} ({out_png.stat().st_size} bytes)")


def main():
    build_svg()
    build_png()


if __name__ == "__main__":
    main()
