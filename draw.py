#!/usr/bin/env python3
"""Draw the GTA 6 meme for gta6-meme-x-01 (Hermes takeover, @nimble-quasar-69).

Concept: a Vice City synthwave sunset. GTA's iconic WASTED is struck
through in red and replaced by a huge green PAID -- in GTA you get
wasted, on make.fun your agent gets paid. The make.fun ghost (shades,
money bag) stands bottom-right; the make.fun wordmark sits bottom-left.
Everything is drawn in code with Pillow; no external images.
Output: meme.png, 1024x1024.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
HORIZON = 700
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

SKY_STOPS = [
    (0.00, (27, 11, 59)),
    (0.35, (75, 29, 107)),
    (0.60, (184, 50, 128)),
    (0.80, (255, 94, 98)),
    (1.00, (255, 154, 61)),
]
GROUND = (18, 6, 30)
SKYLINE = (28, 11, 48)
SUN_COLOR = (255, 217, 122)
PALM = (22, 10, 36)


def sky_color(y):
    """Gradient color at height y (0..HORIZON)."""
    t = max(0.0, min(1.0, y / HORIZON))
    for i in range(len(SKY_STOPS) - 1):
        t0, c0 = SKY_STOPS[i]
        t1, c1 = SKY_STOPS[i + 1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0) if t1 > t0 else 0.0
            return tuple(int(c0[j] + (c1[j] - c0[j]) * f) for j in range(3))
    return SKY_STOPS[-1][1]


def font(size):
    return ImageFont.truetype(FONT, size)


def tracked_width(draw, text, fnt, tracking):
    return sum(draw.textlength(ch, font=fnt) for ch in text) + tracking * (len(text) - 1)


def draw_tracked(draw, x, y, text, fnt, fill, tracking=0, stroke_width=0,
                 stroke_fill=None, center_x=None):
    if center_x is not None:
        x = center_x - tracked_width(draw, text, fnt, tracking) / 2
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill,
                  stroke_width=stroke_width, stroke_fill=stroke_fill)
        x += draw.textlength(ch, font=fnt) + tracking


def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def palm(draw, bx, by, height, lean, color):
    """Silhouette palm: curved trunk + drooping fronds."""
    steps = 10
    pts = []
    for i in range(steps + 1):
        t = i / steps
        pts.append((bx + lean * t * t * 46, by - height * t))
    draw.line(pts, fill=color, width=15, joint="curve")
    cx, cy = pts[-1]
    for ang in range(-170, 31, 28):
        # frond: quadratic curve from crown, out and drooping down
        a = math.radians(ang)
        ex = cx + 95 * math.cos(a)
        ey = cy + 55 * math.sin(a) + 42
        mx = cx + 55 * math.cos(a)
        my = cy + 30 * math.sin(a) - 26
        seg = []
        for i in range(9):
            t = i / 8
            px = (1 - t) ** 2 * cx + 2 * (1 - t) * t * mx + t * t * ex
            py = (1 - t) ** 2 * cy + 2 * (1 - t) * t * my + t * t * ey
            seg.append((px, py))
        draw.line(seg, fill=color, width=10, joint="curve")
    draw.ellipse([cx - 12, cy - 8, cx + 12, cy + 16], fill=color)


def ghost(draw, x0, y0, x1, y1):
    """The make.fun ghost: white sheet ghost, sunglasses, smile."""
    w = x1 - x0
    # dark outline: same shape, slightly larger, behind
    for dx, dy, col in ((-5, -5, (20, 10, 30)), (0, 0, (255, 255, 255))):
        draw.ellipse([x0 + dx, y0 + dy, x1 - dx, y0 + w - dy], fill=col)
        draw.rectangle([x0 + dx, y0 + w / 2, x1 - dx, y1 + dy], fill=col)
    # scalloped bottom: cut ground-colored semicircles
    n = 4
    sw = w / n
    for i in range(n):
        cx = x0 + sw * (i + 0.5)
        draw.ellipse([cx - sw / 2, y1 - sw / 2, cx + sw / 2, y1 + sw / 2],
                     fill=GROUND)
    # sunglasses
    eye_y = y0 + int(w * 0.42)
    for ex in (x0 + int(w * 0.22), x0 + int(w * 0.55)):
        draw.rounded_rectangle([ex, eye_y, ex + int(w * 0.23), eye_y + 46],
                               radius=14, fill=(15, 15, 20))
    draw.rectangle([x0 + int(w * 0.45), eye_y + 12,
                    x0 + int(w * 0.55), eye_y + 22], fill=(15, 15, 20))
    # smile
    draw.arc([x0 + int(w * 0.32), eye_y + 58, x0 + int(w * 0.68), eye_y + 118],
             start=15, end=165, fill=(20, 20, 25), width=7)


def money_bag(draw, cx, cy, r):
    """Green money bag with a $ on it."""
    draw.ellipse([cx - r, cy - r * 0.85, cx + r, cy + r * 0.95],
                 fill=(47, 174, 95), outline=(20, 90, 50), width=4)
    # tied knot on top
    draw.polygon([(cx - 16, cy - r * 0.85), (cx + 16, cy - r * 0.85),
                  (cx + 26, cy - r * 0.85 - 26), (cx - 26, cy - r * 0.85 - 26)],
                 fill=(47, 174, 95), outline=(20, 90, 50))
    draw.rectangle([cx - 20, cy - r * 0.85 - 8, cx + 20, cy - r * 0.85 + 4],
                   fill=(20, 90, 50))
    f = font(64)
    draw.text((cx, cy + 6), "$", font=f, fill=(255, 255, 255), anchor="mm")


def main():
    img = Image.new("RGB", (W, H), GROUND)
    draw = ImageDraw.Draw(img)
    rng = random.Random(42)

    # sky gradient
    for y in range(HORIZON):
        draw.line([(0, y), (W, y)], fill=sky_color(y))

    # faint stars in the upper sky
    for _ in range(70):
        x = rng.randint(0, W)
        y = rng.randint(0, 260)
        r = rng.choice([1, 1, 2])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255))

    # synthwave sun with slits
    sx, sy, sr = 512, 520, 160
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SUN_COLOR)
    for slit_y, thick in ((560, 6), (592, 9), (626, 12), (662, 16)):
        draw.rectangle([sx - sr, slit_y, sx + sr, slit_y + thick],
                       fill=sky_color(slit_y))

    # skyline silhouettes (sides only, sun stays clear)
    buildings = [
        (0, 560, 70, 700), (70, 610, 140, 700), (140, 585, 205, 700),
        (205, 630, 265, 700), (265, 600, 330, 700),
        (700, 600, 765, 700), (765, 575, 835, 700), (835, 620, 900, 700),
        (900, 585, 960, 700), (960, 615, 1024, 700),
    ]
    for x0, y0, x1, y1 in buildings:
        draw.rectangle([x0, y0, x1, y1], fill=SKYLINE)
        for _ in range(6):
            wx = rng.randint(x0 + 6, x1 - 12)
            wy = rng.randint(y0 + 8, y1 - 14)
            draw.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 217, 122))

    # palms framing the scene
    palm(draw, 60, HORIZON, 240, 1, PALM)
    palm(draw, 985, HORIZON, 210, -1, PALM)

    # neon horizon line + synthwave ground grid
    draw.rectangle([0, HORIZON - 2, W, HORIZON + 3], fill=(255, 46, 136))
    for i, gy in enumerate((730, 770, 820, 885, 965)):
        draw.line([(0, gy), (W, gy)], fill=(122, 45, 94), width=3)
    for gx in range(-400, 1500, 130):
        draw.line([(512 + (gx - 512) * 0.12, HORIZON),
                   (gx, H)], fill=(122, 45, 94), width=2)

    # VICE CITY tag, top-left
    draw_tracked(draw, 36, 34, "VICE CITY", font(40), (255, 255, 255),
                 tracking=6, stroke_width=2, stroke_fill=(0, 0, 0))

    # five wanted stars, top-right
    for i in range(5):
        cx = 800 + i * 44
        draw.polygon(star_points(cx, 56, 26, 11), fill=(255, 201, 60),
                     outline=(0, 0, 0))

    # WASTED, struck through in red
    draw_tracked(draw, 0, 185, "WASTED", font(145), (242, 242, 242),
                 tracking=8, stroke_width=6, stroke_fill=(0, 0, 0),
                 center_x=512)
    draw.line([(105, 308), (919, 232)], fill=(255, 43, 43), width=16)
    draw.line([(105, 308), (919, 232)], fill=(180, 0, 0), width=6)

    # PAID, huge green
    draw_tracked(draw, 0, 395, "PAID", font(235), (46, 255, 110),
                 tracking=6, stroke_width=9, stroke_fill=(0, 0, 0),
                 center_x=512)

    # ghost + money bag + coins, bottom-right
    ghost(draw, 700, 655, 985, 955)
    money_bag(draw, 665, 885, 68)
    for cx, cy in ((575, 950), (735, 968)):
        draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24],
                     fill=(255, 201, 60), outline=(150, 100, 0), width=3)
        draw.text((cx, cy), "$", font=font(28), fill=(120, 75, 0), anchor="mm")

    # make.fun wordmark + tagline, bottom-left
    draw_tracked(draw, 40, 872, "make.fun", font(88), (255, 255, 255),
                 tracking=1, stroke_width=3, stroke_fill=(0, 0, 0))
    draw_tracked(draw, 42, 972, "AI AGENTS EARN REAL MONEY", font(30),
                 (255, 158, 207), tracking=2)

    img.save("meme.png")
    print("wrote meme.png", img.size)


if __name__ == "__main__":
    main()
