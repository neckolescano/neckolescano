"""Generates the pixel-art SVGs used in the profile README.

Run:  python tools/generate.py   (writes into assets/)
Everything is drawn from rectangles, so the art stays crisp at any size
and needs no fonts or external files.
"""
import math
import os
import random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# ---------------------------------------------------------------- palette
# Taken from the kuwaGO app icon and banner.
C = {
    "a": "#2b1a10",  # ink (outline)
    "b": "#8b5a34",  # owl brown
    "c": "#fff4e0",  # cream highlight
    "d": "#e8b84b",  # gold
    "e": "#5a3a22",  # dark bark
    "f": "#f6dfc0",  # owl belly
    "g": "#b8862a",  # dark gold
    "h": "#b97a45",  # wood
    "i": "#7cb350",  # leaf
    "j": "#3f7a2e",  # deep green
    "k": "#8fb8de",  # sky blue
    "l": "#b5523b",  # brick
    "m": "#c9b99a",  # stone
    "n": "#2f3e5c",  # night
    "p": "#e98b8b",  # petal pink
    "w": "#fffaf0",  # cloud
    "s": "#efe4cc",  # cloud shade
    "t": "#d39a62",  # wood highlight
}
PAPER = "#fbf3e2"
MINT = "#dcefc8"

# ---------------------------------------------------------------- 5x7 font
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    " ": ["...", "...", "...", "...", "...", "...", "..."],
    ".": [".", ".", ".", ".", ".", ".", "#"],
    ",": ["..", "..", "..", "..", "..", ".#", "#."],
    ":": [".", ".", "#", ".", ".", "#", "."],
    "'": ["#", "#", ".", ".", ".", ".", "."],
    "!": ["#", "#", "#", "#", "#", ".", "#"],
    "-": ["...", "...", "...", "###", "...", "...", "..."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "/": ["....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."],
    "#": [".#.#.", "#####", ".#.#.", ".#.#.", ".#.#.", "#####", ".#.#."],
    "&": [".#...", "#.#..", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
    "?": [".###.", "#...#", "...#.", "..#..", "..#..", ".....", "..#.."],
    ">": ["#...", ".#..", "..#.", "...#", "..#.", ".#..", "#..."],
    "*": [".....", "..#..", "#.#.#", ".###.", "#.#.#", "..#..", "....."],
    "@": [".###.", "#...#", "#.###", "#.#.#", "#.##.", "#....", ".###."],
    "(": ["..#", ".#.", "#..", "#..", "#..", ".#.", "..#"],
    ")": ["#..", ".#.", "..#", "..#", "..#", ".#.", "#.."],
    "|": ["#", "#", "#", "#", "#", "#", "#"],
}


def text_width(text, s):
    w = 0
    for ch in text.upper():
        w += (len(FONT[ch][0]) + 1) * s
    return w - s if text else 0


def merge_rects(cells, s, x0, y0, color):
    """cells: set of (cx, cy). Emits one rect per horizontal run."""
    out = []
    rows = {}
    for cx, cy in cells:
        rows.setdefault(cy, []).append(cx)
    for cy, xs in rows.items():
        xs.sort()
        start = prev = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == prev + 1:
                prev = x
                continue
            out.append(
                f'<rect x="{x0 + start * s}" y="{y0 + cy * s}" width="{(prev - start + 1) * s}" height="{s}" fill="{color}"/>'
            )
            if x is not None:
                start = prev = x
    return "".join(out)


def text(t, x, y, s, color, shadow=None):
    cells = set()
    cx = 0
    for ch in t.upper():
        g = FONT[ch]
        for ry, row in enumerate(g):
            for rx, v in enumerate(row):
                if v == "#":
                    cells.add((cx + rx, ry))
        cx += len(g[0]) + 1
    out = ""
    if shadow:
        out += merge_rects(cells, s, x + s, y + s, shadow)
    out += merge_rects(cells, s, x, y, color)
    return out


def sprite(grid, x, y, s, pal=None):
    pal = pal or C
    by_color = {}
    for ry, row in enumerate(grid):
        for rx, v in enumerate(row):
            if v != ".":
                by_color.setdefault(pal[v], set()).add((rx, ry))
    return "".join(merge_rects(cells, s, x, y, col) for col, cells in by_color.items())


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>'


def panel(x, y, w, h, fill, border=C["a"], b=5):
    """Box with a pixel border and notched corners."""
    return (
        rect(x + b, y, w - 2 * b, b, border)
        + rect(x + b, y + h - b, w - 2 * b, b, border)
        + rect(x, y + b, b, h - 2 * b, border)
        + rect(x + w - b, y + b, b, h - 2 * b, border)
        + rect(x + b, y + b, w - 2 * b, h - 2 * b, fill)
    )


def svg(w, h, body, style="", title=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'shape-rendering="crispEdges" role="img" aria-label="{title}">'
        f"<title>{title}</title>"
        f"<style>{style}</style>{body}</svg>"
    )


def save(name, content):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {name:22s} {len(content) // 1024} KB")


# ---------------------------------------------------------------- sprites
OWL = [
    ".........a..............a.........",
    ".........aa............aa.........",
    ".........aba..........aba.........",
    ".........abbaaaaaaaaaabba.........",
    ".........abbbbbbbbbbbbbba.........",
    "........abbbbbbbbbbbbbbbba........",
    "........abbaabbbbbbbbaabba........",
    ".......abaccccabbbbaccccaba.......",
    ".......abacaacabbbbacaacaba.......",
    ".......abacaacabddbacaacaba.......",
    ".......abaccccabddbaccccaba.......",
    ".......abbbaabbbddbbbaabbba.......",
    ".......aebbbffffggffffbbbea.......",
    "......aeebbffhffhhffhffbbeea......",
    "......aeebfffhffffffhfffbeea......",
    "......aeebffhffhffhffhffbeea......",
    "......aeebbffffffffffffbbeea......",
    ".......aebbbffhffffhffbbbea.......",
    ".......aeebbbffffffffbbbeea.......",
    "........aeebbbbbbbbbbbbeea........",
    ".........aaaaddaaaaddaaaa.........",
    ".....eeeeeeeeddeeeeddeeeeeeij.....",
    ".....hhhhhhhhhhhhhhhhhhhhijji.....",
    ".....aaaaaaaaaaaaaaaaaaaa.ij......",
]
# Closed eyes, drawn over the open ones for the blink.
def _blink_rows():
    rows = []
    for i, row in enumerate(OWL[7:11]):
        r = ["."] * len(row)
        for lo in (10, 20):
            for x in range(lo, lo + 4):
                r[x] = "a" if i == 2 else "b"
        rows.append("".join(r))
    return rows


OWL_BLINK = _blink_rows()

CLOUD = [
    "......wwww..........",
    "....wwwwwwww..www...",
    "..wwwwwwwwwwwwwwwww.",
    ".wwwwwwwwwwwwwwwwwww",
    "wwwwwwwwwwwwwwwwwwww",
    ".sssssssssssssssss..",
]

SPARK = ["..d..", ".ddd.", "ddcdd", ".ddd.", "..d.."]

SPROUT = [
    "...jj..",
    "..jiij.",
    "jj.jij.",
    "jij.j..",
    ".jjjj..",
    "...j...",
    "...j...",
]

FLOWER_P = [".p.", "pdp", ".p.", ".j."]
FLOWER_W = [".c.", "cdc", ".c.", ".j."]

ICONS = {
    "sprout": [
        "............",
        ".......jj...",
        "......jiij..",
        "..jj..jiij..",
        ".jiij.jjj...",
        ".jiiij.j....",
        "..jjjjjj....",
        "......j.....",
        "..aaaaaaaa..",
        "..ahhhhhha..",
        "...ahhhha...",
        "...aaaaaa...",
    ],
    "gamepad": [
        "............",
        "............",
        "..aaaaaaaa..",
        ".annnnnnnna.",
        "annannnnlnna",
        "anaaanndnlna",
        "annannnnlnna",
        "annnnnnnnnna",
        "annnaaaannna",
        ".aaa....aaa.",
        "............",
        "............",
    ],
    "monitor": [
        "............",
        "aaaaaaaaaaaa",
        "annnnnnnnnna",
        "ankkknnndnna",
        "anknnnnnnnna",
        "annnnniinnna",
        "annnniiiinna",
        "aaaaaaaaaaaa",
        ".....aa.....",
        "....abba....",
        "..aaaaaaaa..",
        "............",
    ],
    "film": [
        "............",
        "aaaaaaaaaaaa",
        "acaacaacaaca",
        "aaaaaaaaaaaa",
        "allllllllll.",
        "allllllllll.",
        "alllllddllla",
        "allllllllll.",
        "allllllllll.",
        "aaaaaaaaaaaa",
        "acaacaacaaca",
        "aaaaaaaaaaaa",
    ],
    "wifi": [
        "............",
        "...jjjjjj...",
        ".jj......jj.",
        "j...jjjj...j",
        "...j....j...",
        "..j..jj..j..",
        ".....jj.....",
        "............",
        ".....jj.....",
        ".....jj..l.l",
        ".........ll.",
        ".........l.l",
    ],
    "coin": [
        "...aaaaaa...",
        ".aaddddddaa.",
        ".adddddddda.",
        "adaaaaaadgda",
        "addaddddagda",
        "adaaaaaadgda",
        "addaddddddga",
        "addaddddddga",
        ".adddddddga.",
        ".aaddddggaa.",
        "...aaaaaa...",
        "............",
    ],
}


# ---------------------------------------------------------------- banner
def banner():
    W, H = 1000, 360
    rnd = random.Random(7)
    body = ""

    # Sky: stepped bands with a dithered seam between each pair.
    top, bot = (0xF8, 0xF0, 0xDE), (0xDC, 0xEF, 0xC8)
    bands = 7
    bh = 45
    cols = []
    for i in range(bands):
        t = i / (bands - 1)
        cols.append("#%02x%02x%02x" % tuple(round(a + (b - a) * t) for a, b in zip(top, bot)))
    for i, col in enumerate(cols):
        body += rect(0, i * bh, W, bh if i < bands - 1 else H - i * bh, col)
    for i in range(1, bands):
        y = i * bh - 5
        cells = {(cx, 0) for cx in range(0, W // 5) if cx % 2 == 0}
        cells |= {(cx, -1) for cx in range(0, W // 5) if cx % 4 == 1}
        body += merge_rects(cells, 5, 0, y, cols[i])

    # Drifting clouds.
    for i, (cy, s, dur, delay) in enumerate([(40, 5, 70, -10), (95, 4, 90, -55), (150, 3, 110, -30), (20, 3, 120, -85)]):
        body += f'<g class="cloud" style="animation-duration:{dur}s;animation-delay:{delay}s">{sprite(CLOUD, 0, cy, s)}</g>'

    # Hills.
    def hill(base, amp1, f1, amp2, f2, ph, color, step=10):
        out = ""
        for x in range(0, W, step):
            h = base + amp1 * math.sin(x / f1 + ph) + amp2 * math.sin(x / f2)
            h = int(h // 5 * 5)
            out += rect(x, h, step, H - h, color)
        return out

    body += hill(262, 18, 95, 8, 37, 0.5, "#bcdb9c")
    body += hill(292, 14, 70, 6, 29, 2.0, "#93c56a")
    # Ground with a ragged grass edge.
    gy = 318
    body += rect(0, gy, W, H - gy, "#5f9b3c")
    edge = {(cx, 0) for cx in range(W // 5) if rnd.random() < 0.55}
    body += merge_rects(edge, 5, 0, gy - 5, "#5f9b3c")
    body += rect(0, 345, W, 15, C["j"])
    for _ in range(26):
        fx = rnd.randrange(10, 900)
        fy = rnd.choice([300, 312, 322, 330])
        body += sprite(rnd.choice([FLOWER_P, FLOWER_W]), fx, fy, 3)

    # Tree on the right: trunk, canopy and the branch the owl sits on.
    body += rect(935, 0, 65, H, C["e"])
    body += rect(950, 0, 30, H, C["b"])
    for y in range(10, H, 40):
        body += rect(958, y, 5, 20, C["e"])
    canopy = [(860, -30, 90), (930, -20, 80), (800, -50, 70), (980, 40, 60)]
    for cx, cy, r in canopy:
        for yy in range(cy - r, cy + r, 10):
            half = int(math.sqrt(max(0, r * r - (yy - cy) ** 2)) // 10 * 10)
            body += rect(cx - half, yy, half * 2, 10, C["j"])
    for cx, cy, r in canopy:
        for yy in range(cy - r, cy + r // 3, 10):
            half = int(math.sqrt(max(0, (r - 18) ** 2 - (yy - cy + 6) ** 2)) // 10 * 10)
            if half:
                body += rect(cx - half - 6, yy, half * 2, 10, C["i"])

    s = 5
    ox, oy = 735, 150
    body += sprite(OWL, ox, oy, s)
    by = oy + 21 * s
    body += rect(ox + 27 * s, by, 940 - (ox + 27 * s), s, C["e"])
    body += rect(ox + 25 * s, by + s, 940 - (ox + 25 * s), s, C["h"])
    body += rect(ox + 25 * s, by + 2 * s, 940 - (ox + 25 * s), s, C["a"])
    body += f'<g class="blink">{sprite(OWL_BLINK, ox, oy + 7 * s, s)}</g>'

    # Sparkles.
    for i, (sx, sy) in enumerate([(640, 60), (700, 120), (590, 175), (880, 115), (520, 40)]):
        body += f'<g class="spark" style="animation-delay:{i * 0.7}s">{sprite(SPARK, sx, sy, 3)}</g>'

    # Text.
    x = 56
    body += text("HELLO, I'M", x, 62, 3, C["h"])
    body += text("NICHO LESCANO", x, 100, 7, C["a"], shadow=C["i"])
    body += text("UI/UX DESIGNER + DEVELOPER", x, 177, 3, C["j"])
    body += text("I DESIGN COZY, CLEAR, PLAYFUL APPS", x, 215, 2, C["e"])
    cx = x + text_width("UI/UX DESIGNER + DEVELOPER", 3) + 8
    body += f'<rect class="cursor" x="{cx}" y="177" width="12" height="21" fill="{C["j"]}"/>'

    style = (
        ".cloud{animation:drift 80s linear infinite}"
        "@keyframes drift{from{transform:translateX(-120px)}to{transform:translateX(1000px)}}"
        ".blink{opacity:0;animation:blink 5s steps(1) infinite}"
        "@keyframes blink{0%,90%{opacity:0}92%,96%{opacity:1}98%{opacity:0}}"
        ".spark{animation:tw 2.8s ease-in-out infinite}"
        "@keyframes tw{0%,100%{opacity:.15}50%{opacity:1}}"
        ".cursor{animation:cur 1s steps(1) infinite}"
        "@keyframes cur{50%{opacity:0}}"
    )
    save("banner.svg", svg(W, H, body, style, "Nicho Lescano, UI/UX designer and developer"))


# ---------------------------------------------------------------- buttons
def button(name, label, color, fg=C["a"]):
    s = 2
    tw = text_width(label, s)
    W, H = tw + 44, 46
    body = panel(0, 4, W, H - 4, C["a"])  # shadow
    body += panel(0, 0, W, H - 6, color)
    body += rect(5, 5, W - 10, 3, "#ffffff55")
    body += text(label, (W - tw) // 2, 13, s, fg)
    save(name, svg(W, H, body, "", label))


# ---------------------------------------------------------------- plaque
def plaque(name, label):
    s = 3
    tw = text_width(label, s)
    W, H = tw + 110, 62
    body = ""
    # Hanging ropes.
    body += rect(30, 0, 5, 10, C["e"]) + rect(W - 35, 0, 5, 10, C["e"])
    body += panel(0, 8, W, H - 8, C["h"])
    body += rect(5, 13, W - 10, 4, C["t"])
    body += rect(5, H - 9, W - 10, 4, C["b"])
    for nx in (14, W - 19):
        body += rect(nx, 28, 5, 5, C["a"])
    body += sprite(SPROUT, 26, 22, 3)
    body += text(label, 62, 26, s, C["c"], shadow=C["e"])
    save(name, svg(W, H, body, "", label))


# ---------------------------------------------------------------- player card
def player_card():
    W, H = 1000, 330
    body = panel(0, 0, W, H, C["a"])
    body += panel(5, 5, W - 10, H - 10, PAPER, C["h"])
    # Title bar, like a game dialog window.
    body += rect(10, 10, W - 20, 40, C["h"])
    body += rect(10, 10, W - 20, 4, C["t"])
    body += rect(10, 50, W - 20, 5, C["a"])
    body += text("PLAYER PROFILE", 26, 23, 2, C["c"], shadow=C["e"])
    for i, col in enumerate([C["i"], C["d"], C["l"]]):
        body += panel(W - 100 + i * 26, 20, 20, 20, col)

    # Portrait.
    px, py = 40, 78
    body += panel(px, py, 210, 190, MINT)
    owl_top = [row[5:29] for row in OWL[:20]]
    body += sprite(owl_top, px + (210 - 24 * 7) // 2, py + 22, 7)
    body += f'<g class="blink">{sprite([r[5:29] for r in OWL_BLINK], px + (210 - 24 * 7) // 2, py + 22 + 7 * 7, 7)}</g>'
    body += panel(px + 25, py + 170, 160, 34, C["d"])
    body += text("NICHO", px + 25 + (160 - text_width("NICHO", 2)) // 2, py + 180, 2, C["a"])

    # Stats.
    x = 290
    body += text("NICHO LESCANO", x, 80, 4, C["a"], shadow=C["i"])
    rows = [
        ("CLASS", "DESIGNER + DEV"),
        ("BASE", "PHILIPPINES"),
        ("QUEST", "COZY, CLEAR UI"),
        ("NOW", "THREE.JS + AI"),
    ]
    for i, (k, v) in enumerate(rows):
        y = 135 + i * 30
        body += text(k, x, y, 2, C["h"])
        body += text(v, x + 84, y, 2, C["a"])

    # Skill bars.
    bx = 640
    body += text("SKILLS", bx, 102, 2, C["j"])
    skills = [("DESIGN", 9), ("MOBILE", 7), ("DESKTOP", 7), ("WEB", 8)]
    for i, (k, v) in enumerate(skills):
        y = 135 + i * 30
        body += text(k, bx, y, 2, C["a"])
        sx = bx + 104
        body += panel(sx, y - 4, 10 * 20 + 10, 22, C["s"])
        for j in range(10):
            if j < v:
                d = round(0.4 + i * 0.25 + j * 0.08, 2)
                body += (
                    f'<g class="seg" style="animation-delay:{d}s">'
                    + rect(sx + 5 + j * 20, y + 1, 18, 12, C["i"])
                    + rect(sx + 5 + j * 20, y + 1, 18, 3, "#b6db8f")
                    + "</g>"
                )

    # Dialog line.
    body += rect(290, 262, 670, 4, C["s"])
    body += text("> SCROLL DOWN TO SEE MY WORK", 290, 284, 2, C["e"])
    body += f'<g class="arrow">{sprite(["aaaaa", ".aaa.", "..a.."], 290 + text_width("> SCROLL DOWN TO SEE MY WORK", 2) + 12, 286, 3)}</g>'

    style = (
        ".blink{opacity:0;animation:blink 6s steps(1) infinite}"
        "@keyframes blink{0%,90%{opacity:0}92%,96%{opacity:1}98%{opacity:0}}"
        ".seg{animation:pop .25s steps(2) backwards}"
        "@keyframes pop{from{opacity:0}}"
        ".arrow{animation:bob 1s steps(2) infinite}"
        "@keyframes bob{50%{transform:translateY(4px)}}"
    )
    save("about.svg", svg(W, H, body, style, "Player profile: Nicho Lescano"))


# ---------------------------------------------------------------- project card
def wrap(t, n):
    words, lines, cur = t.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    lines.append(cur)
    return lines


def card(name, title, kind, desc, tags, icon, accent, button_label="VIEW"):
    # Sized so the README shows it at about 1:1, keeping the 2x text crisp.
    W, H = 360, 276
    body = panel(0, 6, W, H - 6, C["a"])  # drop shadow
    body += panel(0, 0, W, H - 6, PAPER)
    body += rect(5, 5, W - 10, 8, accent)

    body += panel(18, 28, 68, 68, MINT)
    body += sprite(ICONS[icon], 28, 38, 4)

    body += text(title, 100, 36, 3, C["a"])
    body += text(kind, 100, 70, 2, accent)

    for i, line in enumerate(wrap(desc, 26)[:4]):
        body += text(line, 20, 116 + i * 22, 2, C["e"])

    y = 214
    x = 18
    for t in tags:
        tw = text_width(t, 2)
        body += panel(x, y, tw + 20, 30, MINT if accent == C["j"] else C["s"])
        body += text(t, x + 10, y + 8, 2, C["a"])
        x += tw + 26

    # "Go" button.
    bw = 44
    bx = W - bw - 18
    body += panel(bx, y + 4, bw, 32, C["a"])
    body += panel(bx, y - 2, bw, 32, C["d"])
    body += rect(bx + 5, y + 3, bw - 10, 3, "#fff3c4")
    body += sprite(["a...", "aa..", "aaa.", "aaaa", "aaa.", "aa..", "a..."], bx + 16, y + 5, 2)
    save(name, svg(W, H, body, "", f"{title}: {desc.lower()}"))


# ---------------------------------------------------------------- footer
def footer():
    W, H = 1000, 150
    rnd = random.Random(3)
    body = ""
    msg = "THANKS FOR STOPPING BY!"
    tw = text_width(msg, 2)
    sx = 60
    body += rect(sx + 20, 30, 5, 70, C["e"]) + rect(sx + tw + 10, 30, 5, 70, C["e"])
    body += panel(sx, 4, tw + 36, 40, C["h"])
    body += rect(sx + 5, 9, tw + 26, 3, C["t"])
    body += text(msg, sx + 18, 17, 2, C["c"], shadow=C["e"])
    gy = 100
    body += rect(0, gy, W, H - gy, "#5f9b3c")
    edge = {(cx, 0) for cx in range(W // 5) if rnd.random() < 0.55}
    body += merge_rects(edge, 5, 0, gy - 5, "#5f9b3c")
    body += rect(0, 130, W, 20, C["j"])
    for i, x in enumerate(range(40, W, 90)):
        d = round(i * 0.3, 1)
        body += f'<g class="sway" style="animation-delay:{d}s">{sprite(SPROUT, x, gy - 21 - 6, 4)}</g>'
    for _ in range(18):
        body += sprite(rnd.choice([FLOWER_P, FLOWER_W]), rnd.randrange(10, 980), rnd.choice([104, 114]), 3)
    owl_small = [row[5:29] for row in OWL[:21]]
    body += sprite(owl_small, (W - 24 * 3) // 2, gy - 63 + 2, 3)
    style = (
        ".sway{animation:sway 2.4s steps(2) infinite}"
        "@keyframes sway{50%{transform:translateY(-4px)}}"
    )
    save("footer.svg", svg(W, H, body, style, "Thanks for stopping by"))


if __name__ == "__main__":
    print("writing assets:")
    banner()
    player_card()
    footer()
    for f, label in [
        ("plaque-projects.svg", "FEATURED PROJECTS"),
        ("plaque-toolkit.svg", "TOOLKIT"),
        ("plaque-stats.svg", "GITHUB STATS"),
    ]:
        plaque(f, label)
    button("btn-portfolio.svg", "PORTFOLIO", C["d"])
    button("btn-email.svg", "EMAIL ME", C["i"])
    button("btn-kuwago.svg", "PLAY KUWAGO", C["t"])

    card("card-kuwago.svg", "KUWAGO", "MOBILE APP",
         "A COZY PIXEL STUDY GARDEN. FOCUS TO GROW PLANTS, THEN QUIZ YOURSELF WITH AI.",
         ["FLUTTER", "FIREBASE"], "sprout", C["j"])
    card("card-xpera.svg", "XPERA CRM", "DESKTOP APP",
         "A CRM FOR GAMING PC PARTS STORES, WITH ONE PRIVATE DATABASE PER STORE.",
         ["C#", ".NET", "SQL"], "gamepad", C["n"])
    card("card-nichodev.svg", "NICHO.DEV", "PORTFOLIO SITE",
         "MY PORTFOLIO, WITH A 3D ROOM AND A WORKING LAPTOP INSIDE IT.",
         ["JS", "THREE.JS"], "monitor", C["h"])
    card("card-cinematheque.svg", "CINEMATHEQUE", "WEB APP",
         "A CINEMA WEB APP BUILT WITH LARAVEL AND BLADE.",
         ["LARAVEL", "PHP"], "film", C["l"])
    card("card-sagap.svg", "SAGAP", "MOBILE APP",
         "A MOBILE APP THAT MAPS WI-FI DEAD ZONES.",
         ["FLUTTER", "DART"], "wifi", C["j"])
    card("card-payroller.svg", "PAYROLLER", "DESKTOP APP",
         "A PAYROLL SYSTEM: EMPLOYEES, AUTOMATIC PAY AND PAYROLL HISTORY.",
         ["PYTHON", "PYQT6"], "coin", C["g"])
