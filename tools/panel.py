"""The frame the profile's wide panels share: activity.py, breakeven.py, flybys.py,
languages.py and pipeline.py all start their SVG with `background`, and all but the last
write their alt text into the README with `write_alt`.

It draws the tiles' navy gradient in a rounded border, a field of still stars, and a few
twinkling ones drawn after them (so adding twinkles never moved a still star), then opens
the panel's own <defs> and <style>. Every animation in the profile stops under
prefers-reduced-motion; `animated` names the classes a panel adds, and the rule that
stops them is written here, beside the twinkle's, so no panel can forget it.

Each panel's finished SVG goes through `keep_clear`, which takes out the stars that would
sit in its text or on its lines, bars and dots, where a star reads as a stray mark or a
data point. The tiles and the banner use it too.
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


# A background star, still or twinkling, as background() and the tiles, banner and footer
# write one. Anything else round (a data dot, the Earth) is a mark.
STAR = re.compile(r'<circle (?:class="tw" )?cx="([\d.]+)" cy="([\d.]+)" r="[\d.]+" fill="#(?:fff|dbe7ff)"[^>]*/>')
TAG = re.compile(r'<(/?)(g|text|line|rect|circle)\b([^>]*?)/?>')
# Average advance of a character, in ems: a little over Segoe UI's and Helvetica's, so a
# box errs wide.
EM = {"400": 0.58, "700": 0.62}


def attrs(text):
    return dict(re.findall(r'([\w-]+)="([^"]*)"', text))


def marks(svg):
    """The boxes (x0, y0, x1, y1) of what an svg draws over its stars: each line of text, as
    wide as its characters at its font size (inherited from its <g> when it has none), each
    line, each rect but the frame, and each circle that is not a star. Text in a clipped
    group is left out: it shows only through its clip, whose rect counts instead (the tiles'
    odometer keeps its unseen digits above the number)."""
    boxes, groups = [], [{}]
    for m in TAG.finditer(svg):
        close, tag, a = m[1], m[2], attrs(m[3])
        if tag == "g":
            if close:
                groups.pop()
            elif not m[0].endswith("/>"):
                groups.append({**groups[-1], **a})
        elif tag == "text" and not close and "clip-path" not in groups[-1]:
            a = {**groups[-1], **a}
            body = re.sub(r"<[^>]+>", "", svg[m.end():svg.index("</text>", m.end())])
            size = float(a.get("font-size", 16))
            width = len(html.unescape(body)) * size * EM.get(a.get("font-weight", "400"), EM["400"])
            x, y = float(a.get("x", 0)), float(a.get("y", 0))
            x -= {"middle": width / 2, "end": width}.get(a.get("text-anchor", "start"), 0)
            boxes.append((x, y - size * 0.8, x + width, y + size * 0.25))
        elif tag == "line":
            x1, y1, x2, y2 = (float(a.get(k, 0)) for k in ("x1", "y1", "x2", "y2"))
            boxes.append((min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))
        elif tag == "rect" and "x" in a and a.get("fill") != "url(#g)":
            x, y = float(a["x"]), float(a.get("y", 0))
            boxes.append((x, y, x + float(a["width"]), y + float(a["height"])))
        elif tag == "circle" and not STAR.match(m[0]) and "cx" in a:
            cx, cy, r = float(a["cx"]), float(a["cy"]), float(a.get("r", 0))
            boxes.append((cx - r, cy - r, cx + r, cy + r))
    return boxes


def clear_boxes(svg, pad=10):
    """The boxes of svg's marks (see marks), each grown by pad: where no star should be."""
    return [(x0 - pad, y0 - pad, x1 + pad, y1 + pad) for x0, y0, x1, y1 in marks(svg)]


def is_clear(boxes, x, y):
    return not any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in boxes)


def keep_clear(svg, pad=10):
    """svg without the stars that would sit on its marks or within pad of one, so no star
    lands in a word or on a chart's line where it could pass for a point. The rest stay
    where they were."""
    boxes = clear_boxes(svg, pad)
    return STAR.sub(lambda m: m[0] if is_clear(boxes, float(m[1]), float(m[2])) else "", svg)


def write_alt(readme, image, alt):
    """The README with alt written into the full-width <img> of docs/<image>, so a screen
    reader hears what the panel shows. Stops unless that image is there exactly once."""
    pattern = rf'(src="docs/{re.escape(image)}" width="100%" alt=")[^"]*(")'
    readme, n = re.subn(pattern, lambda m: m[1] + html.escape(alt, quote=False).replace('"', '&quot;') + m[2], readme)
    if n != 1:
        sys.exit(f"README image docs/{image} matched {n} times, expected 1")
    return readme
