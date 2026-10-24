"""Build the gallery cards for the profile README (docs/gallery/*.webp).

Each card is a project image inset in the stat tiles' dark starfield frame, with the
repo name and a caption under it. `<name>.webp` is for desktop widths, where two cards
share a row and each is about 400px wide. `<name>-compact.webp` drops the caption and
enlarges the name, for phones, where each card is about 170px wide; the README swaps it
in with <picture>, as it does for the tiles.

Cards are drawn at twice their display size so the text stays sharp on high-DPI
screens, and saved as WebP so the rounded corners can be transparent in both GitHub
themes. Images come from the local clones beside this repo (GH); needs Pillow and numpy.

The cards in MOTION also come animated, from the project's demo video (needs ffmpeg) or
from the project itself running (sim_clip.py).
"""
import random
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# The folder holding this repo and the project clones, on either machine.
GH = Path(__file__).resolve().parents[2]
FONTS = Path(r"C:\Windows\Fonts")
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

S = 2                      # supersampling: everything below is in display pixels times S
W = 800 * S                # card width
PAD = 16 * S               # frame around the image
IW, IH = W - 2 * PAD, (W - 2 * PAD) * 9 // 16
NAVY = (14, 24, 48)


def fit(img, bg=NAVY):
    """Letterbox img onto an IW x IH canvas of colour bg."""
    img = img.convert("RGB")
    img.thumbnail((IW, IH), Image.LANCZOS)
    canvas = Image.new("RGB", (IW, IH), bg)
    canvas.paste(img, ((IW - img.width) // 2, (IH - img.height) // 2))
    return canvas


def cover(img, box=None):
    """Crop img to box (if given), then scale to fill IW x IH, centre-cropping the excess."""
    img = img.convert("RGB")
    if box:
        img = img.crop(box)
    s = max(IW / img.width, IH / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    l, t = (img.width - IW) // 2, (img.height - IH) // 2
    return img.crop((l, t, l + IW, t + IH))


def dark(img):
    """A dark version of a white-background figure: invert lightness, keep hue.

    Shifting every channel by 1 - max - min swaps white and black but leaves a colour's
    hue (a red stays red), so the figure's own legend still matches its marks. Black
    then becomes the cards' navy so the plot sits in the palette.
    """
    rgb = np.asarray(img.convert("RGB")).astype(np.float64) / 255
    rgb = np.clip(rgb + 1 - rgb.max(axis=2, keepdims=True) - rgb.min(axis=2, keepdims=True), 0, 1)
    rgb = rgb + (1 - rgb.max(axis=2, keepdims=True)) * (np.array(NAVY) / 255)
    return Image.fromarray((np.clip(rgb, 0, 1) * 255).round().astype(np.uint8))


def rounded_mask(size, radius):
    """An anti-aliased rounded-rectangle mask, drawn at 4x and scaled down."""
    big = Image.new("L", (size[0] * 4, size[1] * 4), 0)
    ImageDraw.Draw(big).rounded_rectangle((0, 0, big.width - 1, big.height - 1), radius * 4, fill=255)
    return big.resize(size, Image.LANCZOS)


def frame(h, seed):
    """The tiles' frame: diagonal navy gradient, faint stars, a thin border."""
    y, x = np.mgrid[0:h, 0:W]
    t = (x / W + y / h) / 2
    stops = [(0, (11, 16, 32)), (0.6, (15, 30, 61)), (1, (17, 38, 80))]
    rgb = np.zeros((h, W, 3))
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        m = (t >= t0) & (t <= t1)
        f = ((t - t0) / (t1 - t0))[m][:, None]
        rgb[m] = np.array(c0) * (1 - f) + np.array(c1) * f
    card = Image.fromarray(rgb.round().astype(np.uint8))
    d = ImageDraw.Draw(card, "RGBA")
    rng = random.Random(seed)
    for _ in range(40):
        cx, cy, r = rng.uniform(0, W), rng.uniform(0, h), rng.choice([0.6, 0.8, 1.0]) * S
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, int(rng.uniform(0.2, 0.6) * 255)))
    border = Image.new("RGBA", card.size, (0, 0, 0, 0))
    ImageDraw.Draw(border).rounded_rectangle((S // 2, S // 2, W - 1 - S // 2, h - 1 - S // 2), 16 * S, outline=(42, 59, 99), width=S)
    card.paste(border, (0, 0), border)
    return card


def card(img, title, caption, seed, compact):
    title_font = ImageFont.truetype(str(FONTS / "segoeuib.ttf"), (64 if compact else 30) * S)
    text_font = ImageFont.truetype(str(FONTS / "segoeui.ttf"), 22 * S)
    caption_h = (96 if compact else 92) * S
    h = PAD + IH + caption_h
    out = frame(h, seed)
    out.paste(img, (PAD, PAD), rounded_mask((IW, IH), 10 * S))
    d = ImageDraw.Draw(out)
    top = PAD + IH
    if compact:
        d.text((W // 2, top + caption_h // 2 - 4 * S), title, font=title_font, fill=(91, 163, 220), anchor="mm")
    else:
        d.text((PAD + 4 * S, top + 40 * S), title, font=title_font, fill=(91, 163, 220), anchor="ls")
        d.text((PAD + 4 * S, top + 74 * S), caption, font=text_font, fill=(219, 227, 245), anchor="ls")
        assert d.textlength(caption, font=text_font) < IW, f"caption too long: {caption}"
    assert d.textlength(title, font=title_font) < IW, f"title too long: {title}"
    out = out.convert("RGBA")
    out.putalpha(rounded_mask(out.size, 16 * S))
    return out


# name: (image, repo name, caption). The caption is also the README's alt text.
CARDS = {
    "satellite": (lambda: cover(Image.open(GH / "Satellite Space Flight/docs/images/overview.png")),
                  "Satellite-Space-Flight", "The ISS orbit, live elements and ground-station passes"),
    "belt": (lambda: fit(dark(Image.open(GH / "asteroid-belt-gradient/figures/fig1b_stacked_composition.png"))),
             "asteroid-belt-gradient", "S-types give way to C-types farther from the Sun"),
    "mars": (lambda: cover(Image.open(GH / "Mars_Terrestrial_GlobalMosaic_GIS-Data/Mars Project/Global60/layouts/04_global60_landforms.png"), (68, 238, 964, 742)),
             "Mars Global Mosaic", "SVM landform classes across Tharsis and Valles Marineris"),
    "drone": (lambda: cover(Image.open(GH / "website/assets/projects/drone/overlay_demo_poster.jpg")),
              "drone-target-id", "Per-target valid/invalid scores on aerial footage"),
}
def clip(video, start, seconds, fps):
    """The video's frames from start for seconds, fps a second, as images."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["ffmpeg", "-v", "error", "-ss", str(start), "-t", str(seconds), "-i", str(video),
                        "-vf", f"fps={fps}", str(Path(tmp, "%03d.png"))], check=True)
        return [Image.open(f).convert("RGB") for f in sorted(Path(tmp).glob("*.png"))]


def simulation(frames):
    """frames frames of Satellite-Space-Flight running, one ISS orbit (sim_clip.py)."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable, str(Path(__file__).with_name("sim_clip.py")), tmp, str(frames)], check=True)
        return [Image.open(f).convert("RGB") for f in sorted(Path(tmp).glob("*.png"))]


# name: (frames at a given rate, frames a second). These cards also come as an animated
# `<name>-motion.webp` (and `-motion-compact`): the project moving, in the same frame. The
# README shows the still card to anyone who asks for reduced motion, since an animated
# image can't be paused by CSS. Kept short and at the display size (2x, not 4x) so each
# file stays near a megabyte.
MOTION = {
    # A drone pass with targets scored as they come into view, from the demo video.
    "drone": (lambda fps: clip(GH / "website/assets/projects/drone/overlay_demo.mp4", 9.0, 5.0, fps), 10),
    # The overview scene through one ISS orbit, in six seconds.
    "satellite": (lambda fps: simulation(6 * fps), 10),
}


def save(frames, path, compact, fps=None):
    """Save one card, or an animation of several, at the display size for its width."""
    scale = 4 if fps and compact else 2 if fps or compact else 1
    if scale > 1:   # the still compact card is shown about 170px wide, so half is still 2x
        frames = [f.resize((f.width // scale, f.height // scale), Image.LANCZOS) for f in frames]
    if fps:
        frames[0].save(path, save_all=True, append_images=frames[1:], duration=round(1000 / fps), loop=0,
                       quality=70, method=6, minimize_size=True)
    else:
        frames[0].save(path, quality=82, method=6)
    print(path.name, path.stat().st_size)


for i, (name, (make, title, caption)) in enumerate(CARDS.items()):
    img = make()
    for compact, suffix in ((False, ""), (True, "-compact")):
        save([card(img, title, caption, 200 + i, compact)], OUT / f"{name}{suffix}.webp", compact)
    if name in MOTION:
        make_frames, fps = MOTION[name]
        frames = [cover(f) for f in make_frames(fps)]
        for compact, suffix in ((False, "-motion"), (True, "-motion-compact")):
            save([card(f, title, caption, 200 + i, compact) for f in frames], OUT / f"{name}{suffix}.webp", compact, fps)
