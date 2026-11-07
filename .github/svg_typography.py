"""Draw self-contained SVG lettering with the profile's bundled fonts."""

from functools import lru_cache
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

NS = "http://www.w3.org/2000/svg"
FONTS = Path(__file__).parent / "fonts"
ET.register_namespace("", NS)


@lru_cache(maxsize=20)
def font(family, weight):
    if family == "IBM Plex Mono":
        variant = "SemiBold" if weight >= 600 else "Medium" if weight >= 500 else "Regular"
        path = FONTS / "ibmplexmono" / f"IBMPlexMono-{variant}.ttf"
        face = TTFont(path)
    else:
        filename = "Sora.ttf" if family == "Sora" else "Inter.ttf"
        face = TTFont(FONTS / family.lower() / filename)
        axes = {"wght": weight}
        if family == "Inter":
            axes["opsz"] = 14
        face = instantiateVariableFont(face, axes, inplace=True)
    return face, face.getGlyphSet(), face.getBestCmap(), face["head"].unitsPerEm


def outline(element):
    value = "".join(element.itertext())
    size = float(element.get("font-size", "16"))
    weight = int(element.get("font-weight", "400"))
    mono = "monospace" in element.get("font-family", "") or re.fullmatch(r"[\d,]+", value)
    family = "IBM Plex Mono" if mono else "Sora" if size >= 40 else "Inter"
    if family == "Sora":
        weight = 700
    face, glyphs, cmap, units = font(family, weight)
    spacing = float(element.get("letter-spacing", "0"))
    runs = []
    width = 0
    for character in value:
        char_face, char_glyphs, char_cmap, char_units = face, glyphs, cmap, units
        if ord(character) not in cmap:
            char_face, char_glyphs, char_cmap, char_units = font("Inter", weight)
        if ord(character) not in char_cmap:
            raise ValueError(f"Missing font glyph: {character!r}")
        name = char_cmap[ord(character)]
        char_scale = size / char_units
        advance = char_face["hmtx"].metrics[name][0] * char_scale
        runs.append((char_glyphs, name, char_scale, width))
        width += advance + spacing
    if runs:
        width -= spacing
    x, y = float(element.get("x", "0")), float(element.get("y", "0"))
    anchor = element.get("text-anchor", "start")
    if anchor == "end":
        x -= width
    elif anchor == "middle":
        x -= width / 2
    pen = SVGPathPen(glyphs, ntos=lambda number: f"{number:.2f}".rstrip("0").rstrip(".") or "0")
    for char_glyphs, name, char_scale, offset in runs:
        pen.glyphSet = char_glyphs
        char_glyphs[name].draw(TransformPen(pen, (char_scale, 0, 0, -char_scale, x + offset, y)))
    group = ET.Element(f"{{{NS}}}g", {"data-font": family, "data-text": value, "aria-label": value})
    if element.get("transform"):
        group.set("transform", element.get("transform"))
    ET.SubElement(group, f"{{{NS}}}path", {"d": pen.getCommands(), "fill": element.get("fill", "#14213d")})
    return group


def outline_svg(content):
    root = ET.fromstring(content)
    for parent in root.iter():
        for index, element in enumerate(list(parent)):
            if element.tag == f"{{{NS}}}text":
                parent.remove(element)
                parent.insert(index, outline(element))
    return ET.tostring(root, encoding="unicode") + "\n"
