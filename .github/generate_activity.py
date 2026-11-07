"""Refresh profile activity cards using public GitHub data."""

from collections import Counter
from datetime import date, timedelta
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen

USERNAME = "PrakashPalsaniya"
ROOT = Path(__file__).resolve().parents[1]


def fetch(url):
    headers = {"User-Agent": "PrakashPalsaniya-profile"}
    token = os.environ.get("GH_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                return response.read().decode("utf-8")
        except (OSError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.counts = {}
        self.tooltip = None
        self.tooltip_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "td" and "data-date" in attrs:
            self.cells[attrs["id"]] = attrs["data-date"]
        if tag == "tool-tip" and attrs.get("for") in self.cells:
            self.tooltip = attrs["for"]
            self.tooltip_text = []

    def handle_data(self, data):
        if self.tooltip:
            self.tooltip_text.append(data)

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.tooltip:
            label = "".join(self.tooltip_text).strip()
            match = re.match(r"(No|[\d,]+) contributions? on ", label)
            if not match:
                raise ValueError("GitHub contribution labels changed")
            self.counts[self.cells[self.tooltip]] = 0 if match[1] == "No" else int(match[1].replace(",", ""))
            self.tooltip = None


def calendar(start, end):
    parser = CalendarParser()
    parser.feed(fetch(f"https://github.com/users/{USERNAME}/contributions?from={start}&to={end}"))
    days = {day: count for day, count in parser.counts.items() if str(start) <= day <= str(end)}
    expected = (end - start).days + 1
    if len(days) != expected:
        raise ValueError(f"Incomplete contribution calendar: {len(days)}/{expected} days")
    return days


def collect():
    today = date.today()
    days = {}
    for year in range(2023, today.year + 1):
        days.update(calendar(date(year, 1, 1), min(today, date(year, 12, 31))))
    languages = Counter()
    for page in range(1, 100):
        repos = json.loads(fetch(f"https://api.github.com/users/{USERNAME}/repos?type=owner&per_page=100&page={page}"))
        languages.update(repo["language"] for repo in repos if not repo["fork"] and repo["language"])
        if len(repos) < 100:
            break
    return {"updated": today.isoformat(), "days": days, "languages": dict(languages)}


def text(x, y, value, size, color, weight=400, mono=False, extra=""):
    font = "Consolas,monospace" if mono else "Arial,Helvetica,sans-serif"
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def box(x, y, width, height, fill, radius=12, stroke=None):
    border = f' stroke="{stroke}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{fill}"{border}/>'


def render(data, dark, mobile):
    p = dict(bg="#111827" if dark else "#f4f6fb", panel="#18243a" if dark else "#ffffff", ink="#f4f6ff" if dark else "#14213d", muted="#a5b3cc" if dark else "#56647e", line="#30405b" if dark else "#d4ddeb", accent="#729aff" if dark else "#285bff")
    colors = [p["accent"], "#ff916d" if dark else "#c84b28", "#49d7b1" if dark else "#007b65", "#b49aff" if dark else "#7143d3"]
    today = date.fromisoformat(data["updated"])
    days = data["days"]
    lifetime = sum(days.values())
    annual = sum(count for day, count in days.items() if day >= str(today - timedelta(days=364)))
    recent = sum(count for day, count in days.items() if day >= str(today - timedelta(days=89)))
    width, height = (640, 954) if mobile else (1200, 344)
    card_width = 592 if mobile else 368
    body = box(1, 1, width - 2, height - 2, p["bg"], 18, p["line"])
    body += text(28, 38, "GITHUB / ACTIVITY", 12, p["muted"], 600, True)
    body += text(width - 28, 38, "UPDATED " + today.strftime("%d %b %Y").upper(), 11, p["muted"], mono=True, extra='text-anchor="end"')

    for index, label in enumerate(["CONTRIBUTIONS", "PRIMARY LANGUAGES", "RECENT ACTIVITY"]):
        x, y = (24, 62 + index * 292) if mobile else (24 + index * 392, 62)
        body += box(x, y, card_width, 268, p["panel"], 12, p["line"])
        body += text(x + 22, y + 31, f"0{index + 1} / {label}", 12, p["muted"], 600, True)
        if index == 0:
            body += text(x + 22, y + 119, f"{lifetime:,}", 76 if mobile else 68, p["accent"], 700)
            body += text(x + 24, y + 152, "contributions since Nov 2023", 17, p["muted"])
            body += box(x + 22, y + 182, card_width - 44, 58, p["bg"], 8)
            body += text(x + 38, y + 219, f"{annual:,}", 25, p["ink"], 700)
            body += text(x + card_width - 38, y + 218, "PAST 365 DAYS", 11, p["muted"], mono=True, extra='text-anchor="end"')
        elif index == 1:
            languages = sorted(data["languages"].items(), key=lambda pair: (-pair[1], pair[0]))[:4]
            total = sum(data["languages"].values())
            for row, (language, count) in enumerate(languages):
                by = y + 67 + row * 43
                body += text(x + 22, by, language, 17, p["ink"], 600)
                body += text(x + card_width - 22, by, f"{count} repo" + ("s" if count != 1 else ""), 12, p["muted"], mono=True, extra='text-anchor="end"')
                body += box(x + 22, by + 10, card_width - 44, 5, p["line"], 2)
                body += box(x + 22, by + 10, round((card_width - 44) * count / total, 2), 5, colors[row], 2)
            body += text(x + 22, y + 244, "Public repos / forks excluded", 12, p["muted"])
        else:
            start = today - timedelta(days=89)
            grid_start = start - timedelta(days=(start.weekday() + 1) % 7)
            grid_end = today + timedelta(days=(6 - (today.weekday() + 1) % 7))
            cell, gap = (16, 5) if mobile else (15, 4)
            for offset in range((grid_end - grid_start).days + 1):
                day = grid_start + timedelta(days=offset)
                if day < start or day > today:
                    continue
                count = days.get(str(day), 0)
                color = p["line"] if not count else ["#adc2ff", "#729aff", "#426fff", "#285bff"][min(3, (count - 1) // 3)]
                cell_body = box(x + 22 + (offset // 7) * (cell + gap), y + 62 + (offset % 7) * (cell + gap), cell, cell, color, 3)
                body += f'<g><title>{day}: {count} contributions</title>{cell_body}</g>'
            body += text(x + 22, y + 232, f"{recent:,}", 25, p["ink"], 700)
            body += text(x + card_width - 22, y + 231, "LAST 90 DAYS", 11, p["muted"], mono=True, extra='text-anchor="end"')

    desc = f"{lifetime} GitHub contributions since November 2023; {annual} in the past 365 days. Primary languages across public nonfork repositories: " + ", ".join(f"{name}: {count}" for name, count in sorted(data["languages"].items())) + f". {recent} contributions in the past 90 days. Updated {today}."
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description"><title id="title">Prakash Palsaniya - GitHub activity</title><desc id="description">{escape(desc)}</desc>{body}</svg>\n'


def write_cards(data):
    # Build all variants before replacing any published card.
    cards = {}
    for dark in [False, True]:
        for mobile in [False, True]:
            name = "github-activity" + ("-dark" if dark else "-light") + ("-mobile" if mobile else "") + ".svg"
            cards[name] = render(data, dark, mobile)
    for name, content in cards.items():
        (ROOT / "assets" / name).write_text(content, encoding="utf-8")


if __name__ == "__main__":
    write_cards(collect())
    print("Updated GitHub activity cards.")
