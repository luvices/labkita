"""Generator wallpaper minimalis gradien orisinal untuk LabKita Linux 0.2."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
bg_dir = root / "payload" / "usr" / "share" / "backgrounds"
bg_dir.mkdir(parents=True, exist_ok=True)

# 1. Generate High Quality SVG Wallpaper
svg_path = bg_dir / "labkita-gradient.svg"
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3840 2160" width="3840" height="2160">
  <defs>
    <!-- Background Base Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="35%" stop-color="#1e1b4b" />
      <stop offset="70%" stop-color="#0e3a6c" />
      <stop offset="100%" stop-color="#064e3b" />
    </linearGradient>

    <!-- Vibrant Mesh Glow 1 (Cyan / Ocean) -->
    <radialGradient id="glowOcean" cx="25%" cy="30%" r="55%">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.85" />
      <stop offset="45%" stop-color="#0369a1" stop-opacity="0.45" />
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0" />
    </radialGradient>

    <!-- Vibrant Mesh Glow 2 (Indigo / Violet) -->
    <radialGradient id="glowViolet" cx="80%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.75" />
      <stop offset="50%" stop-color="#6d28d9" stop-opacity="0.35" />
      <stop offset="100%" stop-color="#4c1d95" stop-opacity="0" />
    </radialGradient>

    <!-- Vibrant Mesh Glow 3 (Emerald / Teal) -->
    <radialGradient id="glowTeal" cx="60%" cy="85%" r="50%">
      <stop offset="0%" stop-color="#0d9488" stop-opacity="0.7" />
      <stop offset="60%" stop-color="#0f766e" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#134e4a" stop-opacity="0" />
    </radialGradient>

    <!-- Flowing Wave Gradient -->
    <linearGradient id="wave1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.4" />
      <stop offset="50%" stop-color="#818cf8" stop-opacity="0.2" />
      <stop offset="100%" stop-color="#c084fc" stop-opacity="0.05" />
    </linearGradient>

    <linearGradient id="wave2" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#2dd4bf" stop-opacity="0.35" />
      <stop offset="50%" stop-color="#3b82f6" stop-opacity="0.2" />
      <stop offset="100%" stop-color="#6366f1" stop-opacity="0.05" />
    </linearGradient>

    <!-- Subtle Center Frosted Disc -->
    <radialGradient id="centerGlow" cx="50%" cy="50%" r="40%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.06" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- Base Rectangle -->
  <rect width="3840" height="2160" fill="url(#bgGrad)" />

  <!-- Ambient Light Orbs -->
  <rect width="3840" height="2160" fill="url(#glowOcean)" />
  <rect width="3840" height="2160" fill="url(#glowViolet)" />
  <rect width="3840" height="2160" fill="url(#glowTeal)" />

  <!-- Minimalist Organic Waves -->
  <path d="M 0,1100 Q 960,650 1920,1050 T 3840,900 L 3840,2160 L 0,2160 Z" fill="url(#wave1)" />
  <path d="M 0,1450 Q 1200,980 2400,1500 T 3840,1350 L 3840,2160 L 0,2160 Z" fill="url(#wave2)" />

  <!-- Center Ambient -->
  <circle cx="1920" cy="1080" r="1200" fill="url(#centerGlow)" />

  <!-- Minimalist LabKita Emblem in Center -->
  <g transform="translate(1920, 1020)" text-anchor="middle">
    <!-- Geometric Flask & Compass Node -->
    <circle cx="0" cy="-60" r="52" fill="none" stroke="#ffffff" stroke-width="3.5" opacity="0.85" />
    <path d="M -24,-60 L 24,-60 M 0,-84 L 0,-36" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" opacity="0.9" />
    
    <!-- Outer accent orbital arc -->
    <path d="M -80,-60 A 80 80 0 0 1 80 -60" fill="none" stroke="#818cf8" stroke-width="2" stroke-dasharray="6 8" opacity="0.6" />

    <!-- Typography -->
    <text x="0" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', 'Helvetica Neue', sans-serif" font-size="52" font-weight="600" fill="#ffffff" letter-spacing="4" opacity="0.95">LabKita Linux</text>
    <text x="0" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', 'Helvetica Neue', sans-serif" font-size="22" font-weight="400" fill="#94a3b8" letter-spacing="8" opacity="0.85">SISTEM OPERASI PRAKTIKUM MANDIRI</text>
  </g>

  <!-- Bottom subtle build badge -->
  <g transform="translate(1920, 2080)" text-anchor="middle">
    <text font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="16" fill="#64748b" letter-spacing="2" opacity="0.65">LABKITA LINUX 0.2 &bull; NOBLE NUMBAT BASED &bull; OFFLINE EDITION</text>
  </g>
</svg>
"""

svg_path.write_text(svg_content.strip(), encoding="utf-8")
(bg_dir / "labkita.svg").write_text(svg_content.strip(), encoding="utf-8")
print(f"SVG wallpaper written: {svg_path}")

# 2. Generate High Resolution PNG Wallpaper (1920x1080 or 3840x2160)
# We can render using PIL gradient mesh
width, height = 3840, 2160
img = Image.new("RGBA", (width, height))
draw = ImageDraw.Draw(img)

# Diagonal base gradient
for y in range(height):
    ratio_y = y / height
    r1, g1, b1 = (15, 23, 42)    # Dark slate
    r2, g2, b2 = (14, 58, 108)   # Deep navy blue
    r3, g3, b3 = (6, 78, 59)     # Deep emerald
    
    if ratio_y < 0.6:
        t = ratio_y / 0.6
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
    else:
        t = (ratio_y - 0.6) / 0.4
        r = int(r2 + (r3 - r2) * t)
        g = int(g2 + (g3 - g2) * t)
        b = int(b2 + (b3 - b2) * t)
    draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

# Radial Glow Layer 1: Ocean Cyan at (960, 648)
glow1 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
g1_draw = ImageDraw.Draw(glow1)
cx1, cy1, r1_rad = 960, 648, 1300
for rad in range(r1_rad, 0, -15):
    alpha = int(90 * (1 - (rad / r1_rad) ** 1.3))
    g1_draw.ellipse([cx1 - rad, cy1 - rad, cx1 + rad, cy1 + rad], fill=(2, 132, 199, alpha))

# Radial Glow Layer 2: Indigo Violet at (3072, 864)
glow2 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
g2_draw = ImageDraw.Draw(glow2)
cx2, cy2, r2_rad = 3072, 864, 1500
for rad in range(r2_rad, 0, -20):
    alpha = int(75 * (1 - (rad / r2_rad) ** 1.2))
    g2_draw.ellipse([cx2 - rad, cy2 - rad, cx2 + rad, cy2 + rad], fill=(124, 58, 237, alpha))

# Radial Glow Layer 3: Teal at (2304, 1836)
glow3 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
g3_draw = ImageDraw.Draw(glow3)
cx3, cy3, r3_rad = 2304, 1836, 1200
for rad in range(r3_rad, 0, -15):
    alpha = int(60 * (1 - (rad / r3_rad) ** 1.3))
    g3_draw.ellipse([cx3 - rad, cy3 - rad, cx3 + rad, cy3 + rad], fill=(13, 148, 136, alpha))

# Composite Glow Layers
img = Image.alpha_composite(img, glow1)
img = Image.alpha_composite(img, glow2)
img = Image.alpha_composite(img, glow3)

# Wave Layer
wave_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
w_draw = ImageDraw.Draw(wave_layer)

points_wave1 = []
for x in range(0, width + 1, 20):
    y = int(1200 + 180 * math.sin(x * 0.0016) + 120 * math.cos(x * 0.0009))
    points_wave1.append((x, y))
points_wave1.extend([(width, height), (0, height)])
w_draw.polygon(points_wave1, fill=(56, 189, 248, 28))

points_wave2 = []
for x in range(0, width + 1, 20):
    y = int(1550 + 150 * math.cos(x * 0.0014) - 90 * math.sin(x * 0.0008))
    points_wave2.append((x, y))
points_wave2.extend([(width, height), (0, height)])
w_draw.polygon(points_wave2, fill=(45, 212, 191, 32))

img = Image.alpha_composite(img, wave_layer)

# Center Minimalist Emblem
draw = ImageDraw.Draw(img)
cx, cy = width // 2, height // 2 - 40
# Outer Circle
draw.ellipse([cx - 52, cy - 60 - 52, cx + 52, cy - 60 + 52], outline=(255, 255, 255, 220), width=4)
# Crosshair / Node
draw.line([(cx - 24, cy - 60), (cx + 24, cy - 60)], fill=(56, 189, 248, 230), width=3)
draw.line([(cx, cy - 60 - 24), (cx, cy - 60 + 24)], fill=(56, 189, 248, 230), width=3)

# Text (fallback to default font if custom font not found)
try:
    font_large = ImageFont.truetype("arial.ttf", 52)
    font_sub = ImageFont.truetype("arial.ttf", 22)
    font_bot = ImageFont.truetype("arial.ttf", 16)
except Exception:
    font_large = font_sub = font_bot = ImageFont.load_default()

draw.text((cx, cy + 45), "LabKita Linux", fill=(255, 255, 255, 240), font=font_large, anchor="mm")
draw.text((cx, cy + 90), "SISTEM OPERASI PRAKTIKUM MANDIRI", fill=(148, 163, 184, 220), font=font_sub, anchor="mm")
draw.text((cx, height - 70), "LABKITA LINUX 0.2 • NOBLE NUMBAT BASED • OFFLINE EDITION", fill=(100, 116, 139, 160), font=font_bot, anchor="mm")

png_path = bg_dir / "labkita-gradient.png"
img.save(png_path, "PNG", optimize=True)
print(f"PNG wallpaper written: {png_path} ({png_path.stat().st_size} bytes)")
