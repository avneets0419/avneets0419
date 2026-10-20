#!/usr/bin/env python3
"""Generate the self-contained SVG assets used by README.md.

Usage:
    python3 scripts/generate_assets.py

Standard library only. Every asset is written to ./assets and contains no
JavaScript, remote stylesheets or web fonts, so GitHub can render it through
its image proxy. Edit the content constants below, then re-run the script.
"""

from pathlib import Path
from random import Random
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# --------------------------------------------------------------------------
# Design tokens
# --------------------------------------------------------------------------
BG0 = "#060A14"      # near-black
BG1 = "#0A1124"      # deep navy
BG2 = "#0E1631"      # raised navy
LINE = "#1E2B4D"     # hairlines
BLUE = "#36BCF7"     # electric blue (primary accent)
BLUE_SOFT = "#7DD3FC"
VIOLET = "#8B5CF6"   # secondary accent
VIOLET_SOFT = "#A78BFA"
WHITE = "#F1F5F9"
SLATE = "#94A3B8"
DIM = "#64748B"

SANS = ("'Inter','SF Pro Display',-apple-system,BlinkMacSystemFont,'Segoe UI',"
        "Roboto,'Helvetica Neue',Arial,sans-serif")
MONO = ("ui-monospace,'SF Mono','JetBrains Mono','Cascadia Code',Menlo,Consolas,"
        "'Liberation Mono',monospace")
MONO_ADVANCE = 0.6   # width of one monospace glyph, as a fraction of font size

REDUCED_MOTION = ("@media (prefers-reduced-motion: reduce){*{animation:none!important;"
                  "transition:none!important}}")

# --------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------
NAME = "Avneet Singh"
TAGLINE = ["Full-Stack Engineer", "AI Systems", "Product Builder"]
TERMINAL = [  # (command, output) pairs shown in the hero's terminal panel
    ("now", "FDE Intern @ Paramount"),
    ("building", "zuplin.in"),
    ("exploring", "agents · rag · automation"),
]
TYPING_LINES = [
    "Full-Stack Developer",
    "AI Agent Builder",
    "Building Zuplin",
    "Exploring RAG and Intelligent Automation",
]


def svg_doc(width, height, body, title, style="", desc=""):
    style_block = f"<style>{style}</style>" if style else ""
    desc_block = f"<desc>{escape(desc)}</desc>" if desc else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="t">'
        f'<title id="t">{escape(title)}</title>{desc_block}{style_block}{body}</svg>\n'
    )


def write(name, content):
    path = ASSETS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  {path.relative_to(ROOT)}  ({len(content.encode()) / 1024:.1f} KiB)")


def card_frame(w, h, uid, rx=16):
    """Shared background: navy gradient, soft corner glows, hairline border."""
    defs = (
        f'<linearGradient id="{uid}bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{BG1}"/><stop offset=".55" stop-color="{BG0}"/>'
        f'<stop offset="1" stop-color="#0B0F24"/></linearGradient>'
        f'<radialGradient id="{uid}gb"><stop offset="0" stop-color="{BLUE}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="{uid}gv"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="{uid}edge" x1="0" x2="1">'
        f'<stop offset="0" stop-color="{BLUE}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{BLUE}" stop-opacity=".55"/>'
        f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="{uid}clip"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>'
        f'<pattern id="{uid}grid" width="28" height="28" patternUnits="userSpaceOnUse">'
        f'<path d="M28 0H0V28" fill="none" stroke="{SLATE}" stroke-opacity=".07"/></pattern>'
    )
    background = f'<rect width="{w}" height="{h}" fill="url(#{uid}bg)"/>'
    border = (
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx - .5}" fill="none" '
        f'stroke="{SLATE}" stroke-opacity=".16"/>'
        f'<rect x="{w * .12:.0f}" y="0" width="{w * .76:.0f}" height="1" fill="url(#{uid}edge)"/>'
    )
    return defs, background, border


# --------------------------------------------------------------------------
# Hero banner
# --------------------------------------------------------------------------
def hero(animated=True):
    w, h = 1000, 260
    defs, background, border = card_frame(w, h, "h", rx=18)
    rnd = Random(419)

    defs += (
        f'<radialGradient id="hfade" cx=".72" cy=".5" r=".55">'
        f'<stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>'
        f'<mask id="hgridmask"><rect width="{w}" height="{h}" fill="url(#hfade)"/></mask>'
        f'<linearGradient id="hname" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#C9D6F2"/></linearGradient>'
        f'<linearGradient id="hshine" gradientUnits="userSpaceOnUse" '
        f'x1="-260" x2="0" y1="0" y2="0">'
        f'<stop offset="0" stop-color="{BLUE_SOFT}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{BLUE_SOFT}" stop-opacity=".75"/>'
        f'<stop offset="1" stop-color="{BLUE_SOFT}" stop-opacity="0"/>'
        + ('<animateTransform attributeName="gradientTransform" type="translate" '
           'values="0 0;760 0;760 0" keyTimes="0;.3;1" dur="9s" begin="1.6s" '
           'repeatCount="indefinite"/>' if animated else "")
        + '</linearGradient>'
        f'<linearGradient id="haccent" x1="0" x2="1">'
        f'<stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'
    )
    glows = (
        f'<g class="drift-a"><ellipse cx="150" cy="30" rx="330" ry="210" fill="url(#hgb)"/></g>'
        f'<g class="drift-b"><ellipse cx="880" cy="250" rx="360" ry="220" fill="url(#hgv)"/></g>'
    )
    grid = (
        f'<g mask="url(#hgridmask)"><g class="grid">'
        f'<rect x="-28" y="-28" width="{w + 56}" height="{h + 56}" fill="url(#hgrid)"/></g></g>'
    )

    particles = []
    while len(particles) < 26:
        x, y = rnd.uniform(16, w - 16), rnd.uniform(24, h - 8)
        if 40 < x < 600 and y > 80:   # keep the name and tagline clean (particles rise)
            continue
        if 630 < x < 950 and y > 40:  # and the terminal panel
            continue
        r = rnd.choice([0.8, 1, 1.2, 1.5, 1.8])
        fill = rnd.choice([BLUE, BLUE, BLUE_SOFT, VIOLET_SOFT, WHITE])
        dur = rnd.uniform(7, 15)
        delay = -rnd.uniform(0, dur)
        particles.append(
            f'<circle class="p" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" '
            f'style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s"/>'
        )

    # Left column: terminal chip, name, accent rule, tagline
    chip = (
        f'<g transform="translate(64 56)">'
        f'<rect width="176" height="28" rx="8" fill="{BG2}" fill-opacity=".85" stroke="{LINE}"/>'
        f'<circle cx="14" cy="14" r="3.5" fill="#334155"/><circle cx="26" cy="14" r="3.5" fill="#334155"/>'
        f'<circle cx="38" cy="14" r="3.5" fill="#334155"/>'
        f'<text x="52" y="18.5" font-family="{MONO}" font-size="12.5" fill="{SLATE}">~/avneets0419</text>'
        f'</g>'
    )
    name = (
        f'<text x="61" y="150" font-family="{SANS}" font-size="60" font-weight="700" '
        f'letter-spacing="-1.6" fill="url(#hname)">{escape(NAME)}</text>'
        f'<text x="61" y="150" font-family="{SANS}" font-size="60" font-weight="700" '
        f'letter-spacing="-1.6" fill="url(#hshine)" aria-hidden="true">{escape(NAME)}</text>'
    )
    accent = f'<rect x="64" y="167" width="72" height="3" rx="1.5" fill="url(#haccent)"/>'
    sep = f'<tspan fill="{BLUE}">  |  </tspan>'
    tagline = (
        f'<text x="64" y="204" font-family="{MONO}" font-size="16" fill="{SLATE}" '
        f'xml:space="preserve">' + sep.join(escape(t) for t in TAGLINE) + '</text>'
    )

    # Right column: terminal panel
    px, py, pw, ph = 640, 48, 300, 164
    lines = []
    y = py + 50
    for i, (cmd, out) in enumerate(TERMINAL):
        delay = 0.35 + i * 0.45
        lines.append(
            f'<text class="ln" style="animation-delay:{delay:.2f}s" x="{px + 20}" y="{y}" '
            f'font-family="{MONO}" font-size="13"><tspan fill="{BLUE}">$</tspan>'
            f'<tspan fill="{WHITE}" dx="8">{escape(cmd)}</tspan></text>'
        )
        y += 20
        out_x = px + 36
        if cmd == "building":  # live-status dot beside the product name
            lines.append(
                f'<g class="ln" style="animation-delay:{delay + .2:.2f}s">'
                f'<circle class="pulse" cx="{out_x + 4}" cy="{y - 4.5}" r="6" fill="{BLUE}" fill-opacity=".25"/>'
                f'<circle cx="{out_x + 4}" cy="{y - 4.5}" r="3" fill="{BLUE}"/></g>'
            )
            out_x += 16
        lines.append(
            f'<text class="ln" style="animation-delay:{delay + .2:.2f}s" x="{out_x}" y="{y}" '
            f'font-family="{MONO}" font-size="13" fill="{SLATE}">{escape(out)}</text>'
        )
        y += 22
    last_len = len(TERMINAL[-1][1])
    caret_x = px + 36 + last_len * 13 * MONO_ADVANCE + 4
    panel = (
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="{BG2}" '
        f'fill-opacity=".78" stroke="{LINE}"/>'
        f'<path d="M{px} {py + 28}H{px + pw}" stroke="{LINE}"/>'
        f'<circle cx="{px + 16}" cy="{py + 14}" r="4" fill="#F87171" fill-opacity=".75"/>'
        f'<circle cx="{px + 30}" cy="{py + 14}" r="4" fill="#FBBF24" fill-opacity=".75"/>'
        f'<circle cx="{px + 44}" cy="{py + 14}" r="4" fill="#34D399" fill-opacity=".75"/>'
        f'<text x="{px + pw / 2}" y="{py + 18}" text-anchor="middle" font-family="{MONO}" '
        f'font-size="11" fill="{DIM}">zsh — avneet</text>'
        + "".join(lines)
        + f'<rect class="caret" x="{caret_x:.1f}" y="{y - 37}" width="7" height="15" rx="1" '
          f'fill="{BLUE}" fill-opacity=".9"/>'
    )

    style = ""
    if animated:
        style = (
            "@keyframes da{to{transform:translate(46px,22px)}}"
            "@keyframes db{to{transform:translate(-52px,-18px)}}"
            "@keyframes gr{to{transform:translate(28px,28px)}}"
            "@keyframes rise{0%{transform:translateY(0);opacity:0}20%{opacity:.85}"
            "80%{opacity:.5}100%{transform:translateY(-64px);opacity:0}}"
            "@keyframes in{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}"
            "@keyframes blink{50%{opacity:0}}"
            "@keyframes pulse{0%{transform:scale(.6);opacity:.9}100%{transform:scale(1.8);opacity:0}}"
            ".drift-a{animation:da 16s ease-in-out infinite alternate}"
            ".drift-b{animation:db 19s ease-in-out infinite alternate}"
            ".grid{animation:gr 12s linear infinite}"
            ".p{opacity:.45;animation:rise 10s linear infinite}"
            ".ln{animation:in .6s ease-out both}"
            ".caret{animation:blink 1.1s steps(1) infinite}"
            ".pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}"
            + REDUCED_MOTION
        )
    else:
        style = ".p{opacity:.45}"

    body = (
        f"<defs>{defs}</defs>"
        f'<g clip-path="url(#hclip)">{background}{glows}{grid}{"".join(particles)}'
        f"{chip}{name}{accent}{tagline}{panel}</g>{border}"
    )
    return svg_doc(
        w, h, body,
        title=f"{NAME} — {' | '.join(TAGLINE)}",
        desc="Dark navy banner with the name Avneet Singh, the tagline Full-Stack Engineer, "
             "AI Systems, Product Builder, and a terminal panel listing current role "
             "(FDE Intern at Paramount), current product (zuplin.in) and focus "
             "(agents, RAG, automation).",
        style=style,
    )


# --------------------------------------------------------------------------
# Typing line (SMIL, so every phrase stays in sync on one timeline)
# --------------------------------------------------------------------------
TYPE_STEP, HOLD, DELETE_STEP, GAP = 0.065, 1.9, 0.024, 0.35


def typing(animated=True):
    # Compact panel: the README caps it at 720px wide, so on a phone it scales far less
    # than the 1000px hero and the phrase stays legible.
    w, h = 600, 56
    defs, background, border = card_frame(w, h, "y", rx=14)
    fs = 20
    cw = fs * MONO_ADVANCE
    x_prompt = 26
    x0 = x_prompt + 24
    baseline = 35

    if not animated:
        half = len(TYPING_LINES) // 2
        rows = ["  ·  ".join(TYPING_LINES[:half]), "  ·  ".join(TYPING_LINES[half:])]
        text = "".join(
            f'<text x="{w / 2}" y="{24 + i * 18}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="13.5" fill="{WHITE if i == 0 else SLATE}" xml:space="preserve">'
            f"{escape(row)}</text>"
            for i, row in enumerate(rows)
        )
        body = (f"<defs>{defs}</defs><g clip-path=\"url(#yclip)\">{background}{text}</g>{border}")
        return svg_doc(w, h, body, title=" · ".join(TYPING_LINES))

    # Build a shared timeline: each phrase types in, holds, deletes, then hands over.
    slots, t = [], 0.0
    for line in TYPING_LINES:
        n = len(line)
        events = [(t + k * TYPE_STEP, k) for k in range(n + 1)]
        start_delete = t + n * TYPE_STEP + HOLD
        events += [(start_delete + j * DELETE_STEP, n - 1 - j) for j in range(n)]
        slots.append(events)
        t = start_delete + n * DELETE_STEP + GAP
    total = t

    def smil(events, to_value):
        merged = {}
        for time, chars in [(0.0, 0)] + events:
            merged[round(time / total, 4)] = to_value(chars)
        keys = sorted(merged)
        return (";".join(f"{merged[k]:.1f}" for k in keys),
                ";".join(f"{k:.4f}".rstrip("0").rstrip(".") or "0" for k in keys))

    clip_defs, texts = [], []
    for i, (line, events) in enumerate(zip(TYPING_LINES, slots)):
        values, key_times = smil(events, lambda k: k * cw)
        static_w = len(line) * cw if i == 0 else 0
        clip_defs.append(
            f'<clipPath id="yc{i}"><rect x="{x0 - 1}" y="8" width="{static_w:.1f}" height="40">'
            f'<animate attributeName="width" values="{values}" keyTimes="{key_times}" '
            f'dur="{total:.3f}s" calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>'
        )
        texts.append(
            f'<text clip-path="url(#yc{i})" x="{x0}" y="{baseline}" font-family="{MONO}" '
            f'font-size="{fs}" fill="{WHITE}" textLength="{len(line) * cw:.1f}" '
            f'lengthAdjust="spacingAndGlyphs">{escape(line)}</text>'
        )

    caret_events = sorted(e for events in slots for e in events)
    caret_values, caret_times = smil(caret_events, lambda k: x0 + k * cw + 2)
    caret = (
        f'<rect class="caret" x="{x0 + len(TYPING_LINES[0]) * cw + 2:.1f}" y="{baseline - 17}" '
        f'width="2.5" height="23" rx="1" fill="{BLUE}">'
        f'<animate attributeName="x" values="{caret_values}" keyTimes="{caret_times}" '
        f'dur="{total:.3f}s" calcMode="discrete" repeatCount="indefinite"/></rect>'
    )
    prompt = (
        f'<text x="{x_prompt}" y="{baseline}" font-family="{MONO}" font-size="{fs}" '
        f'fill="{BLUE}">$</text>'
    )
    defs += "".join(clip_defs)
    defs += (
        f'<linearGradient id="yfade" x1="0" x2="1"><stop offset=".55" stop-color="#000"/>'
        f'<stop offset="1" stop-color="#fff" stop-opacity=".9"/></linearGradient>'
        f'<mask id="ymask"><rect width="{w}" height="{h}" fill="url(#yfade)"/></mask>'
    )
    deco = f'<rect width="{w}" height="{h}" fill="url(#ygrid)" mask="url(#ymask)"/>'
    style = "@keyframes blink{50%{opacity:0}}.caret{animation:blink 1s steps(1) infinite}" + REDUCED_MOTION
    body = (
        f"<defs>{defs}</defs><g clip-path=\"url(#yclip)\">{background}{deco}{prompt}"
        f"{''.join(texts)}{caret}</g>{border}"
    )
    return svg_doc(w, h, body, style=style, title=" · ".join(TYPING_LINES))


# --------------------------------------------------------------------------
# Section divider
# --------------------------------------------------------------------------
def divider():
    w, h = 1000, 24
    cy = h / 2
    body = (
        f'<defs><linearGradient id="dl" x1="0" x2="1">'
        f'<stop offset="0" stop-color="{BLUE}" stop-opacity="0"/>'
        f'<stop offset=".32" stop-color="{BLUE}" stop-opacity=".55"/>'
        f'<stop offset=".5" stop-color="{VIOLET_SOFT}" stop-opacity=".8"/>'
        f'<stop offset=".68" stop-color="{BLUE}" stop-opacity=".55"/>'
        f'<stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>'
        f'<linearGradient id="dp" x1="0" x2="1">'
        f'<stop offset="0" stop-color="{BLUE_SOFT}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{BLUE_SOFT}"/>'
        f'<stop offset="1" stop-color="{BLUE_SOFT}" stop-opacity="0"/></linearGradient>'
        f'<radialGradient id="dg"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".45"/>'
        f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient></defs>'
        f'<rect x="0" y="{cy - .5}" width="{w}" height="1" fill="url(#dl)"/>'
        f'<rect class="pulse" x="-140" y="{cy - .75}" width="140" height="1.5" fill="url(#dp)"/>'
        f'<circle cx="{w / 2}" cy="{cy}" r="11" fill="url(#dg)"/>'
        f'<rect x="{w / 2 - 3.5}" y="{cy - 3.5}" width="7" height="7" fill="{VIOLET_SOFT}" '
        f'transform="rotate(45 {w / 2} {cy})"/>'
    )
    style = ("@keyframes run{0%{transform:translateX(0);opacity:0}10%{opacity:1}"
             "90%{opacity:1}100%{transform:translateX(1140px);opacity:0}}"
             ".pulse{animation:run 6s cubic-bezier(.45,0,.55,1) infinite}" + REDUCED_MOTION)
    return svg_doc(w, h, body, title="Section divider", style=style)


# --------------------------------------------------------------------------
# Link buttons
# --------------------------------------------------------------------------
GITHUB_PATH = (
    "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 "
    "0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 "
    "17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 "
    "1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 "
    "1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 "
    "3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 "
    "3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 "
    "1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627"
    "-5.373-12-12-12"
)
LINKS = {
    "github": ("GitHub", f'<path d="{GITHUB_PATH}" fill="{WHITE}"/>'),
    "website": ("zuplin.in",
                f'<g fill="none" stroke="{BLUE}" stroke-width="1.8">'
                f'<circle cx="12" cy="12" r="10"/><ellipse cx="12" cy="12" rx="4.2" ry="10"/>'
                f'<path d="M2 12h20M4 6.5h16M4 17.5h16"/></g>'),
    "email": ("Email",
              f'<g fill="none" stroke="{VIOLET_SOFT}" stroke-width="1.8" stroke-linejoin="round">'
              f'<rect x="2" y="4.5" width="20" height="15" rx="2.5"/><path d="m3 6 9 7 9-7"/></g>'),
}


def link_button(key):
    label, icon = LINKS[key]
    fs = 13
    w = round(16 + 16 + 9 + len(label) * fs * MONO_ADVANCE + 18)
    h = 36
    body = (
        f'<defs><linearGradient id="b" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG0}"/></linearGradient></defs>'
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="10" fill="url(#b)" '
        f'stroke="{SLATE}" stroke-opacity=".22"/>'
        f'<g transform="translate(16 10) scale(.6667)">{icon}</g>'
        f'<text x="41" y="22.5" font-family="{MONO}" font-size="{fs}" fill="{WHITE}">{escape(label)}</text>'
    )
    return svg_doc(w, h, body, title=label)


# --------------------------------------------------------------------------
# Project cards: a small, factual diagram of each repository's pipeline
# --------------------------------------------------------------------------
NODE_STYLES = {
    "base": (BG2, "#24365F", "#CBD5E1"),
    "blue": ("#0B2340", BLUE, "#E0F2FE"),
    "violet": ("#1B1536", VIOLET, "#EDE9FE"),
}


def node(x, cy, w, label, kind="base", h=26, dashed=False):
    fill, stroke, text = NODE_STYLES[kind]
    dash = ' stroke-dasharray="4 3"' if dashed else ""
    return (
        f'<rect x="{x}" y="{cy - h / 2}" width="{w}" height="{h}" rx="7" fill="{fill}" '
        f'stroke="{stroke}" stroke-opacity=".9"{dash}/>'
        f'<text x="{x + w / 2}" y="{cy + 4}" text-anchor="middle" font-family="{MONO}" '
        f'font-size="12" fill="{text}">{escape(label)}</text>'
    )


def edge(d, color="#3A4F7E", dashed=False, arrow=True):
    dash = ' stroke-dasharray="4 3"' if dashed else ""
    marker = ' marker-end="url(#arrow)"' if arrow else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.4"{dash}{marker}/>'


def chain(xs, cy, w, labels, kinds=None):
    """Nodes left to right on one row, joined by arrows."""
    kinds = kinds or ["base"] * len(labels)
    out = [node(x, cy, w, lab, k) for x, lab, k in zip(xs, labels, kinds)]
    out += [edge(f"M{a + w + 2} {cy}H{b - 4}") for a, b in zip(xs, xs[1:])]
    return out


def project_card(index, tag, caption, parts, pulse_path):
    w, h = 440, 160
    defs, background, border = card_frame(w, h, "c", rx=14)
    defs += (
        '<marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6.5" markerHeight="6.5" '
        'markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0 0L8 4L0 8z" fill="#4A6196"/></marker>'
        f'<radialGradient id="pg"><stop offset="0" stop-color="{BLUE_SOFT}" stop-opacity=".7"/>'
        f'<stop offset="1" stop-color="{BLUE_SOFT}" stop-opacity="0"/></radialGradient>'
    )
    glow = (
        f'<ellipse cx="40" cy="0" rx="200" ry="110" fill="url(#cgb)"/>'
        f'<ellipse cx="430" cy="170" rx="220" ry="120" fill="url(#cgv)"/>'
        f'<rect width="{w}" height="{h}" fill="url(#cgrid)" opacity=".8"/>'
    )
    header = (
        f'<text x="20" y="28" font-family="{MONO}" font-size="10.5" letter-spacing="1.6" '
        f'fill="{BLUE}">{escape(tag)}</text>'
        f'<text x="{w - 20}" y="28" text-anchor="end" font-family="{MONO}" font-size="11" '
        f'fill="{DIM}">{index}</text>'
        f'<path d="M20 40H{w - 20}" stroke="{LINE}"/>'
    )
    # A data pulse travels along the main path, behind the nodes.
    pulse = (
        f'<g opacity="0"><set attributeName="opacity" to="1" begin="0s" fill="freeze"/>'
        f'<circle r="7" fill="url(#pg)"/><circle r="2.4" fill="{BLUE_SOFT}"/>'
        f'<animateMotion path="{pulse_path}" dur="4.2s" repeatCount="indefinite" '
        f'calcMode="paced"/></g>'
    )
    foot = (
        f'<text x="20" y="{h - 14}" font-family="{MONO}" font-size="10.5" fill="{DIM}">'
        f'{escape(caption)}</text>'
    )
    body = (
        f"<defs>{defs}</defs><g clip-path=\"url(#cclip)\">{background}{glow}{header}"
        f"{pulse}{''.join(parts)}{foot}</g>{border}"
    )
    return body, w, h


def projects():
    cards = {}

    # 01 · AI-CRM — LangGraph: score → route → draft → explain → human approval gate
    xs, cy = [20, 103, 186, 269, 352], 88
    parts = chain(xs[:4], cy, 66, ["score", "route", "draft", "explain"], ["base"] * 3 + ["blue"])
    parts.append(node(352, cy, 68, "approve", "violet"))
    parts.append(edge(f"M337 {cy}H348", color=VIOLET, dashed=True))
    parts.append(f'<text x="386" y="{cy + 31}" text-anchor="middle" font-family="{MONO}" '
                 f'font-size="10" fill="{VIOLET_SOFT}">human gate</text>')
    cards["ai-crm"] = ("01", "HUMAN-IN-THE-LOOP AGENTS",
                       "// langgraph interrupt · nothing sends without sign-off",
                       parts, f"M20 {cy}H420", "AI-CRM agent pipeline: score, route, draft and "
                       "explain nodes feed a human approval gate.")

    # 02 · Self-Correcting RAG — retrieve → grade → generate → verify, with rewrite and web loops
    top, bot = 70, 114
    parts = chain([20, 124, 228, 332], top, 84, ["retrieve", "grade", "generate", "verify"],
                  ["base", "blue", "base", "violet"])
    parts += [
        node(72, bot, 84, "rewrite"),
        node(176, bot, 84, "web search"),
        edge(f"M150 {top + 13}L128 {bot - 15}", dashed=True),
        edge(f"M90 {bot - 13}L74 {top + 15}", dashed=True),
        edge(f"M184 {top + 13}L204 {bot - 15}", dashed=True),
        edge(f"M244 {bot - 13}L262 {top + 15}", dashed=True),
        # verify → generate: regenerate when the answer is not grounded
        edge(f"M374 {top - 13}C374 {top - 26} 270 {top - 26} 270 {top - 16}", color=VIOLET,
             dashed=True),
    ]
    cards["self-correcting-rag-agent"] = (
        "02", "CORRECTIVE RAG", "// faiss retrieval · tavily fallback · grounding check",
        parts, f"M20 {top}H416",
        "Self-correcting RAG graph: retrieve, grade, generate and verify, with a query-rewrite "
        "loop, a web-search fallback and regeneration when an answer is not grounded.")

    # 03 · Self-optimizing ad agent — variants → z-test → scale / rewrite, under guardrails
    mid, up, down = 86, 64, 108
    parts = [
        node(20, mid, 86, "variants"),
        node(128, mid, 86, "a/b z-test", "blue"),
        node(236, up, 76, "scale"),
        node(236, down, 76, "rewrite"),
        edge(f"M108 {mid}H124"),
        edge(f"M216 {mid - 6}L232 {up + 6}"),
        edge(f"M216 {mid + 6}L232 {down - 6}"),
        edge(f"M236 {down + 9}C200 {down + 26} 176 {down + 18} 171 {mid + 17}", dashed=True),
        f'<rect x="334" y="{up - 14}" width="86" height="{down - up + 28}" rx="8" fill="#140F2B" '
        f'stroke="{VIOLET}" stroke-opacity=".8" stroke-dasharray="4 3"/>',
        f'<text x="377" y="{up + 1}" text-anchor="middle" font-family="{MONO}" font-size="10.5" '
        f'fill="{VIOLET_SOFT}">guardrails</text>',
    ]
    for i, item in enumerate(["budget cap", "pacing", "stop-loss"]):
        parts.append(f'<text x="377" y="{up + 21 + i * 15}" text-anchor="middle" '
                     f'font-family="{MONO}" font-size="10.5" fill="#CBD5E1">{item}</text>')
    cards["self-optimizing-ad-agent"] = (
        "03", "AUTONOMOUS AD OPTIMIZATION", "// min CPA subject to target ROAS and budget",
        parts, f"M20 {mid}H236L274 {up}",
        "Ad agent loop: generated variants go through an A/B z-test, winners scale and losers "
        "are rewritten, all inside budget, pacing and stop-loss guardrails.")

    # 04 · News credibility — claim → agent → three evidence tools → verdict
    mid = 88
    tools = [(58, "liar rag"), (88, "newsapi"), (118, "web search")]
    parts = [node(20, mid, 70, "claim"), node(110, mid, 76, "agent", "blue"),
             node(338, mid, 82, "verdict", "violet"), edge(f"M92 {mid}H106")]
    for cy, label in tools:
        parts.append(node(212, cy, 96, label))
        parts.append(edge(f"M188 {mid}C198 {mid} 198 {cy} 208 {cy}"))
        parts.append(edge(f"M310 {cy}C322 {cy} 322 {mid} 334 {mid}"))
    cards["news-credibility-model"] = (
        "04", "AGENTIC FACT-CHECKING", "// langgraph react agent · llama 3.3 70b · sse stream",
        parts, f"M20 {mid}H190C200 {mid} 200 {tools[0][0]} 212 {tools[0][0]}H308"
               f"C322 {tools[0][0]} 322 {mid} 338 {mid}H420",
        "News credibility pipeline: a claim goes to a ReAct agent that gathers evidence from "
        "a LIAR-dataset RAG index, NewsAPI and web search before returning a verdict.")

    # 05 · Atlas — mood → swipe → itinerary → map
    xs = [20, 126, 232, 338]
    parts = chain(xs, 90, 82, ["mood", "swipe", "itinerary", "map"],
                  ["base", "blue", "base", "violet"])
    cards["atlas"] = (
        "05", "REACT NATIVE · EXPO", "// reanimated gestures · zustand · simulated itineraries",
        parts, "M20 90H420",
        "Atlas app flow: choose a travel mood, swipe destinations, view a day-by-day "
        "itinerary, then see it on a map.")

    # 06 · Ai-Meeting (MeetWise) — upload → transcribe → summarize → tasks
    parts = chain(xs, 90, 82, ["upload", "transcribe", "summarize", "tasks"],
                  ["base", "blue", "base", "violet"])
    cards["ai-meeting"] = (
        "06", "AI MEETING ASSISTANT", "// assemblyai transcripts → action items on a kanban",
        parts, "M20 90H420",
        "MeetWise flow: upload a recording, transcribe it, summarize it, and extract tasks.")

    for slug, (index, tag, caption, parts, pulse_path, alt) in cards.items():
        body, w, h = project_card(index, tag, caption, parts, pulse_path)
        write(f"projects/{slug}.svg", svg_doc(w, h, body, title=alt))


def main():
    print("Generating assets:")
    write("hero/profile-hero.svg", hero(animated=True))
    write("hero/profile-hero-static.svg", hero(animated=False))
    write("hero/typing.svg", typing(animated=True))
    write("hero/typing-static.svg", typing(animated=False))
    write("ui/divider.svg", divider())
    for key in LINKS:
        write(f"ui/link-{key}.svg", link_button(key))
    projects()


if __name__ == "__main__":
    main()
