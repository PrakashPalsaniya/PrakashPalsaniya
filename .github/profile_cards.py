"""Small PNG title and contribution badges with explicit display dimensions."""

from datetime import date, timedelta
from functools import lru_cache
from io import BytesIO
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageColor, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SCALE = 2


@lru_cache(maxsize=12)
def font(family, size):
    filename = {"Public Sans": "public-sans-400-normal.woff2",
                "Public Sans Medium": "public-sans-500-normal.woff2",
                "Public Sans Bold": "public-sans-600-normal.woff2"}[family]
    face = TTFont(ROOT / ".github" / "fonts" / filename)
    face.flavor = None
    buffer = BytesIO()
    face.save(buffer)
    buffer.seek(0)
    return ImageFont.truetype(buffer, size * SCALE)


def background(width, height, start, end, border, radius):
    width, height = width * SCALE, height * SCALE
    image = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(image)
    first, last = ImageColor.getrgb(start), ImageColor.getrgb(end)
    for x in range(width):
        mix = x / (width - 1)
        color = tuple(round(a + (b - a) * mix) for a, b in zip(first, last))
        draw.line((x, 0, x, height), fill=color)
    mask = Image.new("L", image.size)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius=radius * SCALE, fill=255)
    image.putalpha(mask)
    ImageDraw.Draw(image).rounded_rectangle((0, 0, width - 1, height - 1), radius=radius * SCALE,
                                            outline=border, width=SCALE)
    return image


def label(image, position, value, family, size, color, anchor="la", word_spacing=1.2):
    face = font(family, size)
    words = value.split(" ")
    gap = face.getlength(" ") + word_spacing * SCALE
    width = sum(face.getlength(word) for word in words) + gap * (len(words) - 1)
    x, y = (n * SCALE for n in position)
    if anchor[0] == "r":
        x -= width
    elif anchor[0] == "m":
        x -= width / 2
    draw = ImageDraw.Draw(image)
    for word in words:
        draw.text((x, y), word, font=face, fill=color, anchor="l" + anchor[1])
        x += face.getlength(word) + gap


def png(image):
    output = BytesIO()
    image.save(output, format="PNG", optimize=True)
    return output.getvalue()


def header(dark):
    image = background(320, 64, "#14243d" if dark else "#e2f3ff", "#322444" if dark else "#ede4ff",
                       "#41516a" if dark else "#cbd8ee", 10)
    label(image, (14, 6), "Prakash Palsaniya", "Public Sans Bold", 24,
          "#f1f5ff" if dark else "#18294b", word_spacing=1.8)
    label(image, (15, 39), "Backend development · Applied AI", "Public Sans", 12,
          "#c7c9f1" if dark else "#555487")
    return png(image)


def activity_badge(caption, count, dark, index):
    colors = [
        ("#17364a", "#1b2b40", "#7dd3fc") if dark else ("#dff3fe", "#ecf7ff", "#08638b"),
        ("#352a4d", "#26243b", "#c4b5fd") if dark else ("#ebe2fc", "#f3edff", "#6b3ca4"),
        ("#473326", "#312726", "#fcd38a") if dark else ("#ffedd4", "#fff6e8", "#935315"),
    ]
    start, end, accent = colors[index]
    image = background(128, 36, start, end, "#41516a" if dark else "#cbd8ee", 7)
    label(image, (10, 18), caption, "Public Sans Medium", 11, accent, "lm")
    size = 18
    value = f"{count:,}"
    while font("Public Sans Bold", size).getlength(value) > 50 * SCALE and size > 9:
        size -= 1
    label(image, (118, 18), value, "Public Sans Bold", size, accent, "rm")
    return png(image)


def write_cards(data):
    today = date.fromisoformat(data["updated"])
    days = data["days"]
    counts = [sum(days.values()),
              sum(n for day, n in days.items() if str(today - timedelta(days=364)) <= day <= str(today)),
              sum(n for day, n in days.items() if str(today - timedelta(days=89)) <= day <= str(today))]
    badges = {}
    for dark in [False, True]:
        theme = "dark" if dark else "light"
        badges[f"profile-title-{theme}.png"] = header(dark)
        for index, (name, caption, count) in enumerate(zip(["total", "year", "recent"],
                                                        ["All time", "365 days", "90 days"], counts)):
            badges[f"contributions-{name}-{theme}.png"] = activity_badge(caption, count, dark, index)
    # Finish every render before replacing any published badge.
    for name, content in badges.items():
        (ROOT / "assets" / name).write_bytes(content)
