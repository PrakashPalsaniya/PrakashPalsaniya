"""Refresh public GitHub activity and the native HTML profile."""

import argparse
from collections import Counter
from datetime import date, datetime, timezone
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen

from generate_profile import readme

USERNAME = "PrakashPalsaniya"
ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".github" / "activity-data.json"


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
    today = datetime.now(timezone.utc).date()
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cached", action="store_true", help="Regenerate the README from the saved snapshot without network access")
    args = parser.parse_args()
    data = json.loads(CACHE.read_text(encoding="utf-8")) if args.cached else collect()
    # Validate the complete snapshot and render before updating published files.
    content = readme(data)
    if not args.cached:
        CACHE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    (ROOT / "README.md").write_text(content, encoding="utf-8")
    print(f'Updated profile activity from the {data["updated"]} GitHub snapshot.')
