# Placeholder to ensure assets/ is treated as a Python package
# Actual PNGs are generated on first run if missing
import os
from pathlib import Path
from PIL import Image, ImageDraw

def ensure_assets():
    asset_dir = Path(__file__).parent
    logo_path = asset_dir / "logo.png"
    watermark_path = asset_dir / "watermark.png"

    if not logo_path.exists():
        # Generate minimal placeholder logo
        img = Image.new("RGBA", (256, 256), (70, 130, 180, 255))
        draw = ImageDraw.Draw(img)
        draw.text((80, 120), "CV", fill=(255, 255, 255, 255))
        img.save(logo_path)

    if not watermark_path.exists():
        # Transparent watermark
        img = Image.new("RGBA", (200, 50), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((5, 10), "Chromavine", fill=(255, 255, 255, 64))
        img.save(watermark_path)
