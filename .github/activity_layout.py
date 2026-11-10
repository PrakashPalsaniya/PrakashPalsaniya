"""Render a dated public GitHub snapshot using the profile's visual language."""

from datetime import date, timedelta

from profile_svg import box, circle, frame, label, line, palette, svg, text


def validate(data):
    today = date.fromisoformat(data["updated"])
    first = date(2023, 1, 1)
    expected = {str(first + timedelta(days=i)) for i in range((today - first).days + 1)}
    if set(data["days"]) != expected:
        raise ValueError("Activity snapshot must contain every day from January 2023 through its refresh date")
    if any(type(n) is not int or n < 0 for n in data["days"].values()):
        raise ValueError("Contribution counts must be nonnegative integers")
    if any(not isinstance(name, str) or type(n) is not int or n < 0 for name, n in data["languages"].items()):
        raise ValueError("Language counts must be nonnegative repository counts")


def render(data, dark, mobile):
    p = palette(dark)
    today = date.fromisoformat(data["updated"])
    days = data["days"]
    lifetime = sum(days.values())
    annual = sum(count for day, count in days.items() if str(today - timedelta(days=364)) <= day <= str(today))
    recent = sum(count for day, count in days.items() if str(today - timedelta(days=89)) <= day <= str(today))
    w, h = (640, 1044) if mobile else (1200, 396)
    x = 32 if mobile else 42
    b = frame(w, h, p)
    b += label(x, 43, "GITHUB / THE WORK, OVER TIME", p, p["accent"], size=16 if mobile else 11)
    if mobile:
        b += label(x, 68, "UPDATED " + today.strftime("%d %b %Y").upper(), p, size=16)
    else:
        b += label(w - x, 43, "UPDATED " + today.strftime("%d %b %Y").upper(), p, size=10, extra='text-anchor="end"')
    b += text(x - 3, 177 if mobile else 171, f"{lifetime:,}", 94, p["ink"], 700, extra='letter-spacing="-5"')
    b += text(x, 209 if mobile else 203, "contributions since Nov 2023", 22 if mobile else 18, p["muted"])
    for sx, count, caption in [(x, annual, "PAST 365 DAYS"), (326 if mobile else 228, recent, "PAST 90 DAYS")]:
        b += text(sx, 277, f"{count:,}", 39, p["accent"], 700, extra='letter-spacing="-1"')
        b += label(sx, 301, caption, p, size=16 if mobile else 10)
    if mobile:
        b += line(32, 335, 608, 335, p["line"])
    else:
        b += line(420, 86, 420, 321, p["line"])
        b += line(866, 86, 866, 321, p["line"])

    gx, gy = (32, 411) if mobile else (458, 131)
    b += label(gx, gy - 35, "THE LAST 90 DAYS", p, size=16 if mobile else 11)
    start = today - timedelta(days=89)
    grid_start = start - timedelta(days=(start.weekday() + 1) % 7)
    columns = ((today - grid_start).days // 7) + 1
    step = (576 if mobile else 370) / columns
    cell = min(30 if mobile else 21, step - 5)
    heat = ["#4c642b", "#6c9139", "#94c54c", "#c3f467"] if dark else ["#c4dba4", "#94b86c", "#6a9346", "#456818"]
    for offset in range((today - grid_start).days + 1):
        day = grid_start + timedelta(days=offset)
        if day < start:
            continue
        count = days[str(day)]
        color = p["raised"] if not count else heat[min(3, (count - 1) // 3)]
        b += '<g><title>' + f'{day}: {count} contributions' + '</title>' + box(round(gx + (offset // 7) * step, 2), round(gy + (offset % 7) * (cell + 5), 2), round(cell, 2), round(cell, 2), color, 3) + '</g>'
    foot = gy + 7 * (cell + 5) + 20
    b += text(gx, foot, start.strftime("%d %b") + " — " + today.strftime("%d %b"), 16 if mobile else 11, p["muted"], mono=True)
    legend_x = gx + (425 if mobile else 224)
    b += label(legend_x - 40, foot, "LESS", p, size=13 if mobile else 8)
    for i, color in enumerate([p["raised"]] + heat):
        b += box(legend_x + i * 15, foot - 10, 11, 11, color, 2)
    b += label(legend_x + 80, foot, "MORE", p, size=13 if mobile else 8)

    lx, ly, lw = (32, 765, 576) if mobile else (898, 128, 260)
    if mobile:
        b += line(32, 695, 608, 695, p["line"])
    b += label(lx, ly - 32, "PRIMARY LANGUAGES", p, size=16 if mobile else 11)
    languages = sorted(data["languages"].items(), key=lambda pair: (-pair[1], pair[0]))[:4]
    total = sum(data["languages"].values())
    if not total:
        b += text(lx, ly + 28, "No language data available", 16, p["muted"])
    for row, (language, count) in enumerate(languages):
        by = ly + row * 48
        b += text(lx, by, language, 22 if mobile else 18, p["ink"], 600)
        b += text(lx + lw, by, f"{count} repo" + ("s" if count != 1 else ""), 18 if mobile else 11, p["muted"], mono=True, extra='text-anchor="end"')
        b += box(lx, by + 12, lw, 4, p["line"], 2)
        if total and count:
            b += box(lx, by + 12, round(lw * count / total, 2), 4, p["accent"], 2, extra=f'opacity="{1 - row * .15}"')
    b += line(x, h - 55, w - x, h - 55, p["line"])
    b += circle(x + 4, h - 27, 3, p["accent"])
    b += label(x + 16, h - 23, "PUBLIC GITHUB DATA", p, size=10)
    b += text(w - x, h - 23, "Languages by repo · forks excluded", 10 if mobile else 11, p["muted"], mono=True, extra='text-anchor="end"')
    desc = f"{lifetime} GitHub contributions since November 2023; {annual} in the past 365 days; {recent} in the past 90 days. Primary languages across public nonfork repositories: " + ", ".join(f"{name}: {count}" for name, count in sorted(data["languages"].items())) + f". Updated {today}."
    return svg(w, h, "Prakash Palsaniya — GitHub activity", desc, b)
