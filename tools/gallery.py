"""Build 16:9 gallery thumbnails for the profile README from each project's own images."""
import sys
from pathlib import Path
from PIL import Image

GH = Path(r"C:\Users\Loggg\OneDrive\Documents\GitHub")
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
W, H = 800, 450


def fit(img, bg):
    """Letterbox img onto a W x H canvas of colour bg."""
    img = img.convert("RGB")
    img.thumbnail((W, H), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), bg)
    canvas.paste(img, ((W - img.width) // 2, (H - img.height) // 2))
    return canvas


def cover(img, box=None):
    """Crop img to box (if given), then scale to fill W x H, centre-cropping the excess."""
    img = img.convert("RGB")
    if box:
        img = img.crop(box)
    s = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    l, t = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((l, t, l + W, t + H))


jobs = {
    "satellite.jpg": lambda: cover(Image.open(GH / "Satellite Space Flight/docs/images/overview.png")),
    "belt.jpg": lambda: fit(Image.open(GH / "asteroid-belt-gradient/figures/fig8_proper_elements.png"), "white"),
    "mars.jpg": lambda: cover(Image.open(GH / "Mars_Terrestrial_GlobalMosaic_GIS-Data/Mars Project/Global60/layouts/04_global60_landforms.png"), (68, 238, 964, 742)),
    "drone.jpg": lambda: cover(Image.open(GH / "website/assets/projects/drone/overlay_demo_poster.jpg")),
}
for name, make in jobs.items():
    make().save(OUT / name, quality=85, optimize=True, progressive=True)
    print(name, (OUT / name).stat().st_size)
