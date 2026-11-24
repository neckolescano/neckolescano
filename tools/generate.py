"""Generates the SVGs used in the profile README.

Run:  python tools/generate.py   (writes into assets/)
Smooth, rounded layouts with real system-font text, plus small pixel-art
accents (icons, sparkles, cursor, the name) drawn from rectangles.
"""
import math
import os
import random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# ---------------------------------------------------------------- palette
# Pixel-art colours: warm ink, wood, gold and leaf greens.
C = {
    "a": "#2b1a10",  # ink (outline)
    "b": "#8b5a34",  # brown
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
    "<": ["...#", "..#.", ".#..", "#...", ".#..", "..#.", "...#"],
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


def save(name, content):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {name:22s} {len(content) // 1024} KB")


# =====================================================================
# Smooth layer: rounded shapes and real text, with pixel art as accents.
# =====================================================================
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
INK = "#2b2118"
BODY = "#5a4a3a"
MUTED = "#8a7a68"
CARD = "#fffdf8"
LINE = "#e8dfcc"
CREAM = "#fbf6ec"

ACCENTS = {
    "green": ("#4e7a3a", "#e4eeda"),
    "navy": ("#3b4a6b", "#e2e6ef"),
    "clay": ("#b5653e", "#f5e3d8"),
    "brick": ("#a3483a", "#f3deda"),
    "teal": ("#2f7a73", "#dcefec"),
    "gold": ("#a87a1f", "#f6ebcf"),
}


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def stext(t, x, y, size, color, weight=400, anchor="start", spacing=0):
    extra = f' letter-spacing="{spacing}"' if spacing else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="{size}" font-weight="{weight}" '
        f'fill="{color}" text-anchor="{anchor}"{extra}>{esc(t)}</text>'
    )


def est_width(t, size, weight=400):
    """Rough width of sans text, good enough for sizing pills."""
    per = 0.55 if weight < 600 else 0.6
    return len(t) * size * per


def pix(inner):
    return f'<g shape-rendering="crispEdges">{inner}</g>'


def ssvg(w, h, body, style="", title="", defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
        f"<defs>{defs}</defs><style>{style}</style>{body}</svg>"
    )


SHADOW = (
    '<filter id="sh" x="-10%" y="-10%" width="120%" height="140%">'
    '<feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#2b2118" flood-opacity="0.12"/></filter>'
)


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


# ---------------------------------------------------------------- pixel accents
SPARKLE = ["...d...", "...d...", "..ddd..", "ddddddd", "..ddd..", "...d...", "...d..."]
CLOUD = [
    "......wwww..........",
    "....wwwwwwww..www...",
    "..wwwwwwwwwwwwwwwww.",
    ".wwwwwwwwwwwwwwwwwww",
    "wwwwwwwwwwwwwwwwwwww",
    ".sssssssssssssssss..",
]
CURSOR = [
    "a.........",
    "aa........",
    "aca.......",
    "acca......",
    "accca.....",
    "acccca....",
    "accccca...",
    "acccccca..",
    "accccaaaa.",
    "acaaca....",
    "aa..aca...",
    "a....aca..",
    ".....aa...",
]
PIN = ["..lll..", ".lllll.", "lll.lll", "lll.lll", ".lllll.", "..lll..", "...l..."]
PENCIL = [
    "........aa..",
    ".......alla.",
    "......adala.",
    ".....adda...",
    "....adda....",
    "...adda.....",
    "..adda......",
    ".affa.......",
    ".aaa........",
    "aa..........",
]
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


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1000, 360
    defs = (
        '<clipPath id="r"><rect width="1000" height="360" rx="24"/></clipPath>'
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#fbf6ec"/><stop offset="1" stop-color="#e9f1dc"/></linearGradient>'
        '<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5">'
        '<stop offset="0" stop-color="#f3d48a" stop-opacity="0.55"/>'
        '<stop offset="1" stop-color="#f3d48a" stop-opacity="0"/></radialGradient>'
        + SHADOW
    )
    b = '<g clip-path="url(#r)">'
    b += rect(0, 0, W, H, "url(#sky)")
    b += '<circle cx="800" cy="120" r="220" fill="url(#sun)"/>'
    for cy, s, dur, delay in [(36, 4, 90, -20), (110, 3, 120, -70), (60, 3, 140, -110)]:
        b += (
            f'<g class="cloud" style="animation-duration:{dur}s;animation-delay:{delay}s" opacity="0.9">'
            f"{pix(sprite(CLOUD, 0, cy, s))}</g>"
        )
    b += '<path d="M0 290 C 160 250, 300 270, 460 285 S 760 250, 1000 275 V 360 H 0 Z" fill="#d3e4bf"/>'
    b += '<path d="M0 318 C 200 296, 380 322, 560 312 S 860 296, 1000 312 V 360 H 0 Z" fill="#b2cf98"/>'
    b += '<path d="M0 342 C 260 332, 520 348, 1000 336 V 360 H 0 Z" fill="#8db577"/>'
    b += "</g>"

    # Left: intro.
    x = 64
    label = "UI/UX DESIGNER  ·  DEVELOPER"
    lw = est_width(label, 12, 700) + 36
    b += f'<rect x="{x}" y="56" width="{lw:.0f}" height="30" rx="15" fill="#4e7a3a" fill-opacity="0.12"/>'
    b += stext(label, x + 18, 76, 12, "#3f6b2e", 700, spacing=1.6)
    b += pix(text("NICHO LESCANO", x, 110, 7, INK, shadow="#cfe2bb"))
    b += stext("I design calm, clear and playful interfaces,", x, 200, 21, BODY, 500)
    b += stext("then build them for mobile, desktop and the web.", x, 230, 21, BODY, 500)
    b += pix(sprite(PIN, x, 263, 2, {"l": "#b5653e"}))
    b += stext("Based in the Philippines", x + 22, 276, 15, MUTED, 500)

    # Right: a design-tool window with a frame being edited.
    wx, wy, ww, wh = 630, 52, 316, 236
    b += (
        f'<g filter="url(#sh)"><rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="14" '
        f'fill="{CARD}" stroke="{LINE}" stroke-width="1.5"/></g>'
    )
    b += (
        f'<path d="M{wx} {wy + 14} a14 14 0 0 1 14 -14 H{wx + ww - 14} a14 14 0 0 1 14 14 '
        f'V{wy + 34} H{wx} Z" fill="#f4eee2"/>'
    )
    b += f'<line x1="{wx}" y1="{wy + 34}" x2="{wx + ww}" y2="{wy + 34}" stroke="{LINE}" stroke-width="1.5"/>'
    for i, col in enumerate(["#e58f7d", "#e9c46a", "#8db577"]):
        b += f'<circle cx="{wx + 20 + i * 16}" cy="{wy + 17}" r="5" fill="{col}"/>'
    b += stext("home-screen", wx + ww / 2, wy + 22, 12, MUTED, 600, anchor="middle")
    # Mock app card inside the window.
    cx, cy = wx + 24, wy + 52
    b += f'<rect x="{cx}" y="{cy}" width="190" height="166" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="1.5"/>'
    b += f'<rect x="{cx + 12}" y="{cy + 12}" width="166" height="62" rx="8" fill="#e4eeda"/>'
    b += pix(
        rect(cx + 12, cy + 56, 166, 18, "#b2cf98")
        + rect(cx + 30, cy + 50, 50, 6, "#b2cf98")
        + rect(cx + 100, cy + 46, 46, 10, "#b2cf98")
        + sprite(SPARKLE, cx + 140, cy + 20, 2)
    )
    b += f'<rect x="{cx + 12}" y="{cy + 86}" width="120" height="9" rx="4.5" fill="#d9cfbc"/>'
    b += f'<rect x="{cx + 12}" y="{cy + 102}" width="86" height="9" rx="4.5" fill="#ebe3d3"/>'
    bx, by, bw, bh = cx + 12, cy + 124, 96, 26
    b += f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="13" fill="#e2b04a"/>'
    b += stext("Get started", bx + bw / 2, by + 17, 11, INK, 700, anchor="middle")
    sel = "#4c8bf5"
    b += f'<g class="sel"><rect x="{bx - 5}" y="{by - 5}" width="{bw + 10}" height="{bh + 10}" fill="none" stroke="{sel}" stroke-width="1.5"/>'
    for hx, hy in [(bx - 5, by - 5), (bx + bw + 5, by - 5), (bx - 5, by + bh + 5), (bx + bw + 5, by + bh + 5)]:
        b += f'<rect x="{hx - 3.5}" y="{hy - 3.5}" width="7" height="7" fill="#fff" stroke="{sel}" stroke-width="1.5"/>'
    b += "</g>"
    b += f'<rect x="{bx + bw + 14}" y="{by + 4}" width="52" height="18" rx="4" fill="{sel}"/>'
    b += stext("96 × 26", bx + bw + 40, by + 17, 10, "#ffffff", 600, anchor="middle")
    # Side panel: colour styles.
    px = wx + 236
    b += stext("Colors", px, wy + 64, 11, MUTED, 600)
    for i, col in enumerate(["#2b2118", "#4e7a3a", "#8db577", "#e2b04a", "#b5653e"]):
        b += f'<rect x="{px}" y="{wy + 76 + i * 28}" width="56" height="20" rx="6" fill="{col}"/>'
    # Pixel cursor and sparkles.
    b += f'<g class="cur">{pix(sprite(CURSOR, bx + bw + 2, by + bh + 2, 2, {"a": INK, "c": "#ffffff"}))}</g>'
    for i, (sx, sy) in enumerate([(590, 70), (580, 236), (960, 318), (530, 36)]):
        b += f'<g class="tw" style="animation-delay:{i * 0.8}s">{pix(sprite(SPARKLE, sx, sy, 2))}</g>'

    style = (
        ".cloud{animation:drift 100s linear infinite}"
        "@keyframes drift{from{transform:translateX(-120px)}to{transform:translateX(1000px)}}"
        ".tw{animation:tw 3s ease-in-out infinite}"
        "@keyframes tw{0%,100%{opacity:.2}50%{opacity:1}}"
        ".cur{animation:cur 4s ease-in-out infinite}"
        "@keyframes cur{0%,100%{transform:translate(0,0)}50%{transform:translate(-6px,-4px)}}"
        ".sel{animation:sel 4s ease-in-out infinite}"
        "@keyframes sel{0%,100%{opacity:1}50%{opacity:.55}}"
    )
    save("hero.svg", ssvg(W, H, b, style, "Nicho Lescano, UI/UX designer and developer, based in the Philippines", defs))


# ---------------------------------------------------------------- buttons
def pill_button(name, label, fill, fg, stroke=None):
    size = 15
    tw = est_width(label, size, 700)
    W, H = int(tw + 70), 48
    st = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ""
    b = f'<g filter="url(#sh)"><rect x="6" y="3" width="{W - 12}" height="36" rx="18" fill="{fill}"{st}/></g>'
    b += stext(label, 26, 26, size, fg, 700)
    ax = W - 34
    b += (
        f'<path d="M{ax} 21 h10 m-4 -4 l4 4 l-4 4" stroke="{fg}" stroke-width="2" fill="none" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
    )
    save(name, ssvg(W, H, b, "", label, SHADOW))


# ---------------------------------------------------------------- section heading
def heading(name, label):
    s = 3
    tw = text_width(label, s)
    W, H = tw + 96, 56
    b = f'<rect x="1" y="5" width="{W - 2}" height="46" rx="23" fill="{CARD}" stroke="{LINE}" stroke-width="1.5"/>'
    b += pix(sprite(SPARKLE, 24, 18, 3) + text(label, 62, 18, s, INK))
    save(name, ssvg(W, H, b, "", label.title()))


# ---------------------------------------------------------------- about
def about():
    W, H = 1000, 320
    b = (
        f'<g filter="url(#sh)"><rect x="8" y="4" width="{W - 16}" height="{H - 20}" rx="20" '
        f'fill="{CARD}" stroke="{LINE}" stroke-width="1.5"/></g>'
    )
    x = 52
    b += stext("ABOUT ME", x, 58, 12, "#4e7a3a", 700, spacing=1.6)
    b += stext("Designer first, developer second.", x, 96, 27, INK, 700)
    para = [
        "I'm an IT student from the Philippines who likes",
        "turning ideas into interfaces that feel calm, clear",
        "and a little playful. I take projects from the first",
        "Figma frame all the way to a working app.",
    ]
    for i, line in enumerate(para):
        b += stext(line, x, 138 + i * 27, 17, BODY)
    b += pix(sprite(SPARKLE, x, 256, 2))
    b += stext("Always learning, always sketching", x + 24, 268, 15, MUTED, 600)

    rows = [
        ("Design", "Figma, Illustrator, prototyping", "pencil", "clay"),
        ("Build", "Flutter, .NET, Laravel, JavaScript", "code", "green"),
        ("Exploring", "Three.js and AI features", "spark", "gold"),
    ]
    rx = 560
    for i, (title, sub, icon, acc) in enumerate(rows):
        y = 40 + i * 80
        fg, tint = ACCENTS[acc]
        b += f'<rect x="{rx}" y="{y}" width="392" height="66" rx="14" fill="{CREAM}" stroke="{LINE}" stroke-width="1.5"/>'
        b += f'<rect x="{rx + 12}" y="{y + 11}" width="44" height="44" rx="11" fill="{tint}"/>'
        if icon == "pencil":
            b += pix(sprite(PENCIL, rx + 22, y + 23, 2, C))
        elif icon == "code":
            b += pix(text("</>", rx + 34 - text_width("</>", 2) // 2, y + 26, 2, fg))
        else:
            b += pix(sprite(SPARKLE, rx + 23, y + 22, 3))
        b += stext(title, rx + 72, y + 29, 17, INK, 700)
        b += stext(sub, rx + 72, y + 50, 14, MUTED, 500)
    save("about.svg", ssvg(W, H, b, "", "About me: designer first, developer second", SHADOW))


# ---------------------------------------------------------------- project card
def card(name, title, kind, desc, tags, icon, acc):
    W, H = 480, 250
    fg, tint = ACCENTS[acc]
    b = (
        f'<g filter="url(#sh)"><rect x="8" y="4" width="{W - 16}" height="{H - 20}" rx="18" '
        f'fill="{CARD}" stroke="{LINE}" stroke-width="1.5"/></g>'
    )
    b += f'<rect x="32" y="28" width="60" height="60" rx="14" fill="{tint}"/>'
    b += pix(sprite(ICONS[icon], 38, 34, 4))
    b += stext(title, 108, 56, 22, INK, 700)
    b += stext(kind.upper(), 108, 79, 11, fg, 700, spacing=1.4)
    for i, line in enumerate(wrap(desc, 50)[:3]):
        b += stext(line, 32, 124 + i * 23, 15.5, BODY)
    x = 32
    for t in tags:
        tw = est_width(t, 12, 700) + 22
        b += f'<rect x="{x}" y="186" width="{tw:.0f}" height="26" rx="13" fill="{tint}"/>'
        b += stext(t, x + tw / 2, 203, 12, fg, 700, anchor="middle")
        x += tw + 8
    cx, cy = W - 54, 199
    b += f'<circle cx="{cx}" cy="{cy}" r="18" fill="{INK}"/>'
    b += (
        f'<path d="M{cx - 6} {cy} h12 m-5 -5 l5 5 l-5 5" stroke="#fff" stroke-width="2" fill="none" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
    )
    save(name, ssvg(W, H, b, "", f"{title}: {desc}", SHADOW))


# ---------------------------------------------------------------- footer
def footer():
    W, H = 1000, 130
    defs = '<clipPath id="r"><rect width="1000" height="130" rx="24"/></clipPath>'
    b = '<g clip-path="url(#r)">'
    b += '<path d="M0 40 C 200 10, 380 40, 560 28 S 860 10, 1000 30 V 130 H 0 Z" fill="#b2cf98"/>'
    b += '<path d="M0 62 C 240 46, 520 70, 1000 52 V 130 H 0 Z" fill="#4e7a3a"/>'
    b += "</g>"
    b += stext("Thanks for stopping by. Let's make something nice together.", W / 2, 104, 18, "#fbf6ec", 600, anchor="middle")
    for i, (sx, sy) in enumerate([(150, 70), (840, 74), (300, 30), (700, 22)]):
        b += f'<g class="tw" style="animation-delay:{i * 0.7}s">{pix(sprite(SPARKLE, sx, sy, 2))}</g>'
    style = ".tw{animation:tw 3s ease-in-out infinite}@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}"
    save("footer.svg", ssvg(W, H, b, style, "Thanks for stopping by", defs))


if __name__ == "__main__":
    if os.path.isdir(OUT):
        for f in os.listdir(OUT):
            if f.endswith(".svg"):
                os.remove(os.path.join(OUT, f))
    print("writing assets:")
    hero()
    about()
    footer()
    pill_button("btn-portfolio.svg", "View portfolio", INK, "#fbf6ec")
    pill_button("btn-email.svg", "Email me", CARD, INK, stroke=LINE)
    heading("h-projects.svg", "FEATURED PROJECTS")
    heading("h-toolkit.svg", "TOOLKIT")
    heading("h-stats.svg", "GITHUB STATS")

    card("card-kuwago.svg", "kuwaGO", "Mobile app",
         "A cozy pixel-art study garden. Focus to grow plants, then quiz yourself with AI made from your notes.",
         ["Flutter", "Firebase", "Gemini"], "sprout", "green")
    card("card-xpera.svg", "xpera CRM", "Desktop app",
         "A CRM for gaming PC parts stores: customers, sales and payments, with one private database per store.",
         ["C#", ".NET", "SQL Server"], "gamepad", "navy")
    card("card-nichodev.svg", "Nicho.dev", "Portfolio site",
         "My portfolio, with layered project stacks and a 3D room where the laptop has a working desktop.",
         ["JavaScript", "Three.js"], "monitor", "clay")
    card("card-cinematheque.svg", "Cinematheque", "Web app",
         "A cinema web app built with Laravel and Blade.",
         ["Laravel", "PHP", "MySQL"], "film", "brick")
    card("card-sagap.svg", "sagap", "Mobile app",
         "A mobile app that maps Wi-Fi dead zones.",
         ["Flutter", "Dart"], "wifi", "teal")
    card("card-payroller.svg", "PayRoller", "Desktop app",
         "A payroll system with employee records, automatic pay computation and payroll history.",
         ["Python", "PyQt6", "SQLite"], "coin", "gold")
