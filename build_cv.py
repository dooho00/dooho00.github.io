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
    HRFlowable, Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table,
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
        "body": ParagraphStyle("body", fontName="CV", fontSize=9.5, leading=12, textColor=INK, spaceAfter=2),
        "muted": ParagraphStyle("muted", fontName="CV-Sans", fontSize=8.5, leading=10.5, textColor=MUTED, spaceAfter=2),
        "title": ParagraphStyle("title", fontName="CV-Bold", fontSize=10.5, leading=13, textColor=INK, spaceAfter=2),
        "section": ParagraphStyle("section", fontName="CV-SansBold", fontSize=11, leading=14, textColor=ACCENT, spaceAfter=5, keepWithNext=True),
        "name": ParagraphStyle("name", fontName="CV", fontSize=28, leading=32, textColor=INK, spaceAfter=5),
        "role": ParagraphStyle("role", fontName="CV-Sans", fontSize=11, leading=16, textColor=ACCENT, spaceAfter=8),
    }
    profile = data["profile"]
    story = []

    def p(value, style="body", markup=False):
        return Paragraph(value if markup else text(value), styles[style])

    def heading(value):
        story.append(Spacer(1, 7))
        story.append(p(value, "section"))

    def entry(parts):
        story.append(KeepTogether(parts + [Spacer(1, 3)]))

    def date(item):
        return item["date"] + (f" - {item['dateEnd']}" if item.get("dateEnd") else "")

    def experience(section):
        heading(section["title"])
        for item in section["entries"]:
            parts = [p(item.get("role", item.get("title", "")), "title")]
            meta = [item.get("organization"), item.get("subtitle"), date(item)]
            meta_text = []
            for value in meta:
                if value:
                    href = next((link["href"] for link in data.get("inlineLinks", []) if link["label"] == value), None)
                    meta_text.append(anchor(value, href) if href else text(value))
            parts.append(p(" | ".join(meta_text), "muted", True))
            description = item.get("description") or item.get("summary")
            if description:
                parts.append(p(description))
            parts.extend(p("- " + bullet) for bullet in item.get("bullets", []))
            entry(parts)

    contacts = [anchor(item["label"], item["href"]) for item in profile["links"]
                if not item.get("download") and item["href"] != profile["cv"]
                and not item["href"].startswith("mailto:")]
    identity = [p(profile["name"], "name"), p(profile["role"], "role"),
                p(anchor(profile["email"], "mailto:" + profile["email"]), "body", True),
                p(" &nbsp; | &nbsp; ".join(contacts), "muted", True)]
    photo = Image(str(ROOT / profile["photo"]), width=27 * mm, height=32 * mm, kind="proportional")
    photo.hAlign = "RIGHT"
    header = Table([[identity, photo]], colWidths=[A4[0] - 62 * mm - 12, 30 * mm], style=[
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ])
    story.extend([header, Spacer(1, 7), HRFlowable(width="100%", thickness=.6, color=colors.HexColor("#cdd8d2")), Spacer(1, 7)])
    story.extend(p(paragraph) for paragraph in data["summary"]["paragraphs"])

    heading(data["education"]["title"])
    for item in data["education"]["entries"]:
        parts = [p(item["title"], "title"),
                 p(" | ".join([date(item)] + item.get("lines", [])), "muted")]
        entry(parts)

    heading(data["models"]["title"])
    for model in data["models"]["entries"]:
        entry([
            p(model["name"] + " | " + model["organization"], "title"),
            p(model["description"]),
            p(" &nbsp; | &nbsp; ".join(anchor(link["label"], link["href"]) for link in model["links"]), "muted", True),
        ])

    for key in ("publications", "preprints"):
        publications = data[key]
        heading(publications["title"])
        for item in publications["entries"]:
            venues = item.get("venues") or [{"label": item.get("venue", item["year"]), "href": item.get("venueHref")}]
            venue_text = " &nbsp; | &nbsp; ".join(anchor(v["label"], v["href"]) if v.get("href") else text(v["label"]) for v in venues)
            authors = ", ".join(f"<b>{text(a)}</b>" if a == publications["highlightAuthor"] else text(a) for a in item["authors"])
            parts = [p(item["title"], "title"), p(authors, "body", True)]
            if item.get("links"):
                venue_text += " &nbsp; | &nbsp; " + " &nbsp; | &nbsp; ".join(anchor(link["label"], link["href"]) for link in item["links"])
            parts.append(p(venue_text, "muted", True))
            entry(parts)

    experience(data["workExperience"])
    experience(data["industrialProject"])
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

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("CV-Sans", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(16 * mm, 10 * mm, profile["name"] + " | Curriculum Vitae")
        canvas.drawRightString(A4[0] - 16 * mm, 10 * mm, str(doc.page))
        canvas.restoreState()

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".tmp.pdf")
    try:
        doc = SimpleDocTemplate(str(temporary), pagesize=A4, rightMargin=16 * mm, leftMargin=16 * mm,
                                topMargin=14 * mm, bottomMargin=17 * mm, title=profile["name"] + " - CV",
                                author=profile["name"], invariant=1)
        doc.build(story, onFirstPage=footer, onLaterPages=footer)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
