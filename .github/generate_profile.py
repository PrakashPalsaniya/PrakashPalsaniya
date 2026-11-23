"""Generate compact GitHub-supported HTML from project copy and public activity."""

from datetime import date, timedelta
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".github" / "activity-data.json"

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
    return f'''<table width="100%">
  <tr>
    <td colspan="3">
      <strong>The work, over time</strong><br>
      <sub>GitHub contributions · Updated {today.strftime("%d %b %Y")}</sub>
    </td>
  </tr>
  <tr>
    <td width="333" align="center" valign="top">
      <sub>ALL TIME</sub>
      <h2>{sum(days.values()):,}</h2>
      <sub>Since {since}</sub>
    </td>
    <td width="333" align="center" valign="top">
      <sub>LAST YEAR</sub>
      <h2>{annual:,}</h2>
      <sub>Past 365 days</sub>
    </td>
    <td width="333" align="center" valign="top">
      <sub>RECENT WORK</sub>
      <h2>{recent:,}</h2>
      <sub>Past 90 days</sub>
    </td>
  </tr>
  <tr>
    <td colspan="3">
      <sub>Primary languages by public repository: {language_text}. Forks excluded.<br>
      <a href="https://github.com/PrakashPalsaniya?tab=overview">View GitHub activity ↗</a></sub>
    </td>
  </tr>
</table>'''


def project_block(project, index):
    categories = ["Document intelligence", "Real-time booking", "Personal finance + AI", "Links / microservices"]
    links = f'<a href="{escape(project["url"], quote=True)}">Live ↗</a>'
    if project["repo"]:
        links += f' · <a href="{escape(project["repo"], quote=True)}">Source code</a>'
    return f'''    <td width="50%" valign="top">
      <strong>{escape(project["name"])}</strong><br>
      <sub>0{index + 1} / {categories[index]}</sub><br>
      {escape(project["description"])}<br>
      <sub>{escape(" · ".join(project["tags"]))}</sub><br>
      {links}
    </td>'''


def readme(data=None):
    if data is None:
        data = json.loads(CACHE.read_text(encoding="utf-8"))
    activity = activity_summary(data)
    b = '''<!-- Generated by .github/generate_profile.py. Edit the generator to keep the profile in sync. -->

<table width="100%">
  <tr>
    <td width="1000">
      <sub>PROFILE / OPEN TO OPPORTUNITIES</sub>
      <h2>Prakash Palsaniya</h2>
      <p><code>Backend development</code> <code>Applied AI</code></p>
      <p>Information Technology at <strong>NIT Srinagar</strong> · Class of <strong>2027</strong></p>
      <p>I build what happens behind the screen: APIs, document search pipelines, background workers, and fast redirects.</p>
      <p>
        <a href="https://prakash-palsaniya.vercel.app/"><strong>Portfolio&nbsp;↗</strong></a> ·
        <a href="https://www.linkedin.com/in/prakash-palsaniya">LinkedIn&nbsp;↗</a> ·
        <a href="https://prakash-palsaniya.vercel.app/Prakash-Palsaniya-Resume.pdf">Résumé&nbsp;↗</a> ·
        <a href="mailto:prakash8290682001@gmail.com">Email&nbsp;↗</a>
      </p>
    </td>
  </tr>
</table>

'''
    b += activity + '\n\n<h3>Selected builds</h3>\n\n<table width="100%">\n'
    for row in range(0, len(PROJECTS), 2):
        b += '  <tr>\n'
        for index in range(row, min(row + 2, len(PROJECTS))):
            b += project_block(PROJECTS[index], index) + '\n'
        b += '  </tr>\n'
    b += '</table>\n'
    b += '\n<details>\n<summary>Project stacks and architecture</summary>\n\n'
    for project in PROJECTS:
        b += f'<p><strong>{escape(project["name"])}</strong> · {escape(", ".join(project["tags"]))}</p>\n'
        b += f'<p>{escape(project["detail"])}</p>\n<p><strong>Flow:</strong> {escape(project["flow"])}</p>\n\n'
    b += '''</details>

<h3>Tools I reach for</h3>

<table width="100%">
  <tr>
    <td width="50%" valign="top"><strong>Build the API</strong><br>Node.js · Express · Python · Socket.IO</td>
    <td width="50%" valign="top"><strong>Move the data</strong><br>PostgreSQL · MongoDB · Redis · RabbitMQ · BullMQ</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><strong>Add intelligence</strong><br>LangChain · LangGraph · Qdrant · Gemini</td>
    <td width="50%" valign="top"><strong>Ship the thing</strong><br>React · Tailwind · Docker · AWS</td>
  </tr>
</table>

<p><sub>Also exploring <strong>DSA in C++</strong> and <strong>system design</strong>.</sub></p>

<div align="left">
  <h3>Let's build something good</h3>
  <p>Open to <strong>backend and applied AI opportunities</strong>.<br>
  <a href="mailto:prakash8290682001@gmail.com">Get in touch ↗</a></p>
</div>
'''
    return b


def main():
    (ROOT / "README.md").write_text(readme(), encoding="utf-8")
    print("Generated the compact HTML profile README.")


if __name__ == "__main__":
    main()
