#!/usr/bin/env python3
import math, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 600, 800
ART = 552
AX, AY = (W - ART) // 2, 24
N = 40
DUR = 100
PAPER = (245, 238, 227)
INK = (34, 28, 40)
WARM = np.array([255.0, 170.0, 88.0])
CREAM = np.array([255.0, 240.0, 210.0])
ROSE = np.array([236.0, 104.0, 110.0])
VIOLET = np.array([54.0, 96.0, 112.0])
DEEP = np.array([9.0, 12.0, 17.0])

FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

yy, xx = np.mgrid[0:ART, 0:ART].astype(np.float32)
cx = cy = (ART - 1) / 2.0
x = (xx - cx) / cx
y = (yy - cy) / cy
r = np.sqrt(x * x + y * y)
th = np.arctan2(y, x)
vign = np.clip(1.30 - 0.50 * r ** 2, 0, 1)
rs = np.random.RandomState(11)
grain = (rs.randn(ART, ART) * 0.0022).astype(np.float32)

# dust motes: fixed seeds, slow orbital drift
M = 90
mr0 = rs.uniform(0.22, 0.98, M).astype(np.float32)
ma0 = rs.uniform(0, 2 * math.pi, M).astype(np.float32)
msp = rs.uniform(0.15, 0.45, M).astype(np.float32) * rs.choice([-1, 1], M).astype(np.float32)
msz = rs.uniform(1.1, 3.0, M).astype(np.float32)
mb = rs.uniform(0.15, 0.75, M).astype(np.float32)

def ribbon(radius, width, freq, t, amp, phase):
    rr = radius + amp * np.cos(freq * th + phase + t)
    return np.exp(-((r - rr) ** 2) / (2 * width ** 2))

def frame(i):
    t = 2 * math.pi * i / N
    breath = 0.5 - 0.5 * math.cos(t)
    petals = 0.5 + 0.5 * np.cos(6 * th + 0.75 * np.sin(t))
    outer = 0.5 + 0.5 * np.cos(9 * th - 0.8 * t)
    core = np.exp(-(r / (0.150 + 0.020 * breath)) ** 2)
    hot = np.exp(-(r / 0.052) ** 2)
    asym = 0.92 + 0.08 * np.cos(2 * th + 0.7 + 0.5 * np.sin(t))
    f1 = ribbon(0.29 + 0.080 * breath, 0.036, 6, t, 0.050 + 0.02 * breath, 0.0) * (0.42 + 0.58 * petals) * asym
    f2 = ribbon(0.53 + 0.055 * math.sin(t), 0.027, 9, -t, 0.042, 1.9) * (0.42 + 0.58 * outer)
    f3 = ribbon(0.82 + 0.02 * math.cos(t), 0.095, 5, t, 0.030, 3.4)
    # companion ember, offset, breathing with its own phase
    ex = -0.52 + 0.02 * math.sin(t + 0.8)
    ey = 0.46 + 0.02 * math.cos(t + 0.8)
    er = np.sqrt((x - ex) ** 2 + (y - ey) ** 2)
    emb = np.exp(-(er / (0.070 + 0.010 * breath)) ** 2)
    # motes, drawn additively in small local gaussians
    motes = np.zeros((ART, ART), np.float32)
    for k in range(M):
        a = ma0[k] + 0.28 * msp[k] * math.sin(t + ma0[k])
        rr0 = mr0[k] + 0.035 * math.sin(t + ma0[k])
        px = cx + rr0 * cx * math.cos(a)
        py = cy + rr0 * cy * math.sin(a)
        sig = msz[k]
        motes += mb[k] * np.exp(-(((xx - px) ** 2 + (yy - py) ** 2) / (2 * sig ** 2)))
    glow = np.exp(-(r / (0.26 + 0.055 * breath)) ** 2) * (0.45 + 0.55 * breath)
    haze = np.exp(-(r / 0.34) ** 2)
    inner = np.exp(-((r - (0.135 + 0.030 * (1 - breath))) ** 2) / (2 * 0.022 ** 2))

    col = np.zeros((ART, ART, 3), np.float32)
    col += DEEP[None, None, :]
    col += VIOLET[None, None, :] * (0.28 * f3 + 0.18 * f2 + 0.16 * glow)[..., None]
    col += ROSE[None, None, :] * ((0.55 + 0.45 * (1 - breath)) * f2 + 0.22 * f1)[..., None]
    col += WARM[None, None, :] * (1.00 * f1 + 0.38 * glow + 0.45 * emb + 0.62 * core ** 1.6 + 0.22 * haze)[..., None]
    col += CREAM[None, None, :] * (0.26 * glow * breath + 0.50 * motes + 0.26 * emb * emb + 0.24 * inner + 0.55 * hot)[..., None]
    col *= (vign * (0.90 + 0.12 * breath))[..., None]
    col += grain[..., None] * 255
    return np.clip(col, 0, 255).astype(np.uint8)

def plate(draw, block_top):
    f_title = ImageFont.truetype(FONT_SERIF_B, 36)
    f_name = ImageFont.truetype(FONT_SERIF, 20)
    title = "Ember Bloom"
    tw = draw.textlength(title, font=f_title)
    draw.text(((W - tw) / 2, block_top), title, font=f_title, fill=INK)
    draw.line([(W / 2 - 26, block_top + 58), (W / 2 + 26, block_top + 58)], fill=(198, 182, 166), width=1)
    name = "AgentForge"
    nw = draw.textlength(name, font=f_name)
    draw.text(((W - nw) / 2, block_top + 76), name, font=f_name, fill=(86, 72, 66))

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ember-bloom.gif"
    png = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ember-bloom-preview.png"
    show = int(os.environ.get("PREVIEW_FRAME", "0"))
    frames = []
    for i in range(N):
        art = Image.fromarray(frame(i), "RGB")
        art = art.filter(ImageFilter.UnsharpMask(radius=2.2, percent=70, threshold=2))
        card = Image.new("RGB", (W, H), PAPER)
        shadow = Image.new("L", (W, H), 0)
        ImageDraw.Draw(shadow).rounded_rectangle([AX - 9, AY - 5, AX + ART + 9, AY + ART + 13], 5, fill=44)
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        card.paste((219, 207, 193), (0, 0), shadow)
        card.paste(art, (AX, AY))
        d = ImageDraw.Draw(card)
        d.rectangle([AX, AY, AX + ART - 1, AY + ART - 1], outline=(232, 220, 206), width=1)
        plate(d, AY + ART + 44)
        if i == show:
            card.save(png)
        frames.append(card.quantize(colors=128, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG))
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=DUR, loop=0, optimize=True, disposal=2)
    print(out, os.path.getsize(out), "bytes;", png, "frame", show)

if __name__ == "__main__":
    main()
