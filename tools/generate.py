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


# ---------------------------------------------------------------- project art
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
    w, h = 330, 214
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
    s += f'<rect x="{x0 + w - 118}" y="{y0 + h - 40}" width="104" height="26" rx="13" fill="{c["text"]}"/>'
    s += t("Book seats", x0 + w - 66, y0 + h - 23, 12, c["plane"] if c is THEMES["dark"] else "#ffffff", 700, anchor="middle")
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
        desc="A cozy study garden: focus and your plant grows, give up and it wilts. AI turns your notes into quizzes.",
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
        desc="A customer system for stores that sell gaming PC parts: who each customer is, what they buy, owe and need.",
        stack="C# · .NET WinForms · SQL Server · EF Core",
        proof=[("15", "use cases"), ("4", "user roles"), ("1", "database per store")],
        art=art_xpera,
    ),
]


# ---------------------------------------------------------------- hero
LOOP = 10.0  # seconds for one full build of the stack


def layer_content(kind, c, pw, ph):
    """Contents of one layer, in flat plane coordinates (before the iso transform)."""
    s = ""
    if kind == "sketch":
        s += f'<rect width="{pw}" height="{ph}" rx="14" fill="{c["plane"]}" fill-opacity="0.6" stroke="{c["wire"]}" stroke-dasharray="6 6"/>'
        for y, w in [(30, 150), (54, 110), (100, 200), (124, 170), (148, 120)]:
            s += f'<path d="M22 {y} q {w / 4} -5 {w / 2} 0 t {w / 2} 0" stroke="{c["faint"]}" stroke-width="2.4" stroke-linecap="round"/>'
    elif kind == "wire":
        s += f'<rect width="{pw}" height="{ph}" rx="14" fill="{c["plane"]}" fill-opacity="0.85" stroke="{c["wire"]}"/>'
        s += f'<rect x="18" y="18" width="{pw - 36}" height="18" rx="5" stroke="{c["wire"]}"/>'
        s += f'<rect x="18" y="48" width="110" height="80" rx="7" stroke="{c["wire"]}"/>'
        s += f'<path d="M18 48 L128 128 M128 48 L18 128" stroke="{c["wire"]}"/>'
        for i in range(3):
            s += f'<rect x="142" y="{52 + i * 18}" width="{96 - i * 22}" height="8" rx="4" fill="{c["block"]}"/>'
        s += f'<rect x="142" y="110" width="70" height="18" rx="9" stroke="{c["wire"]}"/>'
    elif kind == "design":
        s += f'<rect width="{pw}" height="{ph}" rx="14" fill="{c["plane2"]}" stroke="{c["line2"]}"/>'
        for i, col in enumerate([c["text"], c["accent"], c["gold"], c["green"]]):
            s += f'<circle cx="{34 + i * 28}" cy="36" r="10" fill="{col}"/>'
        s += t("Aa", 176, 48, 32, c["text"], 700)
        s += f'<rect x="18" y="70" width="{pw - 36}" height="1" fill="{c["line2"]}"/>'
        s += f'<rect x="18" y="88" width="130" height="12" rx="3" fill="{c["text"]}" fill-opacity="0.75"/>'
        s += f'<rect x="18" y="110" width="190" height="7" rx="3.5" fill="{c["block"]}"/>'
        s += f'<rect x="18" y="124" width="150" height="7" rx="3.5" fill="{c["block"]}"/>'
    else:  # build
        s += f'<rect width="{pw}" height="{ph}" rx="14" fill="{c["plane2"]}" stroke="{c["accent"]}" stroke-opacity="0.55"/>'
        s += f'<rect x="18" y="18" width="{pw - 36}" height="22" rx="6" fill="{c["block"]}"/>'
        s += f'<circle cx="32" cy="29" r="5" fill="{c["accent"]}"/>'
        s += f'<rect x="18" y="52" width="{pw - 36}" height="74" rx="10" fill="{c["block"]}"/>'
        s += f'<rect x="32" y="66" width="96" height="10" rx="5" fill="{c["text"]}" fill-opacity="0.85"/>'
        s += f'<rect x="32" y="86" width="{pw - 100}" height="7" rx="3.5" fill="{c["wire"]}"/>'
        s += f'<rect class="ship" x="32" y="86" width="{pw - 100}" height="7" rx="3.5" fill="{c["green"]}"/>'
        s += f'<rect x="32" y="102" width="64" height="16" rx="8" fill="{c["accent"]}"/>'
    return s


def hero(theme):
    c = THEMES[theme]
    W, H = 1000, 330
    b = ""
    x = 2

    # Left column: who I am, kept compact.
    b += f'<g class="fu" style="animation-delay:.05s">{mono("Davao City, Philippines", x, 44, c["accent"], 12)}</g>'
    b += (
        f'<g class="fu" style="animation-delay:.12s">'
        f'<text x="{x}" y="104" font-family="{SANS}" font-size="54" font-weight="800" letter-spacing="-1.8">'
        f'<tspan fill="{c["text"]}">Nicho </tspan>'
        f'<tspan fill="none" stroke="{c["text"]}" stroke-width="1.3">Lescano</tspan></text></g>'
    )
    b += f'<g class="fu" style="animation-delay:.2s">{t("UI/UX designer and developer, also into machine", x, 142, 17, c["text"], 500)}</g>'
    b += f'<g class="fu" style="animation-delay:.24s">{t("learning and AI automation.", x, 166, 17, c["text"], 500)}</g>'
    b += f'<g class="fu" style="animation-delay:.28s">{t("I draw every project first, then build it, layer by layer.", x, 192, 15.5, c["muted"])}</g>'

    # Numbers strip.
    b += f'<rect class="ul" x="{x}" y="226" width="520" height="1" fill="{c["line2"]}"/>'
    stats = [("3", "systems", "shipped"), ("201", "automated", "tests"), ("18", "real", "testers"), ("30", "days to", "ship kuwaGO")]
    for i, (n, l1, l2) in enumerate(stats):
        sx = x + i * 132
        d = 0.4 + i * 0.1
        b += (
            f'<g class="fu" style="animation-delay:{d:.2f}s">'
            + t(n, sx, 272, 32, c["accent"] if i == 1 else c["text"], 800, ls=-1)
            + mono(l1, sx, 296, c["muted"], 10.5)
            + mono(l2, sx, 312, c["muted"], 10.5)
            + "</g>"
        )

    # Right column: the stack builds itself, one layer at a time.
    pw, ph, sc = 260, 170, 0.8
    ox = 568 + ph * 0.866 * sc  # top corner of each plane
    top_y = 18
    gap = 34
    kinds = [("sketch", "01 Sketch"), ("wire", "02 Wireframe"), ("design", "03 Design"), ("build", "04 Build")]
    mat = lambda y: f"matrix({0.866 * sc:.4f},{0.5 * sc:.4f},{-0.866 * sc:.4f},{0.5 * sc:.4f},{ox:.1f},{y})"
    style = FADE_UP + (
        f".ul{{transform-box:fill-box;transform-origin:left;animation:ul 1.6s {EASE} both .3s}}"
        "@keyframes ul{from{transform:scaleX(0)}}"
    )
    for i, (kind, name) in enumerate(kinds):  # bottom layer first
        y = top_y + (3 - i) * gap
        land = (0.4 + i * 1.1) / LOOP * 100  # % of the loop when this layer lands
        start = max(land - 7, 0)
        filt = ' filter="url(#glow)"' if kind == "build" else ""
        b += f'<g class="L{i}"><g transform="{mat(y)}"{filt}>{layer_content(kind, c, pw, ph)}</g></g>'
        style += (
            f".L{i}{{animation:L{i} {LOOP}s {EASE} infinite both}}"
            f"@keyframes L{i}{{0%,{start:.1f}%{{opacity:0;transform:translateY(-34px)}}"
            f"{land:.1f}%,88%{{opacity:1;transform:translateY(0)}}96%,100%{{opacity:0;transform:translateY(0)}}}}"
        )
        # Legend on the right, lined up with each layer's right corner.
        cy = y + pw * 0.5 * sc
        rx = ox + pw * 0.866 * sc
        b += f'<path d="M{rx + 8:.0f} {cy:.0f} h14" stroke="{c["line2"]}"/>'
        b += mono(name, rx + 28, cy + 4, c["faint"], 10.5)
        b += f'<g class="N{i}">{mono(name, rx + 28, cy + 4, c["accent"], 10.5, weight=700)}</g>'
        style += (
            f".N{i}{{animation:N{i} {LOOP}s {EASE} infinite both}}"
            f"@keyframes N{i}{{0%,{start:.1f}%{{opacity:0}}{land:.1f}%,88%{{opacity:1}}96%,100%{{opacity:0}}}}"
        )
    ship_at = (0.4 + 3 * 1.1) / LOOP * 100 + 3
    style += (
        f".ship{{transform-box:fill-box;transform-origin:left;animation:ship {LOOP}s {EASE_IO} infinite both}}"
        f"@keyframes ship{{0%,{ship_at:.1f}%{{transform:scaleX(0)}}{ship_at + 22:.1f}%,100%{{transform:scaleX(1)}}}}"
    )
    defs = (
        '<filter id="glow" x="-30%" y="-30%" width="160%" height="170%">'
        f'<feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="{c["glow"]}" flood-opacity="{c["glow_op"]}"/></filter>'
    )
    save("hero", theme, svg(W, H, b, style, "Nicho Lescano, UI/UX designer and developer in Davao City. 3 systems shipped, 201 automated tests, 18 real testers.", defs))


# ---------------------------------------------------------------- section label
def label(name, num, title, right, theme):
    c = THEMES[theme]
    W, H = 1000, 36
    b = mono(num, 0, 22, c["accent"], 12.5, weight=600)
    b += mono(title, 32, 22, c["text"], 12.5, weight=600)
    tw = 32 + len(title) * 9 + 16
    rw = len(right) * 8.4 + 16
    b += f'<rect class="ln" x="{tw:.0f}" y="17.5" width="{W - tw - rw:.0f}" height="1" fill="{c["line2"]}"/>'
    b += mono(right, W, 22, c["muted"], 11, anchor="end")
    style = f".ln{{transform-box:fill-box;transform-origin:left;animation:ln 1.6s {EASE} both .2s}}@keyframes ln{{from{{transform:scaleX(0)}}}}"
    save(name, theme, svg(W, H, b, style, f"{num} {title}"))


# ---------------------------------------------------------------- project rows
def work(p, theme):
    c = THEMES[theme]
    W, H = 1000, 220
    b = ""
    b += f'<g class="fu">{mono(p["fig"], 0, 34, c["accent"], 11.5)}</g>'
    b += f'<g class="fu" style="animation-delay:.06s">{t(p["name"], -1, 74, 32, c["text"], 800, ls=-1)}</g>'
    for i, line in enumerate(wrap(p["desc"], 62)[:2]):
        b += f'<g class="fu" style="animation-delay:{.12 + i * .05:.2f}s">{t(line, 0, 108 + i * 24, 16, c["body"])}</g>'
    b += f'<g class="fu" style="animation-delay:.24s">{mono(p["stack"], 0, 170, c["muted"], 10.5)}</g>'
    x = 0
    for n, lab in p["proof"]:
        b += t(n, x, 200, 17, c["text"], 800)
        nw = len(n) * 10.5 + 6
        b += mono(lab, x + nw, 199, c["muted"], 10)
        x += nw + len(lab) * 7.9 + 24
    art, astyle = p["art"](c, 0, 0)
    b += f'<g class="fu" style="animation-delay:.15s"><g transform="translate(676 10) scale(0.72)">{art}</g></g>'
    b += f'<rect x="0" y="{H - 1}" width="{W}" height="1" fill="{c["line"]}"/>'
    save(p["file"], theme, svg(W, H, b, FADE_UP + astyle, f'{p["name"]}: {p["desc"]}'))


# ---------------------------------------------------------------- skills
def skills(theme):
    c = THEMES[theme]
    items = [
        ("Design", "Figma · UI/UX · Brand and logo · Prototyping"),
        ("Web", "Laravel · PHP · JavaScript · REST APIs"),
        ("Mobile", "Flutter · Dart · Firebase"),
        ("Desktop", "C# · .NET WinForms · ASP.NET API"),
        ("Data", "MySQL · SQL Server · EF Core"),
        ("AI & ML", "Machine learning · AI automation · Gemini"),
    ]
    rh = 62
    W, H = 1000, 8 + rh * 3
    b = ""
    for i, (area, tools) in enumerate(items):
        col, row = i % 2, i // 2
        x = col * 520
        y = 4 + row * rh
        b += f'<g class="fu" style="animation-delay:{.05 + i * .06:.2f}s">'
        b += f'<rect x="{x}" y="{y}" width="480" height="1" fill="{c["line"]}"/>'
        b += mono(f"0{i + 1}", x, y + 28, c["accent"], 11, weight=600)
        b += t(area, x + 40, y + 29, 16, c["text"], 700)
        b += t(tools, x + 40, y + 51, 14, c["muted"])
        b += "</g>"
    save("skills", theme, svg(W, H, b, FADE_UP, "Skills: " + "; ".join(f"{a}: {tl}" for a, tl in items)))


if __name__ == "__main__":
    if os.path.isdir(OUT):
        for f in os.listdir(OUT):
            if f.endswith(".svg"):
                os.remove(os.path.join(OUT, f))
    print("writing assets:")
    for th in THEMES:
        hero(th)
        label("label-work", "01", "Selected work", "Fig. 01–03", th)
        label("label-skills", "02", "Skills", "Area / tools", th)
        for p in PROJECTS:
            work(p, th)
        skills(th)
