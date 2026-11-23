"""Compact gradient header and contribution cards, with self-contained fonts."""

from datetime import date, timedelta
from html import escape
from pathlib import Path

from profile_svg import box, circle, line, svg
from svg_typography import outline_svg

ASSETS = Path(__file__).resolve().parents[1] / "assets"


def lettering(x, y, value, size, color, family="Public Sans", anchor="start", spacing=0):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'data-font="{family}" text-anchor="{anchor}" letter-spacing="{spacing}">'
            f'{escape(str(value))}</text>')


def gradient(name, start, end):
    return (f'<linearGradient id="{name}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop stop-color="{start}"/><stop offset="1" stop-color="{end}"/>'
            '</linearGradient>')


def header(dark, mobile):
    w, h = (420, 376) if mobile else (900, 326)
    pad = 24 if mobile else 32
    ink, muted = ("#f1f5ff", "#bac6de") if dark else ("#162448", "#4f6081")
    border = "#3b4866" if dark else "#c7d5ec"
    cyan, violet = ("#8cdeff", "#d3bcff") if dark else ("#03658c", "#6b37a5")
    b = '<defs>'
    b += gradient("header", "#111c36" if dark else "#e8f4ff", "#302044" if dark else "#f1eaff")
    b += gradient("headline", cyan, violet)
    b += ('<radialGradient id="glow"><stop stop-color="#38bdf8" stop-opacity=".22"/>'
          '<stop offset="1" stop-color="#38bdf8" stop-opacity="0"/></radialGradient>'
          f'<clipPath id="panel"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22"/></clipPath></defs>')
    b += box(1, 1, w - 2, h - 2, "url(#header)", 22, border)
    b += '<g clip-path="url(#panel)">'
    b += circle(w - 25, 115, 220, "url(#glow)")
    for radius in [68, 112, 158]:
        b += circle(w - 26, 115, radius, "none", cyan, 'opacity=".13"')
    b += '</g>'
    b += lettering(pad, 40 if mobile else 44, "PRAKASH / ENGINEERING", 10 if mobile else 11,
                   cyan, "IBM Plex Mono", spacing=.7)
    if mobile:
        b += circle(pad + 3, 65, 3, "#6ee7b7" if dark else "#059669")
        b += lettering(pad + 13, 69, "OPEN TO OPPORTUNITIES", 9, muted, "IBM Plex Mono", spacing=.3)
        b += lettering(pad - 2, 122, "Prakash", 39, ink, "Sora", spacing=-1.4)
        b += lettering(pad - 2, 168, "Palsaniya", 39, ink, "Sora", spacing=-1.4)
        b += lettering(pad, 209, "Behind the screen.", 25, "url(#headline)", "Sora", spacing=-.8)
        b += lettering(pad, 248, "APIs, document search, background workers,", 14, muted)
        b += lettering(pad, 270, "and the systems that connect them.", 14, muted)
        chip_y, foot_y = 291, 350
    else:
        b += circle(w - 210, 40, 3, "#6ee7b7" if dark else "#059669")
        b += lettering(w - pad, 44, "OPEN TO OPPORTUNITIES", 10, muted, "IBM Plex Mono", "end", .5)
        b += lettering(pad - 2, 113, "Prakash Palsaniya", 45, ink, "Sora", spacing=-1.8)
        b += lettering(pad, 163, "Behind the screen.", 33, "url(#headline)", "Sora", spacing=-1)
        b += lettering(pad, 202, "APIs, document search, background workers,", 16, muted)
        b += lettering(pad, 226, "and the systems that connect them.", 16, muted)
        chip_y, foot_y = 246, 302
    for x, width, title, accent, fill in [
        (pad, 174, "Backend development", cyan, "#123652" if dark else "#d6edfc"),
        (pad + 184, 103, "Applied AI", violet, "#392853" if dark else "#e5dafa"),
    ]:
        b += box(x, chip_y, width, 29, fill, 8)
        b += lettering(x + 12, chip_y + 19, title, 12, accent)
    b += line(pad, foot_y - 20, w - pad, foot_y - 20, border)
    b += lettering(pad, foot_y, "NIT SRINAGAR", 10, ink, "IBM Plex Mono", spacing=.5)
    b += lettering(w - pad, foot_y, "IT / CLASS OF 2027", 10, muted, "IBM Plex Mono", "end", .2)
    desc = ("Prakash Palsaniya. Backend development and applied AI. "
            "I build APIs, document search, background workers, and the systems that connect them. "
            "Information Technology at NIT Srinagar, class of 2027. Open to opportunities.")
    return outline_svg(svg(w, h, "Prakash Palsaniya — Backend development and applied AI", desc, b))


def activity(data, dark, mobile):
    today = date.fromisoformat(data["updated"])
    days = data["days"]
    active = [day for day, count in days.items() if count]
    since = date.fromisoformat(min(active)).strftime("%b %Y") if active else "Jan 2023"
    annual = sum(n for day, n in days.items() if str(today - timedelta(days=364)) <= day <= str(today))
    recent = sum(n for day, n in days.items() if str(today - timedelta(days=89)) <= day <= str(today))
    metrics = [
        ("ALL TIME", sum(days.values()), f"Since {since}", "#7dd3fc" if dark else "#03658c", "#12374b" if dark else "#dff4fd", "#152739" if dark else "#ecf7ff"),
        ("LAST YEAR", annual, "Past 365 days", "#c4b5fd" if dark else "#6d3fa8", "#35284f" if dark else "#ece4fc", "#25233a" if dark else "#f4efff"),
        ("RECENT WORK", recent, "Past 90 days", "#fcd38a" if dark else "#995416", "#493426" if dark else "#ffecd2", "#302725" if dark else "#fff6e8"),
    ]
    w, h = (420, 446) if mobile else (900, 254)
    ink, muted = ("#f1f5ff", "#b9c5d9") if dark else ("#162448", "#54617a")
    border = "#344159" if dark else "#d5dfef"
    b = '<defs>' + gradient("activity", "#111b2d" if dark else "#f7faff", "#201d30" if dark else "#f5f2fc")
    for index, metric in enumerate(metrics):
        b += gradient(f"metric-{index}", metric[4], metric[5])
    b += '</defs>' + box(1, 1, w - 2, h - 2, "url(#activity)", 20, border)
    b += lettering(24, 36, "The work, over time", 20 if mobile else 21, ink, "Sora", spacing=-.5)
    if mobile:
        b += lettering(24, 59, "UPDATED " + today.strftime("%d %b %Y").upper(), 10, muted, "IBM Plex Mono", spacing=.5)
    else:
        b += lettering(w - 24, 35, "UPDATED " + today.strftime("%d %b %Y").upper(), 10, muted, "IBM Plex Mono", "end", .5)
    for index, (caption, count, period, accent, _, _) in enumerate(metrics):
        x, y, cw, ch = (20, 77 + index * 110, 380, 100) if mobile else (24 + index * 290, 60, 272, 147)
        b += box(x, y, cw, ch, f"url(#metric-{index})", 13, border)
        b += box(x + 1, y + 18, 3, ch - 36, accent, 1)
        b += lettering(x + 20, y + 27, caption, 10, accent, "IBM Plex Mono", spacing=.8)
        if mobile:
            b += lettering(x + cw - 21, y + 64, f"{count:,}", 38 if count < 100000 else 28, accent, "Sora", "end", -1.3)
            b += lettering(x + 20, y + 72, period, 13, muted)
        else:
            b += lettering(x + 20, y + 92, f"{count:,}", 51 if count < 100000 else 37, accent, "Sora", spacing=-2)
            b += lettering(x + 20, y + 126, period, 13, muted)
    b += lettering(24, h - 18, "PUBLIC GITHUB CONTRIBUTIONS", 9, muted, "IBM Plex Mono", spacing=.7)
    desc = (f"{sum(days.values()):,} GitHub contributions since {since}; {annual:,} in the past 365 days; "
            f"{recent:,} in the past 90 days. Updated {today:%d %b %Y}.")
    return outline_svg(svg(w, h, "Prakash Palsaniya — GitHub contribution cards", desc, b))


def write_cards(data):
    # Render every variant successfully before updating any published asset.
    cards = {}
    for dark in [False, True]:
        for mobile in [False, True]:
            suffix = ("dark" if dark else "light") + ("-mobile" if mobile else "")
            cards[f"profile-header-{suffix}.svg"] = header(dark, mobile)
            cards[f"github-activity-{suffix}.svg"] = activity(data, dark, mobile)
    for name, content in cards.items():
        (ASSETS / name).write_text(content, encoding="utf-8")
