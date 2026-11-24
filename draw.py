#!/usr/bin/env python3
"""Draw the 23 November 2026 front page: 31 stories, 6 regions, 1024x1024."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FD, "DejaVuSerif.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")

def F(path, size):
    return ImageFont.truetype(path, size)

# palette
INK = (20, 20, 20)
PAPER = (250, 246, 236)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
NAVY = (15, 42, 74)
GREY = (90, 90, 90)
LGREY = (200, 200, 200)
GREEN = (34, 120, 60)
AMBER = (200, 130, 0)
BLUE = (30, 90, 170)
GOLD = (191, 143, 0)
PURPLE = (112, 48, 160)
ORANGE = (197, 90, 17)
TEAL = (46, 125, 50)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit_lines(draw, text, font_sizes, font_path, max_w, max_lines):
    """Try font sizes in order; return (font, lines) that fits max_lines."""
    for sz in font_sizes:
        f = F(font_path, sz)
        lines = wrap(draw, text, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
    f = F(font_path, font_sizes[-1])
    return f, wrap(draw, text, f, max_w)[:max_lines]

def draw_chip(x, y, label, fill):
    f = F(SANS_B, 9)
    tw = d.textlength(label, font=f)
    w = int(tw) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=fill)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w

# ---------- masthead ----------
d.rectangle([0, 0, W, 6], fill=RED)
f_mast = F(SERIF_B, 54)
d.text((24, 8), "THE WORLD TODAY", font=f_mast, fill=INK)
f_r = F(SANS_B, 15)
d.text((W - 24 - d.textlength("31 STORIES", font=f_r), 14), "31 STORIES", font=f_r, fill=INK)
d.text((W - 24 - d.textlength("6 REGIONS", font=f_r), 34), "6 REGIONS", font=f_r, fill=INK)
f_date = F(SANS_B, 21)
d.text((24, 64), "MONDAY 23 NOVEMBER 2026", font=f_date, fill=RED)
f_kick = F(SANS_B, 12)
kt = "AI ROUT  ·  AI RULES  ·  POWER SHIFT"
d.text((W - 24 - d.textlength(kt, font=f_kick), 68), kt, font=f_kick, fill=GREY)

# ---------- number strip ----------
nums = [
    ("-3.3%", "KOSPI"),
    ("5.3", "US-CHINA GAP"),
    ("11,762", "EBOLA CASES"),
    ("10T WON", "SEOUL FUND"),
    ("$450M", "SKUBAL DEAL"),
    ("$107.3B", "ANTHROPIC IPO"),
]
x0, y0, cw = 24, 90, 162
for i, (n, lab) in enumerate(nums):
    x = x0 + i * cw
    if i:
        d.line([x - 1, y0 + 4, x - 1, y0 + 34], fill=LGREY, width=1)
    f_n = F(SANS_B, 27)
    tw = d.textlength(n, font=f_n)
    d.text((x + (cw - tw) / 2, y0), n, font=f_n, fill=RED)
    f_l = F(SANS_B, 10)
    tw = d.textlength(lab, font=f_l)
    d.text((x + (cw - tw) / 2, y0 + 30), lab, font=f_l, fill=INK)

# ---------- region bar ----------
regions = [
    ("NORTH AMERICA 8", 8, (31, 78, 121)),
    ("EUROPE 6", 6, ORANGE),
    ("MIDDLE EAST 6", 6, PURPLE),
    ("ASIA-PACIFIC 6", 6, TEAL),
    ("AFRICA 3", 3, GOLD),
    ("WORLD 2", 2, (89, 89, 89)),
]
bx, by, bw = 24, 130, 976
x = bx
f_rb = F(SANS_B, 11)
for name, cnt, col in regions:
    seg = bw * cnt / 31
    d.rectangle([x, by, x + seg, by + 20], fill=col)
    tw = d.textlength(name, font=f_rb)
    if tw < seg - 8:
        d.text((x + (seg - tw) / 2, by + 4), name, font=f_rb, fill=(255, 255, 255))
    x += seg

# ---------- UTC strip ----------
d.rectangle([24, 154, 1000, 172], fill=NAVY)
f_u = F(SANS_B, 12)
utc = "THE DAY IN UTC   ·   ~00:00 ASIA OPENS   ·   06:30 KOSPI -3.3%   ·   ~09:00 SEOUL FUND   ·   14:30 WALL ST +3%   ·   ~16:00 GUTERRES   ·   ~21:00 FBI HACK   (~ = APPROX.)"
d.text((30, 157), utc, font=f_u, fill=(255, 255, 255))

# ---------- hero scenes ----------
HX, HY, HW, HGAP = 24, 178, 318, 10
SCENE_H = 104

def scene_kospi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # skyline
    import random
    rnd = random.Random(7)
    bx0 = x
    while bx0 < x + w - 14:
        bw_ = rnd.randint(14, 26)
        bh_ = rnd.randint(18, 52)
        d.rectangle([bx0, y + h - bh_, bx0 + bw_, y + h], fill=(24, 62, 105))
        for wy in range(y + h - bh_ + 4, y + h - 4, 8):
            for wx in range(bx0 + 3, bx0 + bw_ - 3, 7):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 205, 80))
        bx0 += bw_ + 2
    # falling chart
    pts = [(x + 12, y + 22), (x + 55, y + 34), (x + 100, y + 28), (x + 150, y + 46),
           (x + 195, y + 40), (x + 240, y + 62), (x + 290, y + 78)]
    d.line(pts, fill=(235, 70, 70), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255))
    f_big = F(SANS_B, 30)
    d.text((x + w - 118, y + 4), "-3.3%", font=f_big, fill=(235, 70, 70))
    f_s = F(SANS_B, 11)
    d.text((x + 8, y + 4), "intraday -5.8%", font=f_s, fill=(255, 255, 255))

def scene_guterres(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # globe
    cx, cy, r = x + 62, y + 54, 36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 200))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    for k in range(-2, 3):
        d.arc([cx - r, cy - r + k * 14, cx + r, cy + r + k * 14], 0, 360, fill=(200, 225, 245))
    d.ellipse([cx - 12, cy - r, cx + 12, cy + r], outline=(200, 225, 245), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(200, 225, 245), width=1)
    # network nodes
    import random
    rnd = random.Random(11)
    nodes = []
    for _ in range(9):
        nx = x + rnd.randint(140, 300)
        ny = y + rnd.randint(12, 92)
        nodes.append((nx, ny))
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if ((nodes[i][0] - nodes[j][0]) ** 2 + (nodes[i][1] - nodes[j][1]) ** 2) ** 0.5 < 70:
                d.line([nodes[i], nodes[j]], fill=(150, 190, 230), width=1)
    for nx, ny in nodes:
        d.ellipse([nx - 4, ny - 4, nx + 4, ny + 4], fill=(255, 205, 80))
    # podium silhouette
    d.ellipse([x + w - 42, y + h - 40, x + w - 26, y + h - 24], fill=(10, 10, 10))
    d.polygon([(x + w - 48, y + h), (x + w - 20, y + h), (x + w - 26, y + h - 26),
               (x + w - 42, y + h - 26)], fill=(10, 10, 10))
    f_b = F(SANS_B, 11)
    d.rectangle([x + 118, y + 6, x + 118 + d.textlength("150 DELEGATES", font=f_b) + 12, y + 22], fill=(255, 205, 80))
    d.text((x + 124, y + 8), "150 DELEGATES", font=f_b, fill=(20, 20, 20))

def scene_power(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=LGREY, width=1)
    f_t = F(SANS_B, 13)
    d.text((x + 10, y + 6), "ASIA POWER INDEX 2026", font=f_t, fill=INK)
    bars = [("US", 78.9, (31, 78, 121)), ("CHINA", 73.6, RED), ("INDIA", 40.5, (150, 150, 150))]
    f_bl = F(SANS_B, 11)
    yy = y + 28
    for lab, val, col in bars:
        d.text((x + 10, yy), lab, font=f_bl, fill=INK)
        bx0 = x + 66
        bw_ = int((w - 66 - 52) * val / 80.0)
        d.rectangle([bx0, yy + 1, bx0 + bw_, yy + 12], fill=col)
        d.text((bx0 + bw_ + 5, yy), f"{val:.1f}", font=f_bl, fill=INK)
        yy += 18
    f_g = F(SANS_B, 13)
    d.text((x + 10, yy + 2), "GAP 5.3", font=f_g, fill=RED)
    f_gs = F(SANS, 11)
    d.text((x + 78, yy + 3), "narrowest since 2018", font=f_gs, fill=INK)

heroes = [
    ("#1 ASIA · MARKETS", "AI ROUT HITS ASIA",
     "Kospi closes 4,708.54, sheds 161 pts. Samsung -3.1%, SK Hynix -2.5%.",
     "Source: Yonhap · Korea JoongAng", "REPORTED", GREEN, scene_kospi),
    ("#2 WORLD · UNITED NATIONS", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
     "Source: UN News · Reuters", "REPORTED", GREEN, scene_guterres),
    ("#3 WORLD · POWER", "US LEAD OVER CHINA AT RECORD LOW",
     "Gap 5.3 narrowest since 2018. US diplomatic influence -6 to 76.7. India third at 40.5.",
     "Source: Lowy Institute", "REPORTED", GREEN, scene_power),
]
for i, (kick, title, body, src, chip, chip_col, scene_fn) in enumerate(heroes):
    hx = HX + i * (HW + HGAP)
    scene_fn(hx, HY, HW, SCENE_H)
    ty = HY + SCENE_H + 6
    f_k = F(SANS_B, 11)
    d.text((hx, ty), kick, font=f_k, fill=RED)
    ty += 15
    f_t, tlines = fit_lines(d, title, [17, 16, 15], SERIF_B, HW, 2)
    for ln in tlines:
        d.text((hx, ty), ln, font=f_t, fill=INK)
        ty += 20
    f_b, blines = fit_lines(d, body, [12, 11, 10], SANS, HW, 2)
    for ln in blines:
        d.text((hx, ty), ln, font=f_b, fill=(40, 40, 40))
        ty += 15
    f_s = F(SANS, 9)
    d.text((hx, ty + 2), src, font=f_s, fill=GREY)
    draw_chip(hx + HW - 78, ty, chip, chip_col)

# ---------- small cards ----------
cards = [
    ("#4 SPORT · US", (31, 78, 121), "Skubal signs $450M Mets deal",
     "Two-time Cy Young winner, nine years — the largest ever for a pitcher.",
     "ESPN", "REPORTED", GREEN),
    ("#5 TECH · US", (31, 78, 121), "Anthropic IPO: $107.3B, largest ever",
     "Claude maker raised at $83 a share on 19 Nov; debut close $97.17.",
     "Bloomberg", "REPORTED", GREEN),
    ("#6 EUROPE · WAR", ORANGE, "Poland: 3 Russian missiles crossed airspace",
     "Kyiv says three Kh-101 entered Poland on Friday; Tusk: provocation.",
     "AP", "CLAIM", AMBER),
    ("#7 EUROPE · SECURITY", ORANGE, "Intel warns of Russian nuclear satellite",
     "Moscow built a satellite to carry a nuclear warhead; launch possible next month.",
     "Bloomberg", "CLAIM", AMBER),
    ("#8 EUROPE · ECONOMY", ORANGE, "Paris: 100+ back 2% billionaire tax",
     "Economists, politicians, unions rally behind France's 2% wealth tax.",
     "AFP", "REPORTED", GREEN),
    ("#9 EUROPE · UK", ORANGE, "Manchester: 12,000 cleared after scare",
     "Substance scare empties arena district; no casualties reported.",
     "AP", "REPORTED", GREEN),
    ("#10 EUROPE · WAR", ORANGE, "Zelenskyy: 165 Russian missiles in a week",
     "Kyiv says Moscow fired 165 missiles in seven days as US delays Patriots.",
     "Kyiv", "CLAIM", AMBER),
    ("#11 EUROPE · CLIMATE", ORANGE, "COP31: the day after",
     "Sunday's collapse — 194 nations reject the Antalya pact — draws fury.",
     "CNN", "REPORTED", GREEN),
    ("#12 AFRICA · LIBYA", GOLD, "Benghazi: UN demands probe of port attacks",
     "Drones hit two Russian ships; UN calls for an investigation.",
     "UN News", "CLAIM", AMBER),
    ("#13 MIDDLE EAST · ISRAEL", PURPLE, "Israel unity talks resume",
     "Likud and Gantz's Yesh Atid return to the table after Sunday's stall.",
     "Reuters", "ONGOING", BLUE),
]
CX, CY, CW2, CH2, CGAP = 24, 372, 188, 100, 8
for idx, (kick, col, title, body, src, chip, chip_col) in enumerate(cards):
    row, c = divmod(idx, 5)
    cx = CX + c * (CW2 + CGAP)
    cy = CY + row * (CH2 + 6)
    d.rectangle([cx, cy, cx + CW2, cy + CH2], outline=(180, 180, 180), width=1, fill=(255, 255, 255))
    d.rectangle([cx, cy, cx + CW2, cy + 15], fill=col)
    f_k = F(SANS_B, 9)
    d.text((cx + 5, cy + 3), kick, font=f_k, fill=(255, 255, 255))
    ty = cy + 19
    f_t, tlines = fit_lines(d, title, [13, 12], SANS_B, CW2 - 10, 2)
    for ln in tlines:
        d.text((cx + 5, ty), ln, font=f_t, fill=INK)
        ty += 15
    f_b, blines = fit_lines(d, body, [11, 10], SANS, CW2 - 10, 3)
    for ln in blines:
        d.text((cx + 5, ty), ln, font=f_b, fill=(40, 40, 40))
        ty += 13
    sy = cy + CH2 - 14
    f_s = F(SANS, 9)
    d.text((cx + 5, sy), src, font=f_s, fill=GREY)
    draw_chip(cx + CW2 - 66, sy - 1, chip, chip_col)

# ---------- map + ALSO ----------
MY = 592
f_sec = F(SANS_B, 15)
d.text((24, MY), "THE WORLD — WHERE IT HAPPENED", font=f_sec, fill=RED)
d.text((612, MY), "ALSO ON MONDAY — 18 MORE STORIES", font=f_sec, fill=RED)

MX0, MY0, MW, MH = 24, 614, 576, 178
SEA = (214, 231, 243)
LAND = (233, 220, 195)
d.rectangle([MX0, MY0, MX0 + MW, MY0 + MH], fill=SEA, outline=(170, 190, 205))
# graticule
for lon in range(-150, 181, 30):
    gx = MX0 + (lon + 180) / 360 * MW
    d.line([gx, MY0, gx, MY0 + MH], fill=(200, 218, 232), width=1)
for lat in range(-60, 79, 30):
    gy = MY0 + (78 - lat) / 136 * MH
    d.line([MX0, gy, MX0 + MW, gy], fill=(200, 218, 232), width=1)

def ll(lon, lat):
    return (MX0 + (lon + 180) / 360 * MW, MY0 + (78 - lat) / 136 * MH)

CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-80, 73), (-60, 60), (-55, 47),
           (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
           (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    "GL": [(-55, 60), (-45, 60), (-40, 70), (-30, 76), (-55, 76), (-60, 70)],
    "SA": [(-80, 10), (-60, 5), (-50, 0), (-40, -5), (-35, -8), (-40, -20), (-48, -28),
           (-58, -35), (-65, -45), (-70, -52), (-73, -40), (-73, -25), (-77, -12), (-80, -3)],
    "AF": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12),
           (51, 11), (48, 0), (40, -10), (35, -20), (32, -29), (25, -34), (18, -32),
           (12, -18), (9, 4), (-8, 5), (-15, 11)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 57), (10, 59),
           (18, 56), (21, 55), (24, 58), (28, 60), (30, 70), (25, 71), (18, 69), (12, 65),
           (5, 60), (-5, 58), (-10, 54), (-10, 43), (-9, 38)],
    "AS": [(30, 70), (40, 68), (55, 69), (70, 72), (90, 75), (110, 74), (130, 72), (150, 70),
           (170, 66), (178, 65), (170, 60), (162, 56), (158, 52), (142, 50), (140, 40),
           (130, 35), (127, 33), (120, 25), (110, 20), (105, 10), (100, 8), (97, 15),
           (92, 20), (88, 22), (80, 13), (77, 8), (72, 20), (66, 25), (60, 25), (57, 26),
           (52, 28), (48, 30), (44, 29), (40, 31), (36, 36), (30, 36), (28, 41), (30, 45),
           (30, 55), (32, 60), (30, 65)],
    "AU": [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35), (140, -38),
           (145, -38), (150, -37), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
           (136, -12), (132, -11), (126, -14), (122, -17), (118, -20)],
}
for poly in CONTINENTS.values():
    d.polygon([ll(lo, la) for lo, la in poly], fill=LAND, outline=(190, 175, 140))

# pins: (num, lon, lat, dx, dy, status)  status: R reported, C claim, O ongoing
PINS = [
    (1, 127, 37.5, 0, 0, "R"),
    (2, -59.6, 13.1, 0, 0, "R"),
    (3, -140, -30, 0, 0, "R"),
    (4, -74, 40.7, -11, 0, "R"),
    (5, -122.4, 37.8, 0, 0, "R"),
    (6, 19, 52, 2, -15, "C"),
    (7, 37.6, 55.7, 14, -12, "C"),
    (8, 2.35, 48.85, -15, 13, "R"),
    (9, -2.24, 53.48, -17, -13, "R"),
    (10, 30.5, 50.45, -10, 12, "C"),
    (11, 30.7, 36.9, -24, -20, "R"),
    (12, 20.07, 32.1, -12, 8, "C"),
    (13, 35.2, 31.77, -18, -14, "O"),
    (14, 34.45, 31.5, 18, -12, "R"),
    (15, 35.2, 32.0, 18, 12, "R"),
    (16, 51.4, 35.7, 12, -12, "R"),
    (17, 35.5, 33.85, -6, 18, "R"),
    (18, 50.55, 26.2, 9, 11, "R"),
    (19, 32.5, 15.6, -14, 12, "R"),
    (20, 29.5, 1.5, 12, 8, "R"),
    (21, 90.4, 23.8, 0, 0, "R"),
    (22, 127, 37.5, -17, -12, "R"),
    (23, 127, 37.5, 17, -11, "R"),
    (24, 116.4, 39.9, -16, 10, "R"),
    (25, 127, 37.5, 0, 15, "R"),
    (26, -77, 38.9, -18, -12, "R"),
    (27, -77, 38.9, 11, -11, "R"),
    (28, -77, 38.9, 0, 13, "R"),
    (29, -74, 40.7, 11, 0, "R"),
    (30, -104.9, 39.7, 0, 0, "R"),
    (31, -97.2, 26, 0, 0, "R"),
]
PCOL = {"R": RED, "C": AMBER, "O": BLUE}
f_pn = F(SANS_B, 8)
for num, lon, lat, dx, dy, st in PINS:
    px, py = ll(lon, lat)
    px += dx
    py += dy
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=PCOL[st], outline=(255, 255, 255), width=1)
    t = str(num)
    tw = d.textlength(t, font=f_pn)
    d.text((px - tw / 2, py - 5), t, font=f_pn, fill=(255, 255, 255))
f_comp = F(SANS_B, 10)
d.text((MX0 + 4, MY0 + MH - 14), "N ↑", font=f_comp, fill=INK)

# ALSO list, two columns
also = [
    ("MIDDLE EAST", (112, 48, 160), [
        "14 Gaza: two killed in strike",
        "15 West Bank: settler attacks",
        "16 Iran war: no deal in sight",
        "17 Lebanon seizes 264 kg explosives",
        "18 Bahrain: strike hits plant, 2 hurt",
    ]),
    ("AFRICA", (191, 143, 0), [
        "19 Sudan: drones downed over Khartoum",
        "20 DRC: fighting traps Ebola teams",
    ]),
    ("ASIA-PACIFIC", (46, 125, 50), [
        "21 Bangladesh: Hasina jailed",
        "22 Seoul minister quits over AI chaos",
        "23 SK Telecom -7.3% as hype cools",
        "24 China eases margin rules",
        "25 Seoul readies 10T-won fund",
    ]),
    ("NORTH AMERICA", (31, 78, 121), [
        "26 Bessent demands Nvidia answers",
        "27 FBI probes police database hack",
        "28 Trump: Iran strikes may resume",
        "29 US futures jump 3% holiday week",
        "30 Tom Jackson dies at 75",
        "31 States sue SpaceX over AI claims",
    ]),
]
f_ah = F(SANS_B, 11)
f_ai = F(SANS, 10)
col_x = [612, 806]
col_w = 188
# left column: MIDDLE EAST + AFRICA ; right column: ASIA-PACIFIC + NORTH AMERICA
col_groups = [[also[0], also[1]], [also[2], also[3]]]
for ci, groups in enumerate(col_groups):
    cx = col_x[ci]
    cy = MY0
    for name, col, items in groups:
        d.text((cx, cy), name, font=f_ah, fill=col)
        cy += 15
        for it in items:
            lines = wrap(d, it, f_ai, col_w)
            for ln in lines:
                d.text((cx, cy), ln, font=f_ai, fill=INK)
                cy += 12
        cy += 4

# ---------- DATE CHECK ----------
DY = 802
d.rectangle([24, DY, 1000, DY + 96], outline=RED, width=2, fill=(255, 244, 244))
f_dc = F(SANS_B, 14)
d.text((34, DY + 7), "DATE CHECK", font=f_dc, fill=RED)
f_dc2 = F(SANS, 12)
d.text((34 + d.textlength("DATE CHECK  ", font=f_dc), DY + 8),
       "Every story above happened or was first reported on Monday 23 November 2026.",
       font=f_dc2, fill=INK)
f_wr = F(SANS_B, 10)
wr = "WIRES READ UP TO 23:00 UTC"
d.text((1000 - 10 - d.textlength(wr, font=f_wr), DY + 9), wr, font=f_wr, fill=RED)
f_dcb = F(SANS, 12)
lo = "LEFT OUT (not 23 Nov):  Democrats reach 258 (22 Nov)  ·  Sparta II fire (22 Nov)  ·  El Chapo Isidro captured (22 Nov)  ·  EU–Indonesia pact (21 Nov)  ·  Nigeria boat (21 Nov)  ·  ICJ Myanmar ruling (19 Nov)."
for i, ln in enumerate(wrap(d, lo, f_dcb, 946)):
    d.text((34, DY + 32 + i * 15), ln, font=f_dcb, fill=INK)
ny = "NOT YET:  Dymer search continues (14 missing)  ·  4 House races uncalled  ·  COP32 venue not set  ·  WHO evacuating trapped Ebola staff."
for i, ln in enumerate(wrap(d, ny, f_dcb, 946)):
    d.text((34, DY + 64 + i * 15), ln, font=f_dcb, fill=INK)

# ---------- footer ----------
FY = 912
f_f = F(SANS, 10)
d.text((24, FY), "SOURCES: AP · Reuters · Bloomberg · AFP · CNN · ESPN · UN News · WHO · Kyiv · Lowy Institute · Korea JoongAng · Morningstar",
       font=f_f, fill=GREY)
d.text((24, FY + 15),
       "CONFIRMED = 2+ outlets · REPORTED = carried by a wire · CLAIM = one side alleges · ONGOING = developing.  Red pin = reported · Amber pin = claim (unverified).",
       font=f_f, fill=GREY)
f_b = F(SANS_B, 11)
d.text((24, FY + 34), "THE WORLD TODAY · 23 NOV 2026", font=f_b, fill=INK)
f_i = F(SANS, 10)
rt = "Scenes are drawn illustrations, not photographs."
d.text((1000 - d.textlength(rt, font=f_i), FY + 35), rt, font=f_i, fill=GREY)

img.save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
