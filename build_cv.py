"""Render the shared homepage data as a downloadable, print-ready CV."""

from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
)


ROOT = Path(__file__).resolve().parent
INK = colors.HexColor("#202522")
MUTED = colors.HexColor("#58635e")
ACCENT = colors.HexColor("#176653")


def text(value):
    return escape(str(value), quote=True)


def anchor(label, href):
    return f'<a href="{text(href)}" color="#176653">{text(label)}</a>'


def build_cv(data, output):
    """Generate a deterministic PDF; fail the site build if generation fails."""
    for name, filename in [
        ("CV", "SourceSerif4-Regular.ttf"),
        ("CV-Bold", "SourceSerif4-Semibold.ttf"),
        ("CV-Sans", "SourceSans3-Regular.ttf"),
        ("CV-SansBold", "SourceSans3-Semibold.ttf"),
    ]:
        pdfmetrics.registerFont(TTFont(name, str(ROOT / "assets" / "fonts" / filename)))
    pdfmetrics.registerFontFamily("CV", normal="CV", bold="CV-Bold")
    pdfmetrics.registerFontFamily("CV-Sans", normal="CV-Sans", bold="CV-SansBold")
    styles = {
        "body": ParagraphStyle("body", fontName="CV", fontSize=9.5, leading=13, textColor=INK, spaceAfter=5),
        "muted": ParagraphStyle("muted", fontName="CV-Sans", fontSize=8.5, leading=11.5, textColor=MUTED, spaceAfter=4),
        "title": ParagraphStyle("title", fontName="CV-Bold", fontSize=10.5, leading=14, textColor=INK, spaceAfter=3),
        "section": ParagraphStyle("section", fontName="CV-SansBold", fontSize=11, leading=15, textColor=ACCENT, spaceBefore=12, spaceAfter=8, keepWithNext=True),
        "name": ParagraphStyle("name", fontName="CV", fontSize=28, leading=32, textColor=INK, spaceAfter=5),
        "role": ParagraphStyle("role", fontName="CV-Sans", fontSize=11, leading=16, textColor=ACCENT, spaceAfter=8),
    }
    profile = data["profile"]
    story = []

    def p(value, style="body", markup=False):
        return Paragraph(value if markup else text(value), styles[style])

    def heading(value):
        story.append(p(value, "section"))

    def entry(parts):
        story.append(KeepTogether(parts + [Spacer(1, 7)]))

    def date(item):
        return item["date"] + (f" - {item['dateEnd']}" if item.get("dateEnd") else "")

    def experience(section):
        heading(section["title"])
        for item in section["entries"]:
            parts = [p(item.get("role", item.get("title", "")), "title")]
            meta = [item.get("organization"), item.get("subtitle"), date(item)]
            parts.append(p(" | ".join(value for value in meta if value), "muted"))
            description = item.get("description") or item.get("summary")
            if description:
                parts.append(p(description))
            parts.extend(p("- " + bullet) for bullet in item.get("bullets", []))
            entry(parts)

    story.extend([p(profile["name"], "name"), p(profile["role"], "role")])
    contacts = [anchor(item["label"], item["href"]) for item in profile["links"] if not item.get("download") and item["href"] != profile["cv"]]
    story.append(p(anchor(profile["email"], "mailto:" + profile["email"]), "body", True))
    story.append(p(" &nbsp; | &nbsp; ".join(contacts), "muted", True))
    story.extend([Spacer(1, 8), HRFlowable(width="100%", thickness=.6, color=colors.HexColor("#cdd8d2")), Spacer(1, 12)])
    story.extend(p(paragraph) for paragraph in data["summary"]["paragraphs"])

    heading(data["education"]["title"])
    for item in data["education"]["entries"]:
        parts = [p(item["title"], "title"), p(date(item), "muted")]
        parts.extend(p(line) for line in item.get("lines", []))
        entry(parts)

    publications = data["publications"]
    heading(publications["title"])
    for item in publications["entries"]:
        venues = item.get("venues") or [{"label": item.get("venue", item["year"]), "href": item.get("venueHref")}]
        venue_text = " &nbsp; | &nbsp; ".join(anchor(v["label"], v["href"]) if v.get("href") else text(v["label"]) for v in venues)
        authors = ", ".join(f"<b>{text(a)}</b>" if a == publications["highlightAuthor"] else text(a) for a in item["authors"])
        parts = [p(item["title"], "title"), p(authors, "body", True), p(venue_text, "muted", True)]
        if item.get("links"):
            parts.append(p(" &nbsp; | &nbsp; ".join(anchor(link["label"], link["href"]) for link in item["links"]), "muted", True))
        entry(parts)

    story.append(PageBreak())
    experience(data["workExperience"])
    experience(data["industrialProject"])
    story.append(PageBreak())
    experience(data["teaching"])
    for key in ("invitedTalk", "service"):
        section = data[key]
        heading(section["title"])
        for item in section["entries"]:
            if isinstance(item, str):
                story.append(p(item))
            else:
                value = text(item["text"])
                if item.get("href") and item.get("linkText"):
                    value = value.replace(text(item["linkText"]), anchor(item["linkText"], item["href"]), 1)
                story.append(p(value, markup=True))

    heading(data["awards"]["title"])
    for item in sorted(data["awards"]["items"], key=lambda a: a.get("sortDate", a.get("date", "")), reverse=True):
        story.append(p(f'<b>{text(item["date"])}</b> &nbsp; {text(item["text"])}', markup=True))
    heading(data["skills"]["title"])
    if data["skills"].get("languages"):
        story.append(p("<b>Languages:</b> " + text(", ".join(data["skills"]["languages"])), markup=True))
    for group in data["skills"]["groups"]:
        story.append(p(f'<b>{text(group["label"])}:</b> {text(", ".join(group["items"]))}', markup=True))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("CV-Sans", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(18 * mm, 12 * mm, profile["name"] + " | Curriculum Vitae")
        canvas.drawRightString(A4[0] - 18 * mm, 12 * mm, str(doc.page))
        canvas.restoreState()

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".tmp.pdf")
    try:
        doc = SimpleDocTemplate(str(temporary), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
                                topMargin=16 * mm, bottomMargin=20 * mm, title=profile["name"] + " - CV",
                                author=profile["name"], invariant=1)
        doc.build(story, onFirstPage=footer, onLaterPages=footer)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
