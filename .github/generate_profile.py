"""Generate the complete SVG identity and README. Run from any working directory."""

from pathlib import Path
import re

from profile_svg import arrow, badge, box, circle, frame, grid, group, label, line, palette, path, svg, tags, text, wire

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PROFILE_IMAGE_WIDTH = 640

PROJECTS = [
    dict(slug="documind", name="DocuMind", category="DOCUMENT INTELLIGENCE", accent=("#ad4623", "#ffa77c"),
         headline=["Your PDFs.", "With answers."], description="Ask questions. Follow the sources.",
         tags=["LangGraph", "Qdrant", "BullMQ", "S3"],
         url="https://docu-mind-alpha-topaz.vercel.app/", repo="https://github.com/PrakashPalsaniya/Docu-Mind",
         detail="Vector search + BM25 retrieve the candidates; reranking puts the useful context first. LangGraph orchestrates the flow. BullMQ workers process documents in the background, with files in S3 and metadata in PostgreSQL.",
         flow="PDF → background worker → hybrid retrieval → reranking → answer + sources"),
    dict(slug="screenly", name="Screenly", category="REAL-TIME BOOKING", accent=("#456818", "#c3f467"),
         headline=["One seat.", "One booking."], description="Built for the race to checkout.",
         tags=["Redis", "MongoDB", "Razorpay", "RabbitMQ"],
         url="https://screenly-beta.vercel.app/", repo=None,
         detail="Redis holds seats during checkout. MongoDB transactions protect bookings, Razorpay handles payments, and RabbitMQ queues confirmation emails.",
         flow="Select seat → Redis hold → payment → booking transaction → queued email"),
    dict(slug="finmate", name="FinMate", category="PERSONAL FINANCE + AI", accent=("#6842a5", "#bfa5ff"),
         headline=["Less logging.", "More living."], description="Track spending, one conversation at a time.",
         tags=["Gemini", "Telegram", "Redis", "Excel"],
         url="https://fin-mate-zeta.vercel.app/", repo="https://github.com/PrakashPalsaniya/FinMate",
         detail="Chat-based expense entry and a Telegram bot make logging quick. A Gemini assistant helps with spending questions. Redis caches reports, and Excel exports keep the data portable.",
         flow="Chat or Telegram → expense entry → reports → assistant + Excel export"),
    dict(slug="pklinks", name="PKLinks", category="LINKS / MICROSERVICES", accent=("#116c7d", "#76d9e7"),
         headline=["Short links.", "Long story."], description="A short URL with a lot under the hood.",
         tags=["Node.js", "Redis", "RabbitMQ", "Docker"],
         url="https://pklinks-frontend.vercel.app/", repo="https://github.com/PrakashPalsaniya/Pklinks-micro-services",
         detail="Redis caches redirects. RabbitMQ sends click events to a separate analytics worker. Built to work through service boundaries, caching, and asynchronous processing.",
         flow="Short link → cached redirect → destination · click event → analytics worker"),
]


def core(p):
    b = grid(p, 480, 400)
    b += f'<ellipse cx="240" cy="205" rx="208" ry="145" fill="none" stroke="{p["line"]}"/>'
    b += f'<ellipse cx="240" cy="205" rx="162" ry="111" fill="none" stroke="{p["line"]}" stroke-dasharray="3 9"/>'
    b += wire("M47 83H118V171H175", p, delay=-1)
    b += wire("M427 106H365V166H300", p, delay=-3)
    b += wire("M240 253V335H402", p, delay=-5)
    b += label(27, 61, "REQUEST", p, size=11)
    b += circle(47, 83, 6, p["accent"])
    b += label(373, 85, "CONTEXT", p, size=11)
    b += circle(427, 106, 6, p["bg"], p["accent"])
    b += circle(402, 335, 6, p["accent"], extra='class="breathe"')
    b += label(345, 365, "RESPONSE", p, size=11)
    for cy in [231, 197, 163]:
        b += f'<polygon points="240,{cy-64} 354,{cy} 240,{cy+64} 126,{cy}" fill="{p["panel"]}" stroke="{p["accent"]}" stroke-width="1.3"/>'
        b += f'<path d="M126 {cy}V{cy+12}L240 {cy+76}L354 {cy+12}V{cy}" fill="{p["raised"]}" stroke="{p["line"]}"/>'
        b += line(145, cy + 20, 182, cy + 41, p["accent"], 2)
        b += circle(321, cy + 25, 2, p["accent"])
        b += circle(332, cy + 19, 2, p["muted"])
    chip = '<polygon points="240,113 307,151 240,189 173,151" fill="' + p["solid"] + '"/>'
    chip += path("M202 151L223 138M202 151L223 164M278 151L257 138M278 151L257 164M247 134L234 168", "#263715", 3)
    b += f'<g class="float">{chip}</g>'
    b += label(33, 389, "INPUT → LOGIC → SOMETHING USEFUL", p, size=11)
    return b


def header(dark, mobile):
    p = palette(dark)
    w, h = (640, 884) if mobile else (1200, 400)
    b = frame(w, h, p)
    b += box(32 if mobile else 42, 32, 38, 30, p["solid"], 5)
    b += text(51 if mobile else 61, 53, "pp", 18, "#233014", 700, True, 'text-anchor="middle"')
    b += label(83 if mobile else 94, 52, "PRAKASH / ENGINEERING", p, size=16 if mobile else 12)
    if not mobile:
        b += circle(972, 47, 4, p["accent"], extra='class="breathe"')
        b += label(985, 52, "OPEN TO OPPORTUNITIES", p, size=10)
    b += line(32 if mobile else 42, 83, w - (32 if mobile else 42), 83, p["line"])
    b += label(34 if mobile else 44, 127 if mobile else 116, "BACKEND DEVELOPMENT  /  APPLIED AI", p, p["accent"], size=17 if mobile else 12)
    x = 30 if mobile else 38
    name_spacing = -6 if mobile else -4
    b += text(x, 229 if mobile else 192, "Prakash", 101 if mobile else 82, p["ink"], 700, extra=f'letter-spacing="{name_spacing}"')
    b += text(x, 323 if mobile else 267, "Palsaniya", 101 if mobile else 82, p["ink"], 700, extra=f'letter-spacing="{name_spacing}"')
    b += circle(452 if mobile else 389, 313 if mobile else 260, 8 if mobile else 6, p["accent"])
    if mobile:
        b += text(36, 374, "I build what happens", 27, p["muted"])
        b += text(36, 410, "behind the screen.", 27, p["ink"], 600)
    else:
        b += text(44, 310, "I build what happens behind the screen.", 24, p["muted"])
    b += group(core(p), 75 if mobile else 750, 434 if mobile else 90, .98 if mobile else .59)
    if not mobile:
        b += line(652, 108, 652, 314, p["line"])
    fy = h - 60
    b += line(32 if mobile else 42, fy, w - (32 if mobile else 42), fy, p["line"])
    b += circle(40 if mobile else 48, fy + 30, 4, p["accent"])
    b += label(54 if mobile else 62, fy + 35, "NIT SRINAGAR", p, p["ink"], size=16 if mobile else 12)
    b += label(w - 34 if mobile else w - 44, fy + 35, "IT · CLASS OF 2027", p, size=16 if mobile else 12, extra='text-anchor="end"')
    return svg(w, h, "Prakash Palsaniya — Behind the screen", "Backend development and applied AI. I build what happens behind the screen. IT student at NIT Srinagar, class of 2027. Open to opportunities. Animated illustration of requests flowing through a layered server.", b, True)


def diagram(slug, p, accent, captions=True):
    b = grid(p, 470, 286)
    if slug == "documind":
        if captions:
            b += label(20, 28, "01 / RETRIEVAL PIPELINE", p, size=10)
        for dx, dy in [(0, 0), (8, -8), (16, -16)]:
            b += box(18 + dx, 83 + dy, 91, 138, p["bg"], 6, p["line"])
        b += box(47, 83, 35, 20, accent, 3)
        b += text(64.5, 97, "PDF", 10, p["bg"], 700, True, 'text-anchor="middle"')
        for y, length in [(119, 63), (132, 45), (145, 59), (158, 38), (171, 54)]:
            b += line(48, y, 48 + length, y, p["line"], 3)
        b += '<g class="scan">' + box(42, 111, 79, 3, accent, 1) + '</g>'
        b += wire("M126 145H153V97H180M153 145V190H180", p, accent, -2)
        for y, label1, label2 in [(69, "VECTOR", "semantic"), (162, "BM25", "keyword")]:
            b += box(180, y, 108, 59, p["bg"], 8, p["line"])
            b += text(234, y + 25, label1, 13, accent, 700, True, 'text-anchor="middle"')
            b += text(234, y + 44, label2, 11, p["muted"], mono=True, extra='text-anchor="middle"')
        b += wire("M288 97H313V143H337M288 190H313V143", p, accent, -4)
        b += box(337, 109, 113, 68, p["raised"], 8, accent)
        b += text(393, 139, "RERANK", 13, p["ink"], 700, True, 'text-anchor="middle"')
        b += text(393, 159, "+ cite", 12, accent, mono=True, extra='text-anchor="middle"')
        if captions:
            b += label(22, 264, "CONTEXT IN. SOURCES OUT.", p, accent, size=11)
    elif slug == "screenly":
        if captions:
            b += label(20, 28, "02 / THE CONCURRENCY PROBLEM", p, size=10)
        b += path("M28 67Q133 42 238 67", p["line"], 3)
        b += label(93, 54, "SCREEN", p, size=9)
        for row in range(4):
            for col in range(6):
                x, y = 29 + col * 33 + (13 if col > 2 else 0), 87 + row * 34
                held = (row, col) == (1, 3)
                taken = (row, col) in [(0, 1), (0, 4), (2, 0), (2, 5), (3, 1), (3, 2)]
                b += box(x, y, 24, 22, accent if held else p["raised"] if taken else p["bg"], 5, accent if held else p["line"])
                b += line(x + 4, y + 17, x + 20, y + 17, p["bg"] if held else p["line"], 2)
                if held:
                    b += circle(x + 12, y + 9, 3, p["bg"])
        b += wire("M166 132H267V103H287", p, accent, -3)
        b += box(287, 72, 160, 67, p["bg"], 8, accent)
        b += circle(306, 94, 3, accent, extra='class="breathe"')
        b += text(318, 98, "SEAT HELD", 12, accent, 700, True)
        b += text(301, 121, "Redis / checkout", 11, p["muted"], mono=True)
        b += wire("M367 139V165", p, accent)
        b += box(287, 165, 160, 51, p["bg"], 8, p["line"])
        b += text(367, 195, "BOOK → CONFIRM", 12, p["ink"], 700, True, 'text-anchor="middle"')
        if captions:
            b += label(22, 264, "HOLD FIRST. CONFIRM ONCE.", p, accent, size=11)
    elif slug == "finmate":
        if captions:
            b += label(20, 28, "03 / SPENDING, IN CONVERSATION", p, size=10)
        b += box(27, 60, 279, 47, p["bg"], 12, p["line"])
        b += text(44, 89, "Add lunch, ₹180", 17, p["ink"])
        b += circle(287, 84, 7, accent)
        b += path("M284 84L287 87L291 81", p["bg"], 1.3)
        b += box(91, 121, 353, 96, p["bg"], 12, p["line"])
        b += text(110, 147, "Logged. Lunch → Food", 15, accent, 600)
        b += text(110, 174, "Your spending, a little clearer.", 13, p["muted"])
        for index, height in enumerate([10, 17, 12, 23, 17, 28, 20]):
            b += box(299 + index * 17, 203 - height, 10, height, accent, 2, extra=f'opacity="{.4 + index * .09}"')
        b += label(110, 201, "ILLUSTRATIVE CHAT", p, size=9)
        if captions:
            b += label(22, 264, "CHAT → TRACK → UNDERSTAND", p, accent, size=11)
    else:
        if captions:
            b += label(20, 28, "04 / TWO PATHS. ONE CLICK.", p, size=10)
        b += box(21, 66, 132, 58, p["bg"], 9, p["line"])
        b += text(87, 101, "/your-link", 15, p["ink"], 700, True, 'text-anchor="middle"')
        b += wire("M153 95H201", p, accent, -1)
        b += box(201, 66, 105, 58, p["raised"], 9, accent)
        b += text(253, 92, "REDIS", 13, accent, 700, True, 'text-anchor="middle"')
        b += text(253, 110, "cached URL", 10, p["muted"], mono=True, extra='text-anchor="middle"')
        b += wire("M306 95H350", p, accent, -3)
        b += box(350, 66, 99, 58, p["bg"], 9, p["line"])
        b += text(399, 101, "302 ↗", 20, p["ink"], 700, True, 'text-anchor="middle"')
        b += wire("M176 95V192H214", p, accent, -4)
        b += box(214, 165, 235, 55, p["bg"], 9, p["line"])
        for i in range(3):
            b += box(230 + i * 13, 185, 8, 14, accent, 2, extra=f'opacity="{1 - i * .25}"')
        b += text(283, 188, "CLICK EVENT", 11, accent, 700, True)
        b += text(283, 206, "→ analytics worker", 11, p["muted"], mono=True)
        if captions:
            b += label(22, 264, "REDIRECT NOW. ANALYZE ASYNC.", p, accent, size=11)
    return b


def project_card(project, index, dark, mobile):
    p = palette(dark)
    accent = project["accent"][int(dark)]
    w, h = (640, 742) if mobile else (1200, 260)
    x = 32 if mobile else 42
    b = frame(w, h, p)
    b += box(x, 32, 37, 27, accent, 4)
    b += text(x + 18.5, 51, f"0{index + 1}", 12, p["bg"], 700, True, 'text-anchor="middle"')
    b += label(x + 50, 51, project["category"], p, accent, size=16 if mobile else 12)
    b += arrow(w - x - 23, 35, accent, 18)
    b += text(x, 104 if mobile else 96, project["name"], 26 if mobile else 23, p["ink"], 700)
    if mobile:
        for row, value in enumerate(project["headline"]):
            b += text(x - 2, 171 + row * 59, value, 59, p["ink"] if row == 0 else accent, 700, extra='letter-spacing="-2.5"')
    else:
        b += text(x - 2, 148, " ".join(project["headline"]), 40, accent, 700, extra='letter-spacing="-1.5"')
    b += text(x, 272 if mobile else 184, project["description"], 23 if mobile else 19, p["muted"])
    b += tags(x, 303 if mobile else 208, project["tags"], p, size=18 if mobile else 12)
    if mobile:
        b += line(32, 360, 608, 360, p["line"])
        art = re.sub(r'font-size="(\d+)"', lambda m: f'font-size="{round(int(m[1]) * 1.2, 1)}"', diagram(project["slug"], p, accent))
        b += group(art, 38, 384, 1.2)
    else:
        b += line(650, 76, 650, 232, p["line"])
        # Keep diagram labels at their original size; trim decorative top/bottom captions.
        b += '<svg x="685" y="64" width="470" height="176" viewBox="0 49 470 176">' + diagram(project["slug"], p, accent, captions=False) + '</svg>'
    return svg(w, h, project["name"], f'{project["name"]}: {" ".join(project["headline"])} {project["description"]} {project["flow"]}. Stack: {", ".join(project["tags"])}.', b, True)


def toolbox(dark, mobile):
    p = palette(dark)
    w, h = (640, 744) if mobile else (1200, 244)
    b = frame(w, h, p)
    b += label(32 if mobile else 42, 44, "THE TOOLBOX / CHOSEN FOR THE JOB", p, p["accent"], size=16 if mobile else 12)
    rows = [
        ("01", "Build the API", ["Node.js · Express", "Python · Socket.IO"]),
        ("02", "Move the data", ["PostgreSQL · MongoDB", "Redis · RabbitMQ · BullMQ"]),
        ("03", "Add intelligence", ["LangChain · LangGraph", "Qdrant"]),
        ("04", "Ship the thing", ["React · Tailwind", "Docker · AWS"]),
    ]
    for index, (number, title, values) in enumerate(rows):
        x, y = (32, 92 + index * 144) if mobile else (42 + index * 285, 94)
        if not mobile and index:
            b += line(x - 24, 82, x - 24, 166, p["line"])
        b += label(x, y, number, p, p["accent"], size=16 if mobile else 12)
        b += text(x, y + (36 if mobile else 28), title, 26 if mobile else 23, p["ink"], 700, extra='letter-spacing="-.7"')
        for row, value in enumerate(values):
            b += text(x, y + (71 if mobile else 53) + row * (26 if mobile else 23), value, 22 if mobile else 16, p["muted"])
        if mobile and index < 3:
            b += line(32, y + 120, 608, y + 120, p["line"])
    b += line(32 if mobile else 42, h - 58, w - (32 if mobile else 42), h - 58, p["line"])
    b += label(32 if mobile else 42, h - 24, "ALSO EXPLORING", p, size=16 if mobile else 11)
    b += text(w - (32 if mobile else 42), h - 24, "DSA in C++ / system design", 17 if mobile else 14, p["ink"], mono=True, extra='text-anchor="end"')
    return svg(w, h, "The toolbox", "Node.js, Express, Python, Socket.IO; PostgreSQL, MongoDB, Redis, RabbitMQ, BullMQ; LangChain, LangGraph, Qdrant; React, Tailwind, Docker, AWS. Also exploring DSA in C++ and system design.", b)


def contact(dark, mobile):
    p = palette(dark)
    w, h = (640, 336) if mobile else (1200, 168)
    b = box(1, 1, w - 2, h - 2, p["solid"], 16)
    ink = "#243413"
    b += label(32 if mobile else 42, 42, "GOT AN INTERESTING PROBLEM?", p, ink, size=17 if mobile else 12)
    if mobile:
        b += text(30, 110, "Let's build", 66, ink, 700, extra='letter-spacing="-3"')
        b += text(30, 178, "something good.", 66, ink, 700, extra='letter-spacing="-3"')
    else:
        b += text(40, 96, "Let's build something good.", 46, ink, 700, extra='letter-spacing="-1.5"')
    b += arrow(w - (73 if mobile else 92), 40 if mobile else 58, ink, 31 if mobile else 32)
    b += line(32 if mobile else 42, h - (87 if mobile else 52), w - (32 if mobile else 42), h - (87 if mobile else 52), "#91bb49")
    b += text(32 if mobile else 42, h - (50 if mobile else 22), "Backend + applied AI opportunities", 22 if mobile else 18, ink)
    b += text(32 if mobile else w - 42, h - 22, "prakash8290682001@gmail.com", 18 if mobile else 14, ink, mono=True, extra='' if mobile else 'text-anchor="end"')
    return svg(w, h, "Let's build something good", "Open to backend and applied AI opportunities. Email Prakash at prakash8290682001@gmail.com.", b)


def picture(slug, alt):
    return f'''<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="./assets/{slug}-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="./assets/{slug}-light-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="./assets/{slug}-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/{slug}-light.svg">
  <img src="./assets/{slug}-light.svg" width="{PROFILE_IMAGE_WIDTH}" alt="{alt}">
</picture>'''


def readme():
    b = "<!-- Generated by .github/generate_profile.py. Edit the generator to keep artwork and copy in sync. -->\n\n"
    b += picture("profile-header", "Prakash Palsaniya. I build what happens behind the screen. Backend and applied AI. NIT Srinagar, IT, 2027.")
    b += '''

<p align="center">
  <a href="https://prakash-palsaniya.vercel.app/"><strong>Portfolio ↗</strong></a>&nbsp;&nbsp; / &nbsp;&nbsp;
  <a href="https://www.linkedin.com/in/prakash-palsaniya"><strong>LinkedIn ↗</strong></a>&nbsp;&nbsp; / &nbsp;&nbsp;
  <a href="https://prakash-palsaniya.vercel.app/Prakash-Palsaniya-Resume.pdf"><strong>Résumé ↗</strong></a>&nbsp;&nbsp; / &nbsp;&nbsp;
  <a href="mailto:prakash8290682001@gmail.com"><strong>Say hello ↗</strong></a>
</p>

I'm **Prakash**, an Information Technology student at **NIT Srinagar**, graduating in **2027**. I like the parts of an app you don't see: two people reaching for the same seat, a document being processed in the background, a redirect that needs to get out of the way.

That's where I spend my time: **backend development and applied AI**. These are a few things I've built along the way.

'''
    b += '## 01 / The work, over time\n\n' + picture("github-activity", "GitHub activity: contributions since November 2023, past-year totals, primary languages by public repository, and a 90-day contribution heatmap. Each card shows its last refresh date.")
    b += '\n\n[Explore my GitHub activity ↗](https://github.com/PrakashPalsaniya?tab=overview) · Refreshed daily with GitHub Actions.\n\n'
    b += '''## 02 / Selected builds

Four different products. Plenty of interesting problems under the hood.

'''
    for project in PROJECTS:
        b += f'<a href="{project["url"]}">\n' + picture(project["slug"], f'{project["name"]}. {" ".join(project["headline"])} {project["description"]}') + '\n</a>\n\n'
        b += f'<p><a href="{project["url"]}"><strong>Explore {project["name"]} ↗</strong></a>'
        if project["repo"]:
            b += f'&nbsp; · &nbsp;<a href="{project["repo"]}">Source code</a>'
        b += '</p>\n\n'
        b += f'<details>\n  <summary><strong>Under the hood</strong> — {project["name"]}</summary>\n\n{project["detail"]}\n\n**The flow**\n\n{project["flow"]}\n\n</details>\n\n<br>\n\n'
    b += '## 03 / Tools I reach for\n\n' + picture("toolbox", "Node.js, Express, Python, Socket.IO; PostgreSQL, MongoDB, Redis, RabbitMQ, BullMQ; LangChain, LangGraph, Qdrant; React, Tailwind, Docker, AWS. Also DSA in C++ and system design.") + '\n\n<br>\n\n'
    b += '<a href="mailto:prakash8290682001@gmail.com">\n' + picture("contact", "Got an interesting problem? Let's build something good. Open to backend and applied AI opportunities. Email prakash8290682001@gmail.com.") + '\n</a>\n'
    return b


def main():
    ASSETS.mkdir(exist_ok=True)
    for dark in [False, True]:
        for mobile in [False, True]:
            suffix = ("-dark" if dark else "-light") + ("-mobile" if mobile else "") + ".svg"
            cards = {"profile-header": header(dark, mobile), "toolbox": toolbox(dark, mobile), "contact": contact(dark, mobile)}
            cards.update({project["slug"]: project_card(project, index, dark, mobile) for index, project in enumerate(PROJECTS)})
            for name, content in cards.items():
                (ASSETS / (name + suffix)).write_text(content, encoding="utf-8")
    (ROOT / "README.md").write_text(readme(), encoding="utf-8")
    print("Generated 28 SVGs and the responsive profile README.")


if __name__ == "__main__":
    main()
