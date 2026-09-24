"""Build the SVG assets for the GitHub profile README.

Text is converted to outlines (IBM Plex) because GitHub does not load external fonts in SVGs.
Usage: pip install fonttools uharfbuzz && python scripts/build_assets.py
Edit PROJECTS / SECTIONS below and re-run to update the images.
"""
import math, os, random, urllib.request
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
FONT_DIR = os.path.join(ROOT, "scripts", ".fonts")
PLEX = "https://raw.githubusercontent.com/IBM/plex/master/packages/plex-{pkg}/fonts/complete/ttf/{name}.ttf"
FONTS = {"semi": ("sans", "IBMPlexSans-SemiBold"), "reg": ("sans", "IBMPlexSans-Regular"),
         "mono": ("mono", "IBMPlexMono-Regular")}

# ---------------------------------------------------------------- content
BANNER = dict(bg="#1F3A57", ink="#FFFFFF", sub="#D3DEEA", mute="#A9BCD0",
              accent="#9CC7EC", area="#34587C", grid="#2A4868")
PROJECTS = {  # key: (card title, hue)
    "money-market": ("Money market", "#1D5B8F"),
    "vaults": ("ERC-4626 vaults", "#1E7A6A"),
    "staking": ("Real-yield staking", "#5B4A9E"),
    "synthetic": ("Synthetic trading", "#A4561C"),
    "prediction-market": ("Prediction market", "#4A5866"),
    "rwa-security-token": ("RWA security token", "#8A3E6E"),
}
SECTIONS = {  # key: (title, subtitle, colour)
    "featured": ("Featured work", "Protocols I designed and built", "#1F3A57"),
    "security": ("Security reviews", "Training reviews through Cyfrin Updraft", "#8C2F2B"),
    "other": ("Other projects", "Solana, tooling and experiments", "#5A6470"),
}
PAGE = {"light": "#FFFFFF", "dark": "#0D1117"}
TEXT_MUTE = {"light": "#57606A", "dark": "#9198A1"}

# ---------------------------------------------------------------- helpers
_cache = {}

def _font(key):
    if key not in _cache:
        pkg, name = FONTS[key]
        path = os.path.join(FONT_DIR, name + ".ttf")
        if not os.path.exists(path):
            os.makedirs(FONT_DIR, exist_ok=True)
            urllib.request.urlretrieve(PLEX.format(pkg=pkg, name=name), path)
        tt = TTFont(path)
        _cache[key] = (hb.Font(hb.Face(open(path, "rb").read())), tt, tt.getGlyphSet(), tt["head"].unitsPerEm)
    return _cache[key]

def shape(txt, key, size, x=0, y=0):
    font, tt, gs, upem = _font(key)
    buf = hb.Buffer(); buf.add_str(txt); buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    s, pen, cx, order = size / upem, SVGPathPen(gs), 0, tt.getGlyphOrder()
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gs[order[info.codepoint]].draw(TransformPen(pen, (s, 0, 0, -s, x + (cx + pos.x_offset) * s, y - pos.y_offset * s)))
        cx += pos.x_advance
    return pen.getCommands(), cx * s

def text(txt, key, size, x, y, fill, anchor="start", opacity=1):
    w = shape(txt, key, size)[1]
    x -= {"start": 0, "middle": w / 2, "end": w}[anchor]
    return f'<path d="{shape(txt, key, size, x, y)[0]}" fill="{fill}" fill-opacity="{opacity}"/>'

def mix(a, b, t):
    """Blend hex colour a towards b by t (0..1)."""
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]; pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(pa, pb))

def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{label}">{"".join(body)}</svg>')

def colours(hue, mode):
    if mode == "light":
        return dict(bg=mix(hue, "#FFFFFF", .9), fg=hue, soft=hue, node=PAGE["light"])
    return dict(bg=mix(hue, PAGE["dark"], .78), fg=mix(hue, "#FFFFFF", .55), soft=mix(hue, "#FFFFFF", .3),
                node=mix(hue, PAGE["dark"], .78))

# ---------------------------------------------------------------- diagrams
def diagram(kind, c, x, y, w, h):
    fg, o = c["fg"], []
    axes = lambda: [f'<line x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}" stroke="{fg}" stroke-width="2"/>',
                    f'<line x1="{x}" y1="{y+h}" x2="{x}" y2="{y}" stroke="{fg}" stroke-width="2"/>']
    if kind == "money-market":
        random.seed(3); n, b, back, liab = 40, 100, [], []
        for i in range(n):
            b += random.uniform(-1, 2.2); back.append(b)
            u = .64 + .1 * math.sin(i / 4.5) + .2 * math.exp(-((i - 27) / 2.4) ** 2)
            liab.append(b * min(u, .95))
        lo, hi = min(liab) * .5, max(back) * 1.04
        X = lambda i: x + w * i / (n - 1); Y = lambda v: y + h - h * (v - lo) / (hi - lo)
        o.append(f'<polygon points="{x},{y+h} ' + " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(liab))
                 + f' {x+w},{y+h}" fill="{fg}" fill-opacity="0.25"/>')
        o.append(f'<polyline fill="none" stroke="{fg}" stroke-width="4" stroke-linejoin="round" points="'
                 + " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(back)) + '"/>')
        o.append(f'<line x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}" stroke="{fg}" stroke-width="2"/>')
        o.append(text("backing", "reg", 16, x + w, Y(back[-1]) - 12, fg, "end", .85))
        o.append(text("liabilities", "reg", 16, x + w - 6, y + h - 12, fg, "end", .85))
    elif kind == "vaults":
        cx, cy, r = x + w / 2, y + h / 2, min(w, h) * .38
        nodes = [("Vault", -90), ("Aave V3", 30), ("Flash loan", 150)]
        for _, a in nodes:
            a0, a1 = math.radians(a + 24), math.radians(a + 96)
            x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
            o.append(f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}" fill="none" stroke="{fg}" stroke-width="4"/>')
            t = a1 + math.pi / 2
            p1 = (x1 - 15 * math.cos(t - .45), y1 - 15 * math.sin(t - .45)); p2 = (x1 - 15 * math.cos(t + .45), y1 - 15 * math.sin(t + .45))
            o.append(f'<polygon points="{x1:.1f},{y1:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{fg}"/>')
        for name, a in nodes:
            nx, ny = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
            bw = shape(name, "semi", 18)[1] + 28
            o.append(f'<rect x="{nx-bw/2:.1f}" y="{ny-20:.1f}" width="{bw:.1f}" height="40" rx="20" fill="{c["node"]}" stroke="{fg}" stroke-width="2.5"/>')
            o.append(text(name, "semi", 18, nx, ny + 6, fg, "middle"))
    elif kind == "staking":
        o += axes()
        o.append(f'<line x1="{x+6}" y1="{y+h-14}" x2="{x+w-10}" y2="{y+18}" stroke="{fg}" stroke-width="3" stroke-dasharray="9 8" stroke-opacity=".6"/>')
        o.append(f'<line x1="{x+6}" y1="{y+h-34}" x2="{x+w-10}" y2="{y+h-34}" stroke="{fg}" stroke-width="5"/>')
        o.append(text("loop-based", "reg", 17, x + 40, y + 44, fg, "start", .8))
        o.append(text("O(1) accumulator", "semi", 18, x + w - 10, y + h - 48, fg, "end"))
        o.append(text("gas", "reg", 15, x + 12, y + 16, fg, "start", .8))
        o.append(text("stakes and epochs", "reg", 15, x + w, y + h + 22, fg, "end", .8))
    elif kind == "synthetic":
        cx, cy, bw, bh = x + w / 2, y + h / 2, 164, 72
        o.append(f'<rect x="{cx-bw/2}" y="{cy-bh/2}" width="{bw}" height="{bh}" rx="10" fill="{fg}"/>')
        o.append(text("USDC vault", "semi", 20, cx, cy + 7, c["node"], "middle"))
        for side, lab in ((-1, "Traders"), (1, "LPs")):
            ex = cx + side * (w / 2 - 50)
            o.append(f'<circle cx="{ex}" cy="{cy}" r="44" fill="{c["node"]}" stroke="{fg}" stroke-width="2.5"/>')
            o.append(text(lab, "semi", 18, ex, cy + 6, fg, "middle"))
            a, b = cx + side * (bw / 2 + 8), ex - side * 52
            o.append(f'<line x1="{a}" y1="{cy-8}" x2="{b}" y2="{cy-8}" stroke="{fg}" stroke-width="3"/>')
            o.append(f'<line x1="{a}" y1="{cy+8}" x2="{b}" y2="{cy+8}" stroke="{fg}" stroke-width="3" stroke-opacity=".5"/>')
    elif kind == "prediction-market":
        o += axes()
        pts = []
        for i in range(60):
            xv = .12 + i * (1.5 / 59)
            pts.append((x + w * (xv - .1) / 1.55, y + h - h * min(.25 / xv, 2.1) / 2.2))
        o.append(f'<polyline fill="none" stroke="{fg}" stroke-width="4" points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + '"/>')
        o.append(f'<circle cx="{pts[22][0]:.1f}" cy="{pts[22][1]:.1f}" r="9" fill="{fg}"/>')
        o.append(text("x · y = k", "reg", 20, x + w - 8, y + 28, fg, "end"))
    elif kind == "rwa-security-token":
        steps = ["Identity", "Compliance", "Transfer"]
        bw = min(140, (w - 70) / 3); gap = (w - 3 * bw) / 2
        cy = y + h / 2 - 10
        for i, s in enumerate(steps):
            bx = x + i * (bw + gap)
            fill, tc = (fg, c["node"]) if i == 2 else (c["node"], fg)
            o.append(f'<rect x="{bx:.1f}" y="{cy-34}" width="{bw}" height="68" rx="10" fill="{fill}" stroke="{fg}" stroke-width="2.5"/>')
            o.append(text(s, "semi", 19 if bw >= 130 else 17, bx + bw / 2, cy + 7, tc, "middle"))
            if i < 2:
                ax0, ax1 = bx + bw + 8, bx + bw + gap - 8
                o.append(f'<line x1="{ax0:.1f}" y1="{cy}" x2="{ax1-10:.1f}" y2="{cy}" stroke="{fg}" stroke-width="3"/>')
                o.append(f'<polygon points="{ax1:.1f},{cy} {ax1-14:.1f},{cy-8} {ax1-14:.1f},{cy+8}" fill="{fg}"/>')
        o.append(text("Transfers blocked unless both checks pass", "reg", 17, x + w / 2, cy + 80, fg, "middle", .8))
    return o

# ---------------------------------------------------------------- pieces
def banner():
    p, W, H, X = BANNER, 1280, 320, 72
    b = [f'<rect width="{W}" height="{H}" rx="12" fill="{p["bg"]}"/>',
         text("Gustavo Martín", "semi", 60, X, 122, p["ink"]),
         text("Protocol Architect &", "reg", 27, X, 172, p["sub"]),
         text("Senior Smart Contract Engineer", "reg", 27, X, 207, p["sub"]),
         text("Solvency-first smart contract engineering for DeFi protocols.", "reg", 18, X, 262, p["mute"])]
    random.seed(7); n, v, back, liab = 60, 100.0, [], []
    for i in range(n):
        v += random.uniform(-1.2, 2.4); back.append(v)
        u = .66 + .12 * math.sin(i / 6.5) + random.uniform(-.03, .03) + .24 * math.exp(-((i - 41) / 3.0) ** 2)
        liab.append(v * min(u, .955))
    x0, x1, y0, y1 = 760, 1208, 70, 222
    lo, hi = min(liab) * .55, max(back) * 1.03
    Xf = lambda i: x0 + (x1 - x0) * i / (n - 1); Yf = lambda q: y1 - (y1 - y0) * (q - lo) / (hi - lo)
    for g in range(1, 4):
        gy = y1 - (y1 - y0) * g / 4
        b.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="{p["grid"]}"/>')
    b.append(f'<polygon points="{x0},{y1} ' + " ".join(f"{Xf(i):.1f},{Yf(q):.1f}" for i, q in enumerate(liab)) + f' {x1},{y1}" fill="{p["area"]}"/>')
    b.append(f'<polyline fill="none" stroke="{p["accent"]}" stroke-width="2.5" stroke-linejoin="round" points="'
             + " ".join(f"{Xf(i):.1f},{Yf(q):.1f}" for i, q in enumerate(back)) + '"/>')
    b.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{p["mute"]}" stroke-width="1.2"/>')
    b.append(text("backing", "reg", 14, x1, Yf(back[-1]) - 12, p["accent"], "end"))
    b.append(text("liabilities", "reg", 14, x1 - 6, y1 - 12, p["sub"], "end", .8))
    b.append(text("assert(backing >= liabilities);", "mono", 17, x0, 262, p["mute"]))
    return svg(W, H, b, "Gustavo Martín. Protocol Architect and Senior Smart Contract Engineer. "
                        "Solvency-first smart contract engineering for DeFi protocols.")

def section(key, mode):
    title, sub, col = SECTIONS[key]
    W, H = 1280, 120
    bg = mix(col, "#FFFFFF", .9) if mode == "light" else mix(col, PAGE["dark"], .72)
    fg = col if mode == "light" else mix(col, "#FFFFFF", .6)
    bar = col if mode == "light" else mix(col, "#FFFFFF", .25)
    return svg(W, H, [f'<rect width="{W}" height="{H}" rx="10" fill="{bg}"/>',
                      f'<rect width="14" height="{H}" rx="4" fill="{bar}"/>',
                      text(title, "semi", 46, 48, 76, fg),
                      text(sub, "reg", 22, W - 40, 72, TEXT_MUTE[mode], "end")], title)

def thumb(key, mode):
    name, hue = PROJECTS[key]
    c, W, H = colours(hue, mode), 640, 360
    b = [f'<rect width="{W}" height="{H}" rx="12" fill="{c["bg"]}"/>',
         f'<rect width="{W}" height="10" rx="4" fill="{c["soft"]}"/>',
         text(name, "semi", 40, 40, 82, c["fg"])]
    return svg(W, H, b + diagram(key, c, 60, 122, 520, 196), name)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    write = lambda f, s: open(os.path.join(OUT, f), "w", encoding="utf-8").write(s)
    write("banner.svg", banner())
    for mode in ("light", "dark"):
        for k in SECTIONS:
            write(f"section-{k}-{mode}.svg", section(k, mode))
        for k in PROJECTS:
            write(f"{k}-{mode}.svg", thumb(k, mode))
    print("assets written to", OUT)


# ---------------------------------------------------------------- social previews (1280x640 PNG)
SOCIAL = {  # key: (title, sentence, stats or chips, hue key or colour)
    "money-market": ("Money market", "Isolated lending market inspired by Compound III, built around provable solvency.",
                     [("331", "tests"), ("17", "stateful invariants"), (">95%", "coverage per contract")]),
    "vaults": ("ERC-4626 vaults", "Modular vaults with an atomic leveraged loop on Uniswap V4 flash loans and Aave V3 E-Mode.",
               [("365", "tests"), ("27", "stateful invariants"), ("98.6%", "line coverage")]),
    "staking": ("Real-yield staking", "A later independent rebuild of my Dexynth staking with an O(1) reward accumulator.",
                [(">96%", "less unstake gas"), (">72%", "less harvest gas"), ("O(1)", "reward accounting")]),
    "rwa-security-token": ("RWA security token", "Permissioned security token built on the ERC-3643 identity and compliance model.",
                           [("ERC-3643", "identity and compliance"), ("EIP-712", "signed attestations"), ("ERC-1643", "document anchoring")]),
    "synthetic": ("Synthetic trading", "Leveraged synthetic futures against a single-sided USDC vault.",
                  [("1", "USDC vault as counterparty"), ("3", "solvency layers"), ("Pyth", "anchored to Chainlink")]),
    "prediction-market": ("Prediction market", "Research proof of concept, built before my work at Roofcast.",
                          [("CPMM", "virtual liquidity"), ("CTF", "Gnosis custody"), ("PoC", "not production code")]),
    "security-review-reports": ("Security reviews", "Reports and findings from my smart contract security reviews.",
                                ["Vault Guardians", "Thunder Loan", "Boss Bridge", "TSwap"]),
}
SOCIAL_HUE = {"security-review-reports": "#8C2F2B"}

def wrap(txt, key, size, maxw):
    lines, cur = [], ""
    for word in txt.split():
        trial = (cur + " " + word).strip()
        if shape(trial, key, size)[1] <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur); cur = word
    return lines + [cur]

def social(key):
    title, sentence, extra = SOCIAL[key]
    hue = SOCIAL_HUE.get(key) or PROJECTS[key][1]
    c, W, H, X = colours(hue, "light"), 1280, 640, 80
    b = [f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>', f'<rect width="{W}" height="16" fill="{hue}"/>',
         text(title, "semi", 66, X, 150, hue)]
    for i, line in enumerate(wrap(sentence, "reg", 30, 640)):
        b.append(text(line, "reg", 30, X, 212 + i * 42, "#1F2328"))
    if isinstance(extra[0], tuple):
        sx = X
        for big, lab in extra:
            b.append(text(big, "semi", 46, sx, 400, hue))
            b.append(text(lab, "reg", 20, sx, 436, TEXT_MUTE["light"]))
            sx += max(shape(big, "semi", 46)[1], shape(lab, "reg", 20)[1]) + 48
    else:
        sx, sy = X, 380
        for chip in extra:
            cw = shape(chip, "semi", 22)[1] + 36
            if sx + cw > 760:
                sx, sy = X, sy + 62
            b.append(f'<rect x="{sx}" y="{sy}" width="{cw:.1f}" height="46" rx="23" fill="#FFFFFF" stroke="{hue}" stroke-width="2.5"/>')
            b.append(text(chip, "semi", 22, sx + cw / 2, sy + 31, hue, "middle"))
            sx += cw + 14
    if key in PROJECTS:
        b += diagram(key, c, 770, 140, 430, 200)
    else:  # security: shield with a check mark
        cx, top = 1010, 150
        b.append(f'<path d="M{cx},{top} L{cx+120},{top+44} L{cx+120},{top+140} C{cx+120},{top+220} {cx+60},{top+262} {cx},{top+290} '
                 f'C{cx-60},{top+262} {cx-120},{top+220} {cx-120},{top+140} L{cx-120},{top+44} Z" fill="{c["node"]}" stroke="{hue}" stroke-width="5"/>')
        b.append(f'<polyline points="{cx-52},{top+146} {cx-14},{top+186} {cx+56},{top+104}" fill="none" stroke="{hue}" '
                 f'stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(f'<line x1="{X}" y1="548" x2="{W-X}" y2="548" stroke="{hue}" stroke-opacity=".25" stroke-width="2"/>')
    b.append(text("Gustavo Martín", "semi", 24, X, 596, "#1F2328"))
    b.append(text("github.com/GushALKDev", "reg", 24, W - X, 596, TEXT_MUTE["light"], "end"))
    return svg(W, H, b, title)

def build_social(outdir):
    import cairosvg
    os.makedirs(outdir, exist_ok=True)
    for k in SOCIAL:
        cairosvg.svg2png(bytestring=social(k).encode(), write_to=os.path.join(outdir, f"{k}.png"))