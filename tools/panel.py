"""The frame the profile's wide panels share: activity.py, breakeven.py, flybys.py,
languages.py and pipeline.py all start their SVG with `background`, and all but the last
write their alt text into the README with `write_alt`.

It draws the tiles' navy gradient in a rounded border, a field of still stars, and a few
twinkling ones drawn after them (so adding twinkles never moved a still star), then opens
the panel's own <defs> and <style>. Every animation in the profile stops under
prefers-reduced-motion; `animated` names the classes a panel adds, and the rule that
stops them is written here, beside the twinkle's, so no panel can forget it.
"""
import html
import random
import re
import sys

GRADIENT = ('<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/>'
            '<stop offset="0.6" stop-color="#0f1e3d"/><stop offset="1" stop-color="#112650"/></linearGradient>')
TWINKLE = (".tw { animation: tw 4s ease-in-out infinite; }",
           "@keyframes tw { 0%, 100% { opacity: 0.15; } 50% { opacity: 1; } }")
# Rules more than one panel uses: bars that grow from their left end, and a fade-in.
GROW = (".grow { transform-box: fill-box; transform-origin: left center; animation: grow 1.1s cubic-bezier(0.2, 0.7, 0.2, 1) both; }",
        "@keyframes grow { from { transform: scaleX(0); } }")
FADE = (".fade { animation: fade 0.8s ease-out both; }",
        "@keyframes fade { from { opacity: 0; } }")


def background(w, h, seed, alt, defs=(), rules=(), animated=()):
    """The opening of a w x h panel: the svg element (alt is its aria-label), <defs> with the
    gradient and defs, <style> with the twinkle and rules (one CSS rule a line), the frame and
    the stars. animated: the classes rules animate, stopped with the twinkle under reduced
    motion. seed fixes the stars, so a panel redraws the same."""
    rng = random.Random(seed)
    stars = "".join(
        f'<circle cx="{rng.uniform(8, w - 8):.1f}" cy="{rng.uniform(8, h - 8):.1f}" r="{rng.choice([0.6, 0.8, 1.0])}" fill="#fff" opacity="{rng.uniform(0.2, 0.6):.2f}"/>'
        for _ in range(int(w * h / 4500))
    )
    # Drawn after the still stars, so those stay where they were.
    twinkles = "".join(
        f'<circle class="tw" cx="{rng.uniform(8, w - 8):.1f}" cy="{rng.uniform(8, h - 8):.1f}" r="{rng.choice([1.1, 1.3])}" '
        f'fill="#dbe7ff" style="animation-delay:-{rng.uniform(0, 4):.2f}s;animation-duration:{rng.uniform(3, 6):.2f}s"/>'
        for _ in range(int(w * h / 60000))
    )
    head = f"<defs>{GRADIENT}</defs>" if not defs else "<defs>\n" + "\n".join((GRADIENT, *defs)) + "\n</defs>"
    css = "\n".join(f"  {rule}" for rule in (*TWINKLE, *rules))
    stopped = ", ".join(f".{c}" for c in ("tw", *animated))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{html.escape(alt)}">
{head}
<style>
{css}
  @media (prefers-reduced-motion: reduce) {{ {stopped} {{ animation: none; }} }}
</style>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="url(#g)" stroke="#2a3b63"/>
{stars}
{twinkles}
"""


def write_alt(readme, image, alt):
    """The README with alt written into the full-width <img> of docs/<image>, so a screen
    reader hears what the panel shows. Stops unless that image is there exactly once."""
    pattern = rf'(src="docs/{re.escape(image)}" width="100%" alt=")[^"]*(")'
    readme, n = re.subn(pattern, lambda m: m[1] + html.escape(alt, quote=False).replace('"', '&quot;') + m[2], readme)
    if n != 1:
        sys.exit(f"README image docs/{image} matched {n} times, expected 1")
    return readme
