"""Generate the GitHub profile with small PNG badges and native content."""

from datetime import date, timedelta
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".github" / "activity-data.json"
ASSET_VERSION = "typography-2"


def spaced(value):
    # A breakable third-em space gives native text slightly more word spacing.
    return escape(str(value)).replace(" ", "\u2004")


def heading(value):
    return f"<h3>{spaced(value)}</h3>"


def picture(name, alt, width, height=None):
    height_attribute = f' height="{height}"' if height is not None else ""
    return f'''<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/{name}-dark.png?v={ASSET_VERSION}">
  <img src="./assets/{name}-light.png?v={ASSET_VERSION}" width="{width}"{height_attribute} alt="{escape(alt, quote=True)}">
</picture>'''

PROJECTS = [
    dict(name="DocuMind", description="PDF Q&A with hybrid retrieval, reranking, and sources.",
         tags=["LangGraph", "Qdrant", "BullMQ", "S3"],
         url="https://docu-mind-alpha-topaz.vercel.app/", repo="https://github.com/PrakashPalsaniya/Docu-Mind",
         detail="Vector search + BM25 retrieve the candidates; reranking puts the useful context first. LangGraph orchestrates the flow. BullMQ workers process documents in the background, with files in S3 and metadata in PostgreSQL.",
         flow="PDF → background worker → hybrid retrieval → reranking → answer + sources"),
    dict(name="Screenly", description="Seat booking with Redis holds and payment-safe transactions.",
         tags=["Redis", "MongoDB", "Razorpay", "RabbitMQ"],
         url="https://screenly-beta.vercel.app/", repo=None,
         detail="Redis holds seats during checkout. MongoDB transactions protect bookings, Razorpay handles payments, and RabbitMQ queues confirmation emails.",
         flow="Select seat → Redis hold → payment → booking transaction → queued email"),
    dict(name="FinMate", description="Expense tracking through chat, Telegram, and an AI assistant.",
         tags=["Gemini", "Telegram", "Redis", "Excel"],
         url="https://fin-mate-zeta.vercel.app/", repo="https://github.com/PrakashPalsaniya/FinMate",
         detail="Chat-based expense entry and a Telegram bot make logging quick. A Gemini assistant helps with spending questions. Redis caches reports, and Excel exports keep the data portable.",
         flow="Chat or Telegram → expense entry → reports → assistant + Excel export"),
    dict(name="PKLinks", description="Cached short links with asynchronous click analytics.",
         tags=["Node.js", "Redis", "RabbitMQ", "Docker"],
         url="https://pklinks-frontend.vercel.app/", repo="https://github.com/PrakashPalsaniya/Pklinks-micro-services",
         detail="Redis caches redirects. RabbitMQ sends click events to a separate analytics worker. Built to work through service boundaries, caching, and asynchronous processing.",
         flow="Short link → cached redirect → destination · click event → analytics worker"),
]


def activity_summary(data):
    today = date.fromisoformat(data["updated"])
    first = date(2023, 1, 1)
    expected = {str(first + timedelta(days=i)) for i in range((today - first).days + 1)}
    days = data["days"]
    if set(days) != expected:
        raise ValueError("Activity snapshot must contain every day from January 2023 through its refresh date")
    if any(type(n) is not int or n < 0 for n in days.values()):
        raise ValueError("Contribution counts must be nonnegative integers")
    if any(not isinstance(name, str) or type(n) is not int or n < 0 for name, n in data["languages"].items()):
        raise ValueError("Language counts must be nonnegative repository counts")
    active_days = [day for day, count in days.items() if count]
    since = date.fromisoformat(min(active_days)).strftime("%b %Y") if active_days else "Jan 2023"
    annual = sum(count for day, count in days.items() if str(today - timedelta(days=364)) <= day <= str(today))
    recent = sum(count for day, count in days.items() if str(today - timedelta(days=89)) <= day <= str(today))
    languages = sorted(data["languages"].items(), key=lambda pair: (-pair[1], pair[0]))[:4]
    language_text = ", ".join(f"{escape(name)} ({count})" for name, count in languages) or "No language data available"
    badges = [picture("contributions-total", f"{sum(days.values()):,} contributions since {since}", 128, 36),
              picture("contributions-year", f"{annual:,} contributions in the past 365 days", 128, 36),
              picture("contributions-recent", f"{recent:,} contributions in the past 90 days", 128, 36)]
    return heading("The work, over time") + '\n\n<p>\n' + '\n'.join(badges) + f'''
</p>
<p><sub>Contributions since {since} · Updated {today:%d %b %Y} ·
<a href="https://github.com/PrakashPalsaniya?tab=overview">View activity ↗</a><br>
Primary languages by public repository: {language_text}. Forks excluded.</sub></p>'''


def project_block(project, index):
    categories = ["Document intelligence", "Real-time booking", "Personal finance + AI", "Links / microservices"]
    links = f'<a href="{escape(project["url"], quote=True)}">Live ↗</a>'
    if project["repo"]:
        links += f' · <a href="{escape(project["repo"], quote=True)}">Source code</a>'
    return f'''    <td width="50%" valign="top">
      <strong>{spaced(project["name"])}</strong><br>
      <sub>{spaced(f"0{index + 1} / {categories[index]}")}</sub><br>
      {spaced(project["description"])}<br>
      <sub>{spaced(" · ".join(project["tags"]))}</sub><br>
      {links}
    </td>'''


def readme(data=None):
    if data is None:
        data = json.loads(CACHE.read_text(encoding="utf-8"))
    activity = activity_summary(data)
    b = '<!-- Generated by .github/generate_profile.py. Edit the generator to keep the profile in sync. -->\n\n'
    b += picture("profile-title", "Prakash Palsaniya — Backend development and applied AI", 320)
    b += f'''

<p>{spaced("Information Technology at ")}<strong>{spaced("NIT Srinagar")}</strong>{spaced(" · Class of ")}<strong>2027</strong><br>
{spaced("I build APIs, document search pipelines, background workers, and connected systems.")}</p>

<p>
  <a href="https://prakash-palsaniya.vercel.app/"><strong>Portfolio&nbsp;↗</strong></a> ·
  <a href="https://www.linkedin.com/in/prakash-palsaniya">LinkedIn&nbsp;↗</a> ·
  <a href="https://prakash-palsaniya.vercel.app/Prakash-Palsaniya-Resume.pdf">Résumé&nbsp;↗</a> ·
  <a href="mailto:prakash8290682001@gmail.com">Email&nbsp;↗</a>
</p>

'''
    b += activity + '\n\n' + heading("Selected builds") + '\n\n<table width="100%">\n'
    for row in range(0, len(PROJECTS), 2):
        b += '  <tr>\n'
        for index in range(row, min(row + 2, len(PROJECTS))):
            b += project_block(PROJECTS[index], index) + '\n'
        b += '  </tr>\n'
    b += '</table>\n'
    b += '\n<details>\n<summary>Project stacks and architecture</summary>\n\n'
    for project in PROJECTS:
        b += f'<p><strong>{spaced(project["name"])}</strong> · <sub>{spaced(", ".join(project["tags"]))}</sub></p>\n'
        b += f'<p>{spaced(project["detail"])}</p>\n<p><strong>Flow:</strong> {spaced(project["flow"])}</p>\n\n'
    b += '</details>\n\n' + heading("Tools I reach for") + f'''

<table width="100%">
  <tr>
    <td width="50%" valign="top"><strong>Build&#8196;the&#8196;API</strong><br>{spaced("Node.js · Express · Python · Socket.IO")}</td>
    <td width="50%" valign="top"><strong>Move&#8196;the&#8196;data</strong><br>{spaced("PostgreSQL · MongoDB · Redis · RabbitMQ · BullMQ")}</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>Add&#8196;intelligence</strong><br>{spaced("LangChain · LangGraph · Qdrant · Gemini")}</td>
    <td width="50%" valign="top"><strong>Ship&#8196;the&#8196;thing</strong><br>{spaced("React · Tailwind · Docker · AWS")}</td>
  </tr>
</table>

<p><sub>Also exploring <strong>DSA in C++</strong> and <strong>system design</strong>.</sub></p>

<div align="left">
  <h3>Let's&#8196;build&#8196;something&#8196;good</h3>
  <p>Open to <strong>backend and applied AI opportunities</strong>.<br>
  <a href="mailto:prakash8290682001@gmail.com">Get in touch ↗</a></p>
</div>
'''
    return b


def main():
    from profile_cards import write_cards
    data = json.loads(CACHE.read_text(encoding="utf-8"))
    content = readme(data)
    write_cards(data)
    (ROOT / "README.md").write_text(content, encoding="utf-8")
    print("Generated the compact PNG badges and README.")


if __name__ == "__main__":
    main()
