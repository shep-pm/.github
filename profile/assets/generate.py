#!/usr/bin/env python3
"""Draw the two artworks on the org profile page, once per colour theme.

An SVG loaded through an <img> tag gets no network and no page context: it
cannot read prefers-color-scheme for itself and it cannot load a web font.
That leaves two consequences this file is built around.

  * One drawing has to ship as two files, and <picture> picks between them.
    The colours live in LIGHT and DARK below and nothing else differs, so the
    pair cannot drift.
  * Every label falls back to whatever system family the reader has. Anything
    inside a box is monospace with an explicit textLength, so a wide fallback
    cannot push text past the border it sits in.

Run it from anywhere:  python3 profile/assets/generate.py
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent

# Both palettes are the docs site's own tokens, from web/src/styles/tokens.css
# in shep-pm/shep. The landing page is the source of truth for shep's colour,
# and a second set invented here would be a second source of truth.
LIGHT = {
    "sky_top": "#a8dcf5",
    "sky_bottom": "#e9f5e0",
    "sun": "#f3c44c",
    "sun_glow": "#f7d97e",
    "cloud": "#fffdf5",
    "hill_back": "#8ed9a0",
    "hill_front": "#6fcb6b",
    "hill_fore": "#55b45c",
    "fence": "#b8864a",
    "fleece": "#fffdf5",
    "outline": "#17251c",
    "ink": "#17251c",
    "ink_2": "#3d5245",
    "ink_3": "#7a8c80",
    "accent": "#e0552b",
    "butter": "#f3c44c",
    "paper": "#fbf6e7",
    "surface": "#fffdf5",
    "hairline": "#17251c",
    "wire": "#3d5245",
    "star": "#fffdf5",
    "star_opacity": "0",
    "glow_opacity": ".30",
    "glow_peak": ".46",
}

DARK = {
    "sky_top": "#0b1a2b",
    "sky_bottom": "#131e18",
    "sun": "#f6d072",
    "sun_glow": "#f6d072",
    "cloud": "#1e2c36",
    "hill_back": "#163527",
    "hill_front": "#1f4a33",
    "hill_fore": "#2a7444",
    "fence": "#6b5231",
    "fleece": "#f0ecdc",
    "outline": "#0b1410",
    "ink": "#f0ecdc",
    "ink_2": "#bfcfc2",
    "ink_3": "#7e9186",
    "accent": "#ff7b4f",
    "butter": "#f6d072",
    "paper": "#131e18",
    "surface": "#1b2a21",
    "hairline": "#35493c",
    "wire": "#7e9186",
    "star": "#f0ecdc",
    "star_opacity": "1",
    "glow_opacity": ".14",
    "glow_peak": ".24",
}

# Every monospace label is pinned to this ratio of its font size per character.
# SF Mono, Consolas and DejaVu Sans Mono sit between 0.55 and 0.61, so a pin at
# 0.6 asks each of them for a width it can reach without visible stretching.
MONO_RATIO = 0.6
MONO_STACK = "ui-monospace,'SF Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS_STACK = "system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"


def escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def mono(x, y, size, text, fill, anchor="start", weight="400", opacity=None):
    """A monospace label whose rendered width is pinned, not hoped for."""
    length = round(MONO_RATIO * size * len(text), 1)
    fade = f' opacity="{opacity}"' if opacity is not None else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{MONO_STACK}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
        f'textLength="{length}" lengthAdjust="spacingAndGlyphs"{fade}>'
        f"{escape(text)}</text>"
    )


def sans(x, y, size, text, fill, anchor="start", weight="400", length=None):
    """A proportional label. Pinned only where an overflow would collide."""
    pin = (
        f' textLength="{length}" lengthAdjust="spacingAndGlyphs"'
        if length is not None
        else ""
    )
    return (
        f'<text x="{x}" y="{y}" font-family="{SANS_STACK}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{pin}>'
        f"{escape(text)}</text>"
    )


def sheep(x, y, scale, palette, delay):
    """The favicon's own mark, from web/public/favicon.svg in shep-pm/shep.

    Its viewBox is 104x78 and the legs run to y=73, so the caller places the
    top-left corner and the feet land at y + 73 * scale.

    Two nested groups, and the nesting is load-bearing. An animated CSS
    transform REPLACES the transform presentation attribute rather than
    composing with it, so putting the bob on this same element throws away the
    translate and the scale: every sheep renders full size at the origin, on
    top of every other sheep. Placement goes on the outer group, motion on the
    inner one.
    """
    return f"""<g transform="translate({x},{y}) scale({scale})"><g class="sheep" style="animation-delay:{delay}s">
    <g fill="{palette['outline']}"><rect x="40" y="52" width="8" height="21" rx="4"/><rect x="66" y="52" width="8" height="21" rx="4"/></g>
    <path d="M40 20c6-9 22-10 28-2 10-3 19 4 18 13 7 4 7 15-1 19-2 8-12 11-19 8-8 5-21 4-26-3-10 1-17-7-15-16-4-8 4-18 15-19Z" fill="{palette['fleece']}" stroke="{palette['outline']}" stroke-width="4" stroke-linejoin="round"/>
    <ellipse cx="26" cy="34" rx="9" ry="7" transform="rotate(-28 26 34)" fill="{palette['outline']}"/>
    <ellipse cx="27" cy="48" rx="15" ry="14" fill="{palette['outline']}"/>
    <circle cx="22" cy="45" r="3" fill="{palette['fleece']}"/>
    <circle cx="21.4" cy="45.6" r="1.4" fill="{palette['outline']}"/>
  </g></g>"""


# --------------------------------------------------------------------------
# The banner
# --------------------------------------------------------------------------

BANNER_W, BANNER_H = 880, 300


def banner(palette: dict) -> str:
    stars = ""
    if palette["star_opacity"] != "0":
        seeds = [
            (92, 44, 1.5, 0.0), (168, 28, 1.1, 1.3), (243, 62, 1.4, 2.6),
            (318, 36, 1.0, 0.7), (402, 22, 1.5, 3.1), (486, 54, 1.2, 1.9),
            (566, 30, 1.3, 0.4), (648, 58, 1.0, 2.2), (712, 26, 1.4, 1.1),
            (798, 48, 1.2, 2.9), (846, 18, 1.1, 0.9), (58, 76, 1.0, 3.4),
        ]
        stars = "\n  ".join(
            f'<circle class="star" cx="{cx}" cy="{cy}" r="{r}" '
            f'fill="{palette["star"]}" style="animation-delay:{d}s"/>'
            for cx, cy, r, d in seeds
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BANNER_W} {BANNER_H}" width="{BANNER_W}" height="{BANNER_H}" role="img" aria-label="shep: a process manager written in Rust. Three sheep graze on a hillside under a low sun.">
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{palette['sky_top']}"/>
    <stop offset="1" stop-color="{palette['sky_bottom']}"/>
  </linearGradient>
  <radialGradient id="glow">
    <stop offset="0" stop-color="{palette['sun_glow']}" stop-opacity="1"/>
    <stop offset="1" stop-color="{palette['sun_glow']}" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="frame"><rect width="{BANNER_W}" height="{BANNER_H}" rx="14"/></clipPath>
</defs>
<style>
  .sheep {{ animation: bob 3.6s ease-in-out infinite; }}
  @keyframes bob {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-3.5px); }} }}
  .cloud {{ animation: drift 74s linear infinite; }}
  @keyframes drift {{ from {{ transform: translateX(-260px); }} to {{ transform: translateX({BANNER_W + 260}px); }} }}
  .glow {{ animation: breathe 7s ease-in-out infinite; transform-origin: 754px 74px; }}
  @keyframes breathe {{ 0%, 100% {{ opacity: {palette['glow_opacity']}; transform: scale(1); }} 50% {{ opacity: {palette['glow_peak']}; transform: scale(1.07); }} }}
  .star {{ animation: twinkle 4.2s ease-in-out infinite; }}
  @keyframes twinkle {{ 0%, 100% {{ opacity: .25; }} 50% {{ opacity: .95; }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<g clip-path="url(#frame)">
  <rect width="{BANNER_W}" height="{BANNER_H}" fill="url(#sky)"/>
  {stars}
  <circle class="glow" cx="754" cy="74" r="84" fill="url(#glow)" opacity="{palette['glow_opacity']}"/>
  <circle cx="754" cy="74" r="30" fill="{palette['sun']}"/>

  <g class="cloud" opacity=".9">
    <ellipse cx="120" cy="58" rx="34" ry="15" fill="{palette['cloud']}"/>
    <ellipse cx="148" cy="50" rx="26" ry="18" fill="{palette['cloud']}"/>
    <ellipse cx="90" cy="52" rx="20" ry="13" fill="{palette['cloud']}"/>
  </g>
  <g class="cloud" opacity=".65" style="animation-delay:-41s;animation-duration:96s">
    <ellipse cx="400" cy="96" rx="28" ry="12" fill="{palette['cloud']}"/>
    <ellipse cx="422" cy="90" rx="20" ry="14" fill="{palette['cloud']}"/>
  </g>

  <path d="M0 228 C 120 190, 232 224, 348 210 C 470 196, 566 230, 688 212 C 782 198, 838 214, 880 206 L880 300 L0 300 Z" fill="{palette['hill_back']}"/>
  <path d="M0 258 C 138 228, 268 264, 404 250 C 546 236, 650 268, 760 254 C 824 246, 856 256, 880 252 L880 300 L0 300 Z" fill="{palette['hill_front']}"/>
  <path d="M0 290 C 160 274, 320 298, 496 286 C 664 274, 780 296, 880 288 L880 300 L0 300 Z" fill="{palette['hill_fore']}"/>

  <g stroke="{palette['fence']}" stroke-width="5" stroke-linecap="round">
    <line x1="652" y1="252" x2="652" y2="288"/>
    <line x1="716" y1="250" x2="716" y2="286"/>
    <line x1="780" y1="252" x2="780" y2="288"/>
    <line x1="844" y1="254" x2="844" y2="290"/>
    <line x1="648" y1="260" x2="848" y2="258"/>
    <line x1="648" y1="276" x2="848" y2="274"/>
  </g>

  {sheep(430, 214, 0.52, palette, 0.0)}
  {sheep(512, 206, 0.44, palette, 1.2)}
  {sheep(590, 214, 0.38, palette, 2.1)}

  {sans(54, 138, 88, "shep", palette['ink'], weight="800", length=196)}
  <rect x="58" y="160" width="186" height="7" rx="3.5" fill="{palette['butter']}"/>
  {sans(56, 198, 20, "A process manager written in Rust.", palette['ink_2'], weight="600")}
  {sans(56, 226, 20, "One shepherd keeps your flock alive.", palette['ink_2'], weight="600")}
</g>
</svg>
"""


# --------------------------------------------------------------------------
# The flock map
# --------------------------------------------------------------------------

MAP_W, MAP_H = 880, 478

# Every label is sized against this 880-unit coordinate space, and GitHub then
# stretches the whole thing to whatever the README column happens to be. That
# column measured 574px in a 960px window and 846px in a 1440px one, so a label
# drawn at 12 lands somewhere between 8px and 12px for the reader. Nothing here
# goes below 14.


def box(x, y, w, h, palette, accent):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
        f'fill="{palette["surface"]}" stroke="{palette["hairline"]}" stroke-width="2"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="4" rx="2" fill="{accent}"/>'
    )


def flock_map(palette: dict) -> str:
    wire = palette["wire"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {MAP_W} {MAP_H}" width="{MAP_W}" height="{MAP_H}" role="img" aria-label="How shep fits together: you drive the CLI, lookout or whistle; they speak to the shepherd over a control socket; the shepherd supervises your flock and its dogs; a sheep answers back over the shepherd channel.">
<defs>
  <marker id="head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 z" fill="{wire}"/>
  </marker>
</defs>
<rect width="{MAP_W}" height="{MAP_H}" rx="14" fill="{palette['paper']}"/>

<!-- what you drive -->
{box(136, 24, 608, 82, palette, palette['butter'])}
{mono(440, 58, 17, "shep · lookout (TUI) · whistle (MCP) · JSON", palette['ink'], anchor="middle", weight="700")}
{mono(440, 84, 14, "what you drive: one binary, every surface", palette['ink_3'], anchor="middle")}

<line x1="440" y1="106" x2="440" y2="158" stroke="{wire}" stroke-width="2" marker-end="url(#head)"/>
{mono(452, 138, 14, "control socket", palette['ink_3'])}

<!-- the shepherd -->
{box(136, 162, 608, 90, palette, palette['accent'])}
{sans(440, 200, 24, "the shepherd", palette['ink'], anchor="middle", weight="700")}
{mono(440, 230, 14, "one daemon · re-execs itself to detach · never binds your sockets", palette['ink_3'], anchor="middle")}

<line x1="281" y1="252" x2="281" y2="310" stroke="{wire}" stroke-width="2" marker-end="url(#head)"/>
{mono(293, 288, 14, "supervises", palette['ink_3'])}
<line x1="599" y1="252" x2="599" y2="310" stroke="{wire}" stroke-width="2" marker-end="url(#head)"/>
{mono(611, 288, 14, "supervises", palette['ink_3'])}

<!-- the flock -->
{box(136, 314, 290, 132, palette, palette['hill_front'])}
{sans(158, 348, 20, "the flock", palette['ink'], weight="700")}
{mono(158, 376, 14, "your long-running processes", palette['ink_3'])}
{mono(158, 402, 15, "web   worker   cron", palette['ink_2'], weight="700")}
{mono(158, 428, 14, "restarted, backed off, logged", palette['ink_3'])}

<!-- the dogs -->
{box(454, 314, 290, 132, palette, palette['sun'])}
{sans(476, 348, 20, "the dogs", palette['ink'], weight="700")}
{mono(476, 376, 14, "plugins the shepherd runs", palette['ink_3'])}
{mono(476, 402, 15, "metrics  bark  log-rotate", palette['ink_2'], weight="700")}
{mono(476, 428, 14, "deploy, and any you write", palette['ink_3'])}

<!-- the shepherd channel, back up from a sheep -->
<path d="M136 396 L88 396 L88 207 L136 207" fill="none" stroke="{wire}" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#head)"/>
{mono(440, 462, 14, "a sheep answers back over the shepherd channel: readiness, metrics, custom actions", palette['ink_3'], anchor="middle")}
</svg>
"""


def main() -> None:
    for name, palette in (("light", LIGHT), ("dark", DARK)):
        (OUT / f"banner-{name}.svg").write_text(banner(palette), encoding="utf-8")
        (OUT / f"flock-map-{name}.svg").write_text(flock_map(palette), encoding="utf-8")
    print(f"wrote 4 files to {OUT}")


if __name__ == "__main__":
    main()
