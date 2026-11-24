"""Generates the SVGs used in the profile README.

Run:  python tools/generate.py   (writes into assets/)

Every graphic is written twice, as name-dark.svg and name-light.svg, with a
transparent background, so the README can swap them with <picture> and the
art sits directly on GitHub's own page colour instead of in a box.
The look follows nicho-dev.vercel.app: cream / ink type, an orange accent,
small monospace labels and stacked wireframe layers.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

SANS = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI Variable Display', 'Segoe UI', Inter, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', 'Cascadia Code', 'JetBrains Mono', Consolas, Menlo, monospace"
EASE = "cubic-bezier(.22,1,.36,1)"  # long, soft ease-out
EASE_IO = "cubic-bezier(.65,0,.35,1)"

THEMES = {
    "dark": dict(
        text="#f4efe6", body="#c9c4bb", muted="#8b8781", faint="#5b5852",
        line="rgba(244,239,230,0.14)", line2="rgba(244,239,230,0.28)",
        accent="#e2763f", gold="#c9a227", green="#7cc47f",
        plane="#16181d", plane2="#1c1f25", wire="rgba(244,239,230,0.22)", block="rgba(244,239,230,0.10)",
        glow="#7cc47f", glow_op="0.35",
    ),
    "light": dict(
        text="#141414", body="#3d3b38", muted="#6b6862", faint="#a19d96",
        line="rgba(20,20,20,0.12)", line2="rgba(20,20,20,0.26)",
        accent="#cf5f28", gold="#a8861a", green="#3f8f4a",
        plane="#ffffff", plane2="#faf8f4", wire="rgba(20,20,20,0.22)", block="rgba(20,20,20,0.07)",
        glow="#141414", glow_op="0.10",
    ),
}


# ---------------------------------------------------------------- helpers
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(s, x, y, size, fill, weight=400, font=SANS, anchor="start", ls=0, extra=""):
    a = f' letter-spacing="{ls}"' if ls else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}"{a}{extra}>{esc(s)}</text>'
    )


def mono(s, x, y, fill, size=12, anchor="start", weight=500, extra=""):
    return t(s.upper(), x, y, size, fill, weight, MONO, anchor, 1.2, extra)


def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    lines.append(cur)
    return lines


def svg(w, h, body, style="", title="", defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'fill="none" role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
        f"<defs>{defs}</defs><style>{style}</style>{body}</svg>"
    )


def save(name, theme, content):
    os.makedirs(OUT, exist_ok=True)
    fn = f"{name}-{theme}.svg"
    with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {fn:28s} {len(content) // 1024} KB")


FADE_UP = (
    f".fu{{animation:fu 1.2s {EASE} both}}"
    "@keyframes fu{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}"
)

ISO = "matrix(0.866,0.5,-0.866,0.5,{x},{y})"  # flat plane, isometric


# ---------------------------------------------------------------- hero
def layer_content(kind, c, pw, ph):
    """Contents of one wireframe layer, in flat plane coordinates."""
    s = ""
    if kind == "sketch":
        s += f'<rect x="0" y="0" width="{pw}" height="{ph}" rx="12" fill="{c["plane"]}" fill-opacity="0.55" stroke="{c["wire"]}" stroke-dasharray="5 6"/>'
        for i, (y, w) in enumerate([(30, 150), (52, 110), (100, 200), (122, 170), (144, 130)]):
            s += f'<path d="M20 {y} q {w / 4} -4 {w / 2} 0 t {w / 2} 0" stroke="{c["faint"]}" stroke-width="2" stroke-linecap="round"/>'
        s += mono("01 sketch", 18, ph - 14, c["muted"], 11)
    elif kind == "wire":
        s += f'<rect x="0" y="0" width="{pw}" height="{ph}" rx="12" fill="{c["plane"]}" fill-opacity="0.8" stroke="{c["wire"]}"/>'
        s += f'<rect x="16" y="16" width="{pw - 32}" height="18" rx="4" stroke="{c["wire"]}"/>'
        s += f'<rect x="16" y="44" width="110" height="76" rx="6" stroke="{c["wire"]}"/>'
        s += f'<path d="M16 44 L126 120 M126 44 L16 120" stroke="{c["wire"]}"/>'
        for i in range(3):
            s += f'<rect x="140" y="{48 + i * 18}" width="{100 - i * 22}" height="8" rx="4" fill="{c["block"]}"/>'
        s += f'<rect x="140" y="104" width="70" height="16" rx="8" stroke="{c["wire"]}"/>'
        s += mono("02 wireframe", 18, ph - 14, c["muted"], 11)
    elif kind == "design":
        s += f'<rect x="0" y="0" width="{pw}" height="{ph}" rx="12" fill="{c["plane2"]}" stroke="{c["line2"]}"/>'
        for i, col in enumerate([c["text"], c["accent"], c["body"], c["gold"]]):
            s += f'<circle cx="{30 + i * 26}" cy="32" r="9" fill="{col}"/>'
        s += t("Aa", pw - 70, 44, 30, c["text"], 700)
        s += f'<rect x="16" y="64" width="{pw - 32}" height="1" fill="{c["line2"]}"/>'
        s += t("Display 64/600", 18, 92, 13, c["body"], 600)
        s += t("Body 16/400", 18, 112, 12, c["muted"])
        s += mono("03 design", 18, ph - 14, c["muted"], 11)
    else:  # build
        s += f'<rect x="0" y="0" width="{pw}" height="{ph}" rx="12" fill="{c["plane2"]}" stroke="{c["line2"]}"/>'
        s += f'<rect x="16" y="16" width="{pw - 32}" height="22" rx="6" fill="{c["block"]}"/>'
        s += f'<circle cx="30" cy="27" r="5" fill="{c["accent"]}"/>'
        s += f'<rect x="16" y="50" width="{pw - 32}" height="66" rx="10" fill="{c["block"]}"/>'
        s += f'<rect x="30" y="64" width="90" height="9" rx="4.5" fill="{c["text"]}" fill-opacity="0.8"/>'
        s += f'<rect x="30" y="80" width="{pw - 92}" height="6" rx="3" fill="{c["block"]}"/>'
        s += f'<rect class="bar" x="30" y="80" width="{pw - 92}" height="6" rx="3" fill="{c["green"]}"/>'
        s += f'<rect x="30" y="94" width="60" height="14" rx="7" fill="{c["accent"]}"/>'
        s += mono("04 build & ship", 18, ph - 14, c["muted"], 11)
    return s


def hero(theme):
    c = THEMES[theme]
    W, H = 1000, 460
    b = ""
    # Left: name block.
    x = 4
    b += f'<g class="fu" style="animation-delay:.1s">{mono("Davao City, Philippines", x, 70, c["accent"], 13)}</g>'
    b += f'<g class="fu" style="animation-delay:.2s">{t("NICHO", x, 162, 96, c["text"], 800, ls=-3)}</g>'
    b += (
        f'<g class="fu" style="animation-delay:.3s">'
        f'<text x="{x}" y="258" font-family="{SANS}" font-size="96" font-weight="800" letter-spacing="-3" '
        f'fill="none" stroke="{c["text"]}" stroke-width="1.6">LESCANO</text></g>'
    )
    lines = [
        ("UI/UX designer and developer, also into", c["text"]),
        ("machine learning and AI automation.", c["text"]),
        ("I draw every project first, then build it,", c["muted"]),
        ("layer by layer.", c["muted"]),
    ]
    for i, (s, col) in enumerate(lines):
        b += f'<g class="fu" style="animation-delay:{.45 + i * .06:.2f}s">{t(s, x, 310 + i * 26, 18, col, 500)}</g>'
    # Meta row.
    b += f'<rect x="{x}" y="412" width="470" height="1" fill="{c["line"]}"/>'
    for i, (k, v) in enumerate([("Builds", "Web · Mobile · Desktop"), ("Designs in", "Figma"), ("Studying", "BS IT, UM")]):
        cx = x + (0, 210, 330)[i]
        b += f'<g class="fu" style="animation-delay:{.8 + i * .08:.2f}s">{mono(k, cx, 436, c["accent"], 10.5)}{mono(v, cx, 454, c["text"], 10.5, weight=600)}</g>'

    # Right: the stack of wireframe layers.
    pw, ph = 260, 180
    ox = 560 + ph * 0.866 + 10
    oy = 70
    gap = 52
    kinds = ["sketch", "wire", "design", "build"]
    for i, kind in enumerate(kinds):  # bottom first
        y = oy + (3 - i) * gap
        filt = ' filter="url(#glow)"' if kind == "build" else ""
        b += (
            f'<g class="L{i}"><g transform="{ISO.format(x=round(ox, 1), y=y)}"{filt}>'
            f"{layer_content(kind, c, pw, ph)}</g></g>"
        )
    defs = (
        '<filter id="glow" x="-30%" y="-30%" width="160%" height="160%">'
        f'<feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="{c["glow"]}" flood-opacity="{c["glow_op"]}"/></filter>'
    )
    # Layers breathe apart and back together.
    style = FADE_UP
    for i, d in enumerate([18, 6, -6, -18]):
        style += (
            f".L{i}{{animation:l{i} 7s {EASE_IO} infinite}}"
            f"@keyframes l{i}{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY({d}px)}}}}"
        )
    style += (
        f".bar{{transform-box:fill-box;transform-origin:left;animation:bar 7s {EASE_IO} infinite}}"
        "@keyframes bar{0%{transform:scaleX(.08)}60%,100%{transform:scaleX(1)}}"
    )
    save("hero", theme, svg(W, H, b, style, "Nicho Lescano. UI/UX designer and developer, also into machine learning and AI automation. Based in Davao City, Philippines.", defs))


# ---------------------------------------------------------------- section label
def label(name, num, title, right, theme):
    c = THEMES[theme]
    W, H = 1000, 40
    b = mono(num, 0, 24, c["accent"], 13, weight=600)
    b += mono(title, 34, 24, c["text"], 13, weight=600)
    tw = 34 + len(title) * 9.4 + 18
    rw = len(right) * 8.6 + 18
    b += f'<rect class="ln" x="{tw:.0f}" y="19" width="{W - tw - rw:.0f}" height="1" fill="{c["line2"]}"/>'
    b += mono(right, W, 24, c["muted"], 11.5, anchor="end")
    style = f".ln{{transform-box:fill-box;transform-origin:left;animation:ln 1.6s {EASE} both .2s}}@keyframes ln{{from{{transform:scaleX(0)}}}}"
    save(name, theme, svg(W, H, b, style, f"{num} {title}"))


# ---------------------------------------------------------------- project rows
def art_kuwago(c, x0, y0):
    s = ""
    for i in range(3):
        px, py = x0 + i * 112, y0 + (0, -12, 6)[i]
        s += f'<rect x="{px}" y="{py}" width="92" height="184" rx="16" stroke="{c["line2"]}" fill="{c["plane"]}" fill-opacity="0.35"/>'
        s += f'<rect x="{px + 34}" y="{py + 8}" width="24" height="5" rx="2.5" fill="{c["block"]}"/>'
    # phone 1: focus timer ring
    cx, cy = x0 + 46, y0 + 78
    s += f'<circle cx="{cx}" cy="{cy}" r="28" stroke="{c["block"]}" stroke-width="5"/>'
    s += (
        f'<circle class="ring" cx="{cx}" cy="{cy}" r="28" stroke="{c["accent"]}" stroke-width="5" '
        f'stroke-linecap="round" stroke-dasharray="176" transform="rotate(-90 {cx} {cy})"/>'
    )
    s += t("25:00", cx, cy + 5, 13, c["text"], 700, anchor="middle")
    s += f'<rect x="{x0 + 18}" y="{y0 + 130}" width="56" height="16" rx="8" fill="{c["accent"]}"/>'
    # phone 2: a sprout growing
    gx, gy = x0 + 158, y0 + 140
    s += f'<rect x="{gx - 22}" y="{gy}" width="44" height="18" rx="5" fill="{c["block"]}"/>'
    s += f'<path class="stem" d="M{gx} {gy} C {gx} {gy - 30}, {gx - 4} {gy - 50}, {gx} {gy - 70}" stroke="{c["green"]}" stroke-width="3" stroke-linecap="round" pathLength="1" stroke-dasharray="1"/>'
    s += f'<path class="leaf l1" d="M{gx} {gy - 40} c -18 -4 -26 -16 -24 -26 c 14 2 22 12 24 26 z" fill="{c["green"]}"/>'
    s += f'<path class="leaf l2" d="M{gx} {gy - 58} c 18 -4 26 -16 24 -26 c -14 2 -22 12 -24 26 z" fill="{c["green"]}"/>'
    # phone 3: quiz card
    qx, qy = x0 + 236, y0 + 40
    s += f'<rect x="{qx}" y="{qy}" width="68" height="56" rx="8" fill="{c["block"]}"/>'
    for i in range(3):
        s += f'<rect x="{qx}" y="{qy + 66 + i * 20}" width="68" height="14" rx="7" stroke="{c["wire"]}"/>'
    s += f'<rect class="pick" x="{qx}" y="{qy + 86}" width="68" height="14" rx="7" fill="{c["green"]}"/>'
    style = (
        f".ring{{animation:ring 6s {EASE_IO} infinite}}@keyframes ring{{0%{{stroke-dashoffset:176}}70%,100%{{stroke-dashoffset:0}}}}"
        f".stem{{animation:stem 6s {EASE} infinite}}@keyframes stem{{0%{{stroke-dashoffset:1}}45%,100%{{stroke-dashoffset:0}}}}"
        f".leaf{{transform-box:fill-box;animation:leaf 6s {EASE} infinite}}.l1{{transform-origin:right bottom}}.l2{{transform-origin:left bottom;animation-delay:.3s}}"
        "@keyframes leaf{0%,25%{transform:scale(0)}55%,100%{transform:scale(1)}}"
        f".pick{{animation:pick 6s {EASE} infinite}}@keyframes pick{{0%,40%{{opacity:0}}55%,100%{{opacity:.9}}}}"
    )
    return s, style


def art_cinema(c, x0, y0):
    s = ""
    w, h = 330, 180
    s += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="12" stroke="{c["line2"]}" fill="{c["plane"]}" fill-opacity="0.35"/>'
    s += f'<path d="M{x0} {y0 + 24} H{x0 + w}" stroke="{c["line"]}"/>'
    for i in range(3):
        s += f'<circle cx="{x0 + 16 + i * 12}" cy="{y0 + 12}" r="3.5" fill="{c["block"]}"/>'
    s += f'<path d="M{x0 + 80} {y0 + 50} Q {x0 + w / 2} {y0 + 36} {x0 + w - 80} {y0 + 50}" stroke="{c["muted"]}" stroke-width="2" stroke-linecap="round"/>'
    s += mono("screen", x0 + w / 2, y0 + 66, c["faint"], 9, anchor="middle")
    picks = {(2, 4): 0, (2, 5): 1, (2, 6): 2}
    for r in range(5):
        for col in range(11):
            if col == 5 and False:
                continue
            cx = x0 + 45 + col * 22 + (6 if col > 4 else 0)
            cy = y0 + 84 + r * 16
            s += f'<rect x="{cx}" y="{cy}" width="14" height="10" rx="3" fill="{c["block"]}"/>'
            if (r, col) in picks:
                s += f'<rect class="seat" style="animation-delay:{picks[(r, col)] * .35:.2f}s" x="{cx}" y="{cy}" width="14" height="10" rx="3" fill="{c["accent"]}"/>'
    s += f'<rect x="{x0 + w - 104}" y="{y0 + h + 14}" width="104" height="26" rx="13" fill="{c["text"]}"/>'
    s += t("Book seats", x0 + w - 52, y0 + h + 31, 12, c["plane"] if c is THEMES["dark"] else "#ffffff", 700, anchor="middle")
    style = (
        f".seat{{animation:seat 5s {EASE} infinite both}}"
        "@keyframes seat{0%,15%{opacity:0;transform:translateY(-3px)}30%,85%{opacity:1;transform:none}100%{opacity:0}}"
    )
    return s, style


def art_xpera(c, x0, y0):
    s = ""
    w, h = 330, 200
    s += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="12" stroke="{c["line2"]}" fill="{c["plane"]}" fill-opacity="0.35"/>'
    s += f'<path d="M{x0 + 52} {y0} V{y0 + h}" stroke="{c["line"]}"/>'
    for i in range(4):
        s += f'<rect x="{x0 + 16}" y="{y0 + 20 + i * 30}" width="20" height="20" rx="6" fill="{c["accent"] if i == 1 else c["block"]}"/>'
    for i, k in enumerate(["Customers", "Sales", "Inquiries"]):
        kx = x0 + 68 + i * 86
        s += f'<rect x="{kx}" y="{y0 + 16}" width="76" height="46" rx="8" fill="{c["block"]}"/>'
        s += t(k, kx + 10, y0 + 33, 9.5, c["muted"], 500)
        s += f'<rect x="{kx + 10}" y="{y0 + 42}" width="{(40, 30, 22)[i]}" height="8" rx="4" fill="{c["text"]}" fill-opacity="0.7"/>'
    base = y0 + h - 22
    heights = [40, 62, 48, 86, 70, 104, 92]
    for i, hh in enumerate(heights):
        bx = x0 + 72 + i * 34
        col = c["accent"] if i == 5 else c["wire"]
        s += f'<rect class="bar" style="animation-delay:{i * .08:.2f}s" x="{bx}" y="{base - hh}" width="20" height="{hh}" rx="4" fill="{col}"/>'
    s += f'<path d="M{x0 + 66} {base} H{x0 + w - 16}" stroke="{c["line2"]}"/>'
    style = (
        f".bar{{transform-box:fill-box;transform-origin:bottom;animation:grow 6s {EASE} infinite both}}"
        "@keyframes grow{0%{transform:scaleY(.05)}25%,85%{transform:scaleY(1)}100%{transform:scaleY(.05)}}"
    )
    return s, style


PROJECTS = [
    dict(
        file="work-kuwago", fig="Fig. 01 / Mobile app", name="kuwaGO",
        desc="A cozy study garden. Finish a focus session and your plant grows; give up and it wilts. AI turns your own notes into quizzes.",
        stack="Flutter · Firebase · Gemini · Cloudflare Workers",
        proof=[("30", "days to ship"), ("18", "testers"), ("72", "tests")],
        art=art_kuwago,
    ),
    dict(
        file="work-cinematheque", fig="Fig. 02 / Web system", name="Cinematheque",
        desc="Ticketing for a real cinema. Moviegoers pick exact seats, pay online and get an e-ticket; staff run schedules and reports.",
        stack="Laravel 12 · MySQL · PayMongo · Blade",
        proof=[("129", "tests"), ("3", "person team"), ("1", "real client")],
        art=art_cinema,
    ),
    dict(
        file="work-xpera", fig="Fig. 03 / Desktop system", name="xpera CRM",
        desc="A customer system for small stores that sell gaming PC parts: who each customer is, what they buy, owe and need.",
        stack="C# · .NET WinForms · SQL Server · EF Core",
        proof=[("15", "use cases"), ("4", "user roles"), ("1", "database per store")],
        art=art_xpera,
    ),
]


def work(p, theme):
    c = THEMES[theme]
    W, H = 1000, 290
    b = ""
    b += f'<g class="fu">{mono(p["fig"], 0, 40, c["accent"], 12)}</g>'
    b += f'<g class="fu" style="animation-delay:.08s">{t(p["name"], -2, 92, 46, c["text"], 800, ls=-1.5)}</g>'
    for i, line in enumerate(wrap(p["desc"], 52)[:3]):
        b += f'<g class="fu" style="animation-delay:{.16 + i * .05:.2f}s">{t(line, 0, 128 + i * 25, 16.5, c["body"])}</g>'
    b += f'<g class="fu" style="animation-delay:.32s">{mono(p["stack"], 0, 214, c["muted"], 11)}</g>'
    x = 0
    for n, lab in p["proof"]:
        b += t(n, x, 256, 24, c["text"], 700)
        nw = len(n) * 14 + 8
        b += mono(lab, x + nw, 255, c["muted"], 10.5)
        x += nw + len(lab) * 8.2 + 30
    art, astyle = p["art"](c, 620, 44)
    b += f'<g class="fu" style="animation-delay:.2s">{art}</g>'
    b += f'<rect x="0" y="{H - 1}" width="{W}" height="1" fill="{c["line"]}"/>'
    save(p["file"], theme, svg(W, H, b, FADE_UP + astyle, f'{p["name"]}: {p["desc"]}'))


# ---------------------------------------------------------------- process
def process(theme):
    c = THEMES[theme]
    W, H = 1000, 190
    steps = [
        ("Brief", "What it's for,", "and who uses it."),
        ("Sketch", "Rough lines,", "cheap to change."),
        ("Wireframe", "Boxes, hierarchy", "and flow."),
        ("Design", "Decided before", "the code."),
        ("Build & ship", "Built, tested,", "shipped."),
    ]
    step = 212
    y = 40
    b = f'<rect x="8" y="{y - 0.5}" width="{step * 4}" height="1" fill="{c["line2"]}"/>'
    b += f'<rect class="prog" x="8" y="{y - 1}" width="{step * 4}" height="2" fill="{c["accent"]}"/>'
    total = 8.0
    style = (
        f".prog{{transform-box:fill-box;transform-origin:left;animation:prog {total}s {EASE_IO} infinite}}"
        "@keyframes prog{0%{transform:scaleX(0)}70%,92%{transform:scaleX(1)}100%{transform:scaleX(1);opacity:0}}"
    )
    for i, (name, l1, l2) in enumerate(steps):
        x = 8 + i * step
        at = i / 4 * 70  # percent of the loop when the line reaches this dot
        b += f'<circle cx="{x}" cy="{y}" r="7" fill="{c["plane"]}" stroke="{c["line2"]}" stroke-width="1.5"/>'
        b += f'<circle class="d{i}" cx="{x}" cy="{y}" r="7" fill="{c["accent"]}"/>'
        style += (
            f".d{i}{{transform-box:fill-box;transform-origin:center;animation:d{i} {total}s {EASE} infinite}}"
            f"@keyframes d{i}{{0%,{max(at - 0.1, 0):.1f}%{{transform:scale(0)}}{at + 4:.1f}%,92%{{transform:scale(1)}}100%{{transform:scale(0)}}}}"
        )
        tx = x - 8
        b += mono(f"0{i + 1}", tx, y + 44, c["accent"], 11.5, weight=600)
        b += t(name, tx, y + 74, 21, c["text"], 700, ls=-0.4)
        b += t(l1, tx, y + 102, 14.5, c["muted"])
        b += t(l2, tx, y + 122, 14.5, c["muted"])
    save("process", theme, svg(W, H, b, style, "How I work: brief, sketch, wireframe, design, build and ship"))


# ---------------------------------------------------------------- numbers
def numbers(theme):
    c = THEMES[theme]
    W, H = 1000, 150
    items = [
        ("3", "systems shipped", "mobile, web, desktop"),
        ("201", "automated tests", "across two projects"),
        ("18", "real testers", "on kuwaGO"),
        ("30", "days to ship", "kuwaGO, idea to release"),
    ]
    b = ""
    style = FADE_UP + (
        f".ul{{transform-box:fill-box;transform-origin:left;animation:ul 1.8s {EASE} both}}"
        "@keyframes ul{from{transform:scaleX(0)}}"
    )
    for i, (n, l1, l2) in enumerate(items):
        x = i * 250
        d = 0.15 + i * 0.12
        b += f'<g class="fu" style="animation-delay:{d:.2f}s">{t(n, x - 3, 70, 68, c["text"], 800, ls=-2.5)}</g>'
        b += f'<rect class="ul" style="animation-delay:{d + .2:.2f}s" x="{x}" y="90" width="210" height="1.5" fill="{c["accent"] if i == 1 else c["line2"]}"/>'
        b += f'<g class="fu" style="animation-delay:{d + .1:.2f}s">{mono(l1, x, 116, c["text"], 11.5, weight=600)}{mono(l2, x, 136, c["muted"], 10.5)}</g>'
    save("numbers", theme, svg(W, H, b, style, "3 systems shipped, 201 automated tests, 18 real testers, 30 days from idea to release"))


# ---------------------------------------------------------------- skills
def skills(theme):
    c = THEMES[theme]
    rows = [
        ("Design", "Figma · UI/UX · Brand and logo · Prototyping"),
        ("Web", "Laravel · PHP · Blade · HTML · CSS · JavaScript · REST APIs"),
        ("Mobile", "Flutter · Dart · Firebase Auth · Firestore"),
        ("Desktop", "C# · .NET WinForms · ASP.NET API · Java"),
        ("Data", "MySQL · SQL Server · EF Core · Multi-tenant design"),
        ("AI & ML", "Machine learning · AI automation · LLM APIs (Gemini)"),
        ("Tools", "Git and GitHub · Cloudflare Workers · AI-assisted development"),
    ]
    rh = 46
    W, H = 1000, 30 + rh * len(rows)
    b = mono("No.", 0, 16, c["muted"], 10.5) + mono("Area", 70, 16, c["muted"], 10.5) + mono("Tools", 250, 16, c["muted"], 10.5)
    for i, (area, tools) in enumerate(rows):
        y = 30 + i * rh
        b += f'<g class="fu" style="animation-delay:{.05 + i * .07:.2f}s">'
        b += f'<rect x="0" y="{y}" width="{W}" height="1" fill="{c["line"]}"/>'
        b += mono(f"0{i + 1}", 0, y + 29, c["accent"], 11.5, weight=600)
        b += t(area, 70, y + 30, 17, c["text"], 700)
        b += t(tools, 250, y + 30, 15.5, c["body"])
        b += "</g>"
    save("skills", theme, svg(W, H, b, FADE_UP, "Skills: design, web, mobile, desktop, data, AI and ML, tools"))


# ---------------------------------------------------------------- closing line
def closing(theme):
    c = THEMES[theme]
    W, H = 1000, 130
    b = f'<rect x="0" y="0" width="{W}" height="1" fill="{c["line"]}"/>'
    b += t("Draw it first. Then build it,", 0, 62, 34, c["text"], 700, ls=-0.8)
    b += t("layer by layer.", 0, 104, 34, c["muted"], 700, ls=-0.8)
    # A small stack of three cards that settles into place.
    for i in range(3):
        y = 30 + i * 18
        op = (0.35, 0.6, 1)[i]
        b += (
            f'<g class="s{i}"><g transform="{ISO.format(x=880, y=y)}">'
            f'<rect width="110" height="70" rx="8" fill="{c["plane"]}" stroke="{c["accent"] if i == 2 else c["line2"]}" stroke-opacity="{op}"/></g></g>'
        )
    style = ""
    for i, d in enumerate([10, 0, -10]):
        style += f".s{i}{{animation:s{i} 6s {EASE_IO} infinite}}@keyframes s{i}{{50%{{transform:translateY({d}px)}}}}"
    save("closing", theme, svg(W, H, b, style, "Draw it first. Then build it, layer by layer."))


if __name__ == "__main__":
    if os.path.isdir(OUT):
        for f in os.listdir(OUT):
            if f.endswith(".svg"):
                os.remove(os.path.join(OUT, f))
    print("writing assets:")
    for th in THEMES:
        hero(th)
        label("label-work", "01", "Selected work", "Fig. 01–03", th)
        label("label-process", "02", "How I work", "One screen, brief to shipped", th)
        label("label-numbers", "03", "By the numbers", "So far", th)
        label("label-skills", "04", "Skills", "Area / tools", th)
        for p in PROJECTS:
            work(p, th)
        process(th)
        numbers(th)
        skills(th)
        closing(th)
