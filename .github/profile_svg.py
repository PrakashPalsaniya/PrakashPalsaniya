"""Small, dependency-free drawing primitives shared by the profile generators."""

from html import escape


def palette(dark):
    return dict(
        bg="#111310" if dark else "#f7f7f0",
        panel="#191c17" if dark else "#eeefe6",
        raised="#22271e" if dark else "#e3e7d9",
        ink="#f1f2e9" if dark else "#20251b",
        muted="#a5ad9b" if dark else "#59634d",
        line="#343b2d" if dark else "#d2d8c6",
        accent="#c3f467" if dark else "#456818",
        solid="#c3f467",
    )


def text(x, y, value, size, color, weight=400, mono=False, extra=""):
    font = "Consolas,'Liberation Mono',monospace" if mono else "Arial,Helvetica,sans-serif"
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def box(x, y, width, height, fill, radius=0, stroke=None, extra=""):
    border = f' stroke="{stroke}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{fill}"{border} {extra}/>'


def line(x1, y1, x2, y2, color, width=1, extra=""):
    return f'<path d="M{x1} {y1}H{x2}" stroke="{color}" stroke-width="{width}" {extra}/>' if y1 == y2 else f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" {extra}/>'


def circle(x, y, radius, fill, stroke=None, extra=""):
    border = f' stroke="{stroke}"' if stroke else ""
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}"{border} {extra}/>'


def path(d, color, width=1.5, extra=""):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def arrow(x, y, color, size=22):
    return path(f"M{x} {y + size}L{x + size} {y}M{x} {y}H{x + size}V{y + size}", color, 2.5)


def label(x, y, value, p, color=None, size=12, extra=""):
    return text(x, y, value, size, color or p["muted"], 600, True, 'letter-spacing="1" ' + extra)


def group(body, x=0, y=0, scale=1, extra=""):
    return f'<g transform="translate({x} {y}) scale({scale})" {extra}>{body}</g>'


def badge(x, y, value, p, color=None, size=12):
    width = len(value) * size * .64 + 26
    return box(x, y, width, size + 18, p["panel"], 5, p["line"]) + text(x + 13, y + size + 8, value, size, color or p["ink"], mono=True), width


def tags(x, y, values, p, size=12):
    body = ""
    for value in values:
        item, width = badge(x, y, value, p, size=size)
        body += item
        x += width + 8
    return body


def grid(p, width=480, height=360):
    return '<defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">' + circle(1, 1, 1, p["line"]) + '</pattern></defs>' + box(0, 0, width, height, "url(#grid)")


def wire(d, p, color=None, delay=0):
    color = color or p["accent"]
    return path(d, p["line"], 2) + path(d, color, 2, f'class="packet" style="animation-delay:{delay}s"')


MOTION = """
<style>
  .packet { stroke-dasharray: 9 180; animation: travel 8s linear infinite; }
  .breathe { animation: breathe 5s ease-in-out infinite; }
  .float { animation: float 7s ease-in-out infinite; }
  .scan { animation: scan 6s ease-in-out infinite; }
  @keyframes travel { to { stroke-dashoffset: -378; } }
  @keyframes breathe { 0%,100% { opacity:.45; } 50% { opacity:1; } }
  @keyframes float { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-9px); } }
  @keyframes scan { 0%,100% { transform:translateY(0); opacity:.35; } 50% { transform:translateY(62px); opacity:.85; } }
  @media (prefers-reduced-motion: reduce) {
    .packet,.breathe,.float,.scan { animation:none; }
  }
</style>
"""


def svg(width, height, title, description, body, animated=False):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description"><title id="title">{escape(title)}</title><desc id="description">{escape(description)}</desc>{MOTION if animated else ""}{body}</svg>\n'


def frame(width, height, p):
    return box(1, 1, width - 2, height - 2, p["bg"], 16, p["line"])
