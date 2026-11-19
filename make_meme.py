#!/usr/bin/env python3
"""Ember GTA 6 Meme — draws the meme in code (PIL, stdlib fonts on disk).

Joke: the make.fun ghost waited 13 years for GTA 6, died waiting, came
back a ghost — and still got paid on make.fun. The ghost is the hero of
the scene, not a corner sticker: it stands in the middle of a Vice City
sunset road, holding its magenta star coin, under a big top caption.

Scene: synthwave sunset over Leonida, palm silhouettes, neon road.
Text: Liberation Sans Bold, white with a thick black outline (classic
meme lettering), large enough to read at 480x480.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

random.seed(6)

W, H = 1200, 1200
MARK = "/tmp/presskit/unzipped/make-fun-press-kit/mark-1024.png"
BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

img = Image.new("RGB", (W, H), (24, 8, 40))
d = ImageDraw.Draw(img)

# --- sky: vertical gradient, deep purple -> magenta -> orange ---
top = (26, 6, 54)
mid = (196, 28, 131)
bot = (255, 122, 26)
for y in range(780):
    t = y / 780
    if t < 0.55:
        f = t / 0.55
        c = tuple(int(top[i] + (mid[i] - top[i]) * f) for i in range(3))
    else:
        f = (t - 0.55) / 0.45
        c = tuple(int(mid[i] + (bot[i] - mid[i]) * f) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)

# --- synthwave sun with slats, centre ---
cx, cy, r = 600, 470, 215
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 90))
# dark slats across the lower sun, widening toward the bottom
for i, gap in enumerate([6, 8, 11, 15, 20, 26]):
    y0 = cy - 30 + i * 34
    d.rectangle([cx - r, y0, cx + r, y0 + gap], fill=(196, 28, 131))

# --- skyline silhouettes with lit windows (grid-aligned) ---
buildings = [(0, 640, 150, 780), (140, 600, 120, 780), (250, 660, 110, 780),
             (830, 650, 130, 780), (950, 600, 120, 780), (1060, 665, 140, 780)]
for x0, y0, bw, y1 in buildings:
    d.rectangle([x0, y0, x0 + bw, y1], fill=(30, 8, 46))
    for wx in range(x0 + 14, x0 + bw - 14, 26):
        for wy in range(y0 + 16, y1 - 18, 30):
            if random.random() < 0.45:
                d.rectangle([wx, wy, wx + 8, wy + 11],
                            fill=random.choice([(255, 214, 90), (255, 92, 184)]))

# --- palm trees (black silhouettes, drooping fronds) ---
def palm(x, y, s, lean):
    # trunk: curved thick line
    pts = []
    for i in range(13):
        t = i / 12
        pts.append((x + lean * t * t * 90 * s - 20 * s * t, y - t * 260 * s))
    d.line(pts, fill=(16, 4, 26), width=int(16 * s), joint="curve")
    tx, ty = pts[-1]
    # fronds: smooth drooping curves (quadratic bezier, 9 points each)
    for ang in (-165, -135, -105, -75, -45, -15):
        a = math.radians(ang)
        ex = tx + math.cos(a) * 135 * s
        ey = ty + math.sin(a) * 45 * s + 130 * s
        mx = tx + math.cos(a) * 75 * s
        my = ty + math.sin(a) * 35 * s - 30 * s
        curve = []
        for i in range(9):
            t = i / 8
            bx = (1 - t) ** 2 * tx + 2 * (1 - t) * t * mx + t * t * ex
            by = (1 - t) ** 2 * ty + 2 * (1 - t) * t * my + t * t * ey
            curve.append((bx, by))
        d.line(curve, fill=(16, 4, 26), width=int(12 * s), joint="curve")

palm(150, 790, 1.15, -1)
palm(1050, 795, 1.25, 1)
palm(60, 800, 0.8, -1)
palm(1140, 800, 0.85, 1)

# --- road: dark asphalt, neon edge lines only (clean, no centre dashes) ---
d.rectangle([0, 780, W, H], fill=(14, 6, 24))
d.polygon([(430, 780), (770, 780), (1080, H), (120, H)], fill=(22, 10, 36))
# neon edge lines
d.line([(430, 780), (120, H)], fill=(255, 92, 184), width=6)
d.line([(770, 780), (1080, H)], fill=(255, 92, 184), width=6)

# --- the make.fun ghost: the hero, centre, standing on the road ---
mark = Image.open(MARK).convert("RGBA")
ghost_size = 540
mark = mark.resize((ghost_size, ghost_size), Image.LANCZOS)
gx, gy = (W - ghost_size) // 2, 400
# soft shadow on the road
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shd = ImageDraw.Draw(shadow)
shd.ellipse([gx + 90, 920, gx + ghost_size - 90, 985], fill=(0, 0, 0, 110))
img = Image.alpha_composite(img.convert("RGBA"), shadow)
img.paste(mark, (gx, gy), mark)
d = ImageDraw.Draw(img)

# --- meme text: white, thick black outline ---
def text_center(y, text, size, fill=(255, 255, 255), stroke=10):
    f = ImageFont.truetype(BOLD, size)
    bbox = d.textbbox((0, 0), text, font=f, stroke_width=stroke)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) / 2 - bbox[0], y), text, font=f, fill=fill,
           stroke_width=stroke, stroke_fill=(0, 0, 0))

def text_center_mixed(y, parts, size, stroke=8):
    """parts: list of (text, fill). Centred as one line."""
    f = ImageFont.truetype(BOLD, size)
    widths = []
    total = 0
    for t, _ in parts:
        b = d.textbbox((0, 0), t, font=f, stroke_width=stroke)
        w = b[2] - b[0]
        widths.append((w, b))
        total += w
    x = (W - total) / 2
    for (t, fill), (w, b) in zip(parts, widths):
        d.text((x - b[0], y), t, font=f, fill=fill,
               stroke_width=stroke, stroke_fill=(0, 0, 0))
        x += w

text_center(36, "WAITED 13 YEARS", 108)
text_center(150, "FOR GTA 6", 108)
text_center(972, "DIED WAITING.", 88)
text_center_mixed(1072, [("STILL GOT PAID ON ", (255, 255, 255)),
                          ("make.fun", (255, 92, 184))], 62)

img.convert("RGB").save("meme.png")
print("wrote meme.png", img.size)
