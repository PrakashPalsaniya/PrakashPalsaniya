"""Outline bundled fonts so GitHub SVG images keep their typography."""

from functools import lru_cache
from pathlib import Path
import xml.etree.ElementTree as ET

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

NS = "http://www.w3.org/2000/svg"
FONTS = Path(__file__).parent / "fonts"
ET.register_namespace("", NS)


@lru_cache(maxsize=3)
def font(family):
    filename = {
        "Sora": "sora-700-normal.woff2",
        "Public Sans": "public-sans-400-normal.woff2",
        "IBM Plex Mono": "ibm-plex-mono-400-normal.woff2",
    }[family]
    face = TTFont(FONTS / filename)
    return face, face.getGlyphSet(), face.getBestCmap(), face["head"].unitsPerEm


def outline(element):
    value = "".join(element.itertext())
    size = float(element.get("font-size", "16"))
    family = element.get("data-font", "Public Sans")
    face, glyphs, cmap, units = font(family)
    spacing = float(element.get("letter-spacing", "0"))
    scale = size / units
    runs, width = [], 0
    for character in value:
        if ord(character) not in cmap:
            raise ValueError(f"Missing {family} glyph: {character!r}")
        name = cmap[ord(character)]
        runs.append((name, width))
        width += face["hmtx"].metrics[name][0] * scale + spacing
    if runs:
        width -= spacing
    x, y = float(element.get("x", "0")), float(element.get("y", "0"))
    anchor = element.get("text-anchor", "start")
    if anchor == "end":
        x -= width
    elif anchor == "middle":
        x -= width / 2
    pen = SVGPathPen(glyphs, ntos=lambda n: f"{n:.2f}".rstrip("0").rstrip(".") or "0")
    for name, offset in runs:
        glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x + offset, y)))
    group = ET.Element(f"{{{NS}}}g", {"data-font": family, "data-text": value, "aria-label": value})
    ET.SubElement(group, f"{{{NS}}}path", {"d": pen.getCommands(), "fill": element.get("fill", "#fff")})
    return group


def outline_svg(content):
    root = ET.fromstring(content)
    for parent in root.iter():
        for index, element in enumerate(list(parent)):
            if element.tag == f"{{{NS}}}text":
                parent.remove(element)
                parent.insert(index, outline(element))
    return ET.tostring(root, encoding="unicode") + "\n"
