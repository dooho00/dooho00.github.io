#!/usr/bin/env python3
"""Generate the static homepage from data/site.json.

The generated index.html is intentionally plain static HTML so it works when
opened directly from the filesystem and on GitHub Pages without any build
service.
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "site.json"
OUTPUT_PATH = ROOT / "index.html"


def e(value: Any) -> str:
    return escape(str(value), quote=True)


def rich_text(value: Any, links: list[dict[str, Any]]) -> str:
    text = e(value)
    matches: list[tuple[int, int, dict[str, Any]]] = []
    for item in sorted(links, key=lambda link_item: len(link_item["label"]), reverse=True):
        label = e(item["label"])
        start = 0
        while True:
            index = text.find(label, start)
            if index == -1:
                break
            end = index + len(label)
            overlaps = any(not (end <= match_start or index >= match_end) for match_start, match_end, _ in matches)
            if not overlaps:
                matches.append((index, end, item))
            start = end
    if not matches:
        return text

    output = []
    cursor = 0
    for start, end, item in sorted(matches, key=lambda match: match[0]):
        output.append(text[cursor:start])
        output.append(f'<a href="{e(item["href"])}">{text[start:end]}</a>')
        cursor = end
    output.append(text[cursor:])
    return "".join(output)


def indent(text: str, spaces: int) -> str:
    pad = " " * spaces
    return "\n".join(f"{pad}{line}" if line else "" for line in text.splitlines())


def attrs(**kwargs: Any) -> str:
    parts = []
    for key, value in kwargs.items():
        attr_name = key[:-1] if key.endswith("_") else key
        attr_name = attr_name.replace("_", "-")
        if value is True:
            parts.append(attr_name)
        elif value:
            parts.append(f'{attr_name}="{e(value)}"')
    return (" " + " ".join(parts)) if parts else ""


def link(item: dict[str, Any]) -> str:
    icon = icon_svg(item.get("icon"))
    return (
        f"<a class=\"icon-link\"{attrs(href=item['href'], download=item.get('download'))}>"
        f"{icon}<span>{e(item['label'])}</span></a>"
    )


def icon_svg(name: str | None) -> str:
    icons = {
        "email": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16v12H4V6Z"/><path d="m4 7 8 6 8-6"/></svg>',
        "scholar": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 4 9 5-9 5-9-5 9-5Z"/><path d="M6 12v4c2 2 10 2 12 0v-4"/><path d="M21 9v6"/></svg>',
        "linkedin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.5 10v8"/><path d="M6.5 6v.1"/><path d="M11 18v-8"/><path d="M11 13.5c0-2 1.2-3.5 3.2-3.5 2.1 0 3.3 1.4 3.3 3.8V18"/></svg>',
        "cv": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h7l4 4v14H7V3Z"/><path d="M14 3v5h4"/><path d="M10 13h5"/><path d="M10 17h5"/></svg>',
    }
    return icons.get(name or "", "")


def author_list(authors: list[str], highlight: str) -> str:
    rendered = [
        f'<span class="author-highlight">{e(author)}</span>' if author == highlight else e(author)
        for author in authors
    ]
    if len(rendered) <= 1:
        return "".join(rendered)
    return f"{', '.join(rendered[:-1])}, and {rendered[-1]}"


def paragraph(text: str, class_name: str | None = None, links: list[dict[str, Any]] | None = None) -> str:
    return f"<p{attrs(class_=class_name)}>{rich_text(text, links or [])}</p>"


def simple_list(items: list[str], links: list[dict[str, Any]] | None = None) -> str:
    lines = "\n".join(f"<li>{rich_text(item, links or [])}</li>" for item in items)
    return f'<ul class="simple-list">\n{lines}\n</ul>'


def chips(items: list[str]) -> str:
    body = "\n".join(f"            <span>{e(item)}</span>" for item in items)
    return f'          <div class="chips">\n{body}\n          </div>'


def section(section_id: str, title: str, body: str) -> str:
    return f"""        <section id="{e(section_id)}" class="section">
          <h2>{e(title)}</h2>
{body}
        </section>"""


def render_profile(data: dict[str, Any]) -> str:
    profile = data["profile"]
    inline_links = data.get("inlineLinks", [])
    links = "\n".join(f"            {link(item)}" for item in profile["links"])
    return f"""      <header class="profile">
        <img src="{e(profile['photo'])}" alt="{e(profile['photoAlt'])}" />
        <div>
          <h1>{e(profile['name'])}</h1>
          <p class="role">{rich_text(profile['role'], inline_links)}</p>
          <p class="tagline">{rich_text(profile['tagline'], inline_links)}</p>
          <div class="links" aria-label="Profile links">
{links}
          </div>
        </div>
      </header>"""


def render_nav(data: dict[str, Any]) -> str:
    items = "\n".join(f'        <a href="{e(item["href"])}">{e(item["label"])}</a>' for item in data["nav"])
    return f"""      <nav class="anchor-nav" aria-label="Section navigation">
{items}
      </nav>"""


def render_summary(data: dict[str, Any]) -> str:
    summary = data["summary"]
    inline_links = data.get("inlineLinks", [])
    paragraphs = "\n".join(f"          {paragraph(text, links=inline_links)}" for text in summary["paragraphs"])
    if summary.get("chips"):
        paragraphs = f"{paragraphs}\n{chips(summary['chips'])}"
    return section(summary["id"], summary["title"], paragraphs)


def timeline_heading(entry: dict[str, Any], links: list[dict[str, Any]]) -> list[str]:
    if entry.get("organization") or entry.get("role"):
        parts = []
        if entry.get("organization"):
            parts.append(f'                <h3 class="entry-org">{rich_text(entry["organization"], links)}</h3>')
        if entry.get("role"):
            parts.append(f'                <p class="entry-role">{rich_text(entry["role"], links)}</p>')
        return parts
    return [f"                <h3>{rich_text(entry['title'], links)}</h3>"]


def render_timeline_section(item: dict[str, Any], links: list[dict[str, Any]]) -> str:
    rows = []
    for entry in item["entries"]:
        date = e(entry["date"])
        if entry.get("dateEnd"):
            date = f'{date}<span class="date-end">- {e(entry["dateEnd"])}</span>'
        parts = timeline_heading(entry, links)
        if entry.get("subtitle"):
            parts.append(f'                <p class="muted">{rich_text(entry["subtitle"], links)}</p>')
        for index, line in enumerate(entry.get("lines", [])):
            class_name = "muted" if index > 0 or len(entry.get("lines", [])) == 1 else None
            parts.append(f"                {paragraph(line, class_name, links)}")
        if entry.get("bullets"):
            parts.append(indent(simple_list(entry["bullets"], links), 16))
        body = "\n".join(parts)
        rows.append(
            f"""            <article class="timeline-row">
              <div class="date">{date}</div>
              <div>
{body}
              </div>
            </article>"""
        )
    timeline = f'          <div class="timeline">\n' + "\n".join(rows) + "\n          </div>"
    return section(item["id"], item["title"], timeline)


def date_range(entry: dict[str, Any]) -> str:
    if entry.get("dateEnd"):
        return f'{e(entry["date"])} - {e(entry["dateEnd"])}'
    return e(entry["date"])


def render_expandable_entries_body(item: dict[str, Any], links: list[dict[str, Any]]) -> str:
    rows = []
    for entry in item["entries"]:
        meta_items = []
        if entry.get("organization"):
            meta_items.append(rich_text(entry["organization"], links))
        if entry.get("subtitle"):
            meta_items.append(rich_text(entry["subtitle"], links))
        meta_items.append(date_range(entry))
        meta = "".join(f"<span>{item}</span>" for item in meta_items)
        role = entry.get("role", entry.get("title", ""))
        summary = ""
        if entry.get("summary"):
            summary = f'\n                  <span class="entry-impact">{rich_text(entry["summary"], links)}</span>'
        if entry.get("description"):
            body = f"""              <details class="expandable-details">
                <summary>
                  <span class="entry-role-title">{rich_text(role, links)}</span>
                  <span class="entry-meta">{meta}</span>{summary}
                </summary>
                <p>{rich_text(entry["description"], links)}</p>
              </details>"""
        elif entry.get("bullets"):
            body = f"""              <details class="expandable-details">
                <summary>
                  <span class="entry-role-title">{rich_text(role, links)}</span>
                  <span class="entry-meta">{meta}</span>{summary}
                </summary>
{indent(simple_list(entry["bullets"], links), 16)}
              </details>"""
        else:
            body = f"""              <div class="entry-header">
                <span class="entry-role-title">{rich_text(role, links)}</span>
                <span class="entry-meta">{meta}</span>{summary}
              </div>"""
        rows.append(
            f"""            <article class="expandable-entry">
{body}
            </article>"""
        )
    return f'          <div class="entry-list">\n' + "\n".join(rows) + "\n          </div>"


def render_expandable_entries(item: dict[str, Any], links: list[dict[str, Any]]) -> str:
    return section(item["id"], item["title"], render_expandable_entries_body(item, links))


def render_publications(data: dict[str, Any]) -> str:
    item = data["publications"]
    rows = []
    for entry in item["entries"]:
        venue_label = entry.get("venue", entry["year"])
        if entry.get("venueHref"):
            venue = f'<a href="{e(entry["venueHref"])}">{e(venue_label)}</a>'
        else:
            venue = e(venue_label)
        parts = [
            f"                <h3>{e(entry['title'])}</h3>",
            f"                <p class=\"authors\">{author_list(entry['authors'], item['highlightAuthor'])}</p>",
        ]
        if entry.get("links"):
            link_items = "\n".join(
                f'                  <a href="{e(link_item["href"])}">{e(link_item["label"])}</a>'
                for link_item in entry["links"]
            )
            parts.append(f'                <div class="pub-links">\n{link_items}\n                </div>')
        details = "\n".join(parts)
        rows.append(
            f"""            <article class="publication">
              <div class="pub-year">{venue}</div>
              <div>
{details}
              </div>
            </article>"""
        )
    body = f'          <div class="publication-list">\n' + "\n".join(rows) + "\n          </div>"
    return section(item["id"], item["title"], body)


def render_skills(data: dict[str, Any]) -> str:
    item = data["skills"]
    inline_links = data.get("inlineLinks", [])
    languages = ""
    if item.get("languages"):
        languages = (
            f'          <p class="skill-language"><strong>Languages:</strong> '
            f'{rich_text(", ".join(item["languages"]), inline_links)}</p>\n'
        )
    cards = [
        f"""            <article class="skill-card">
              <h3>{e(group['label'])}</h3>
              <p>{rich_text(', '.join(group['items']), inline_links)}</p>
            </article>"""
        for group in item["groups"]
    ]
    body = f'{languages}          <div class="skill-card-grid">\n' + "\n".join(cards) + "\n          </div>"
    return section(item["id"], item["title"], body)


def render_awards(data: dict[str, Any]) -> str:
    item = data["awards"]
    inline_links = data.get("inlineLinks", [])
    rows = []
    for award in sorted(item["items"], key=lambda award: award.get("sortDate", award.get("date", "")), reverse=True):
        tags = "".join(f'<span class="award-tag">{e(tag)}</span>' for tag in award.get("tags", []))
        rows.append(
            f"""            <li class="award-row">
              <span class="award-date">{e(award['date'])}</span>
              <span class="award-text">{rich_text(award['text'], inline_links)}</span>
              <span class="award-tags">{tags}</span>
            </li>"""
        )
    body = f'          <ul class="award-list">\n' + "\n".join(rows) + "\n          </ul>"
    return section(item["id"], item["title"], body)


def render_linked_list_body(item: dict[str, Any], links: list[dict[str, Any]]) -> str:
    rows = []
    for entry in item["entries"]:
        if isinstance(entry, str):
            rows.append(f"            <li>{rich_text(entry, links)}</li>")
            continue
        text = e(entry["text"])
        if entry.get("href") and entry.get("linkText"):
            linked = f'<a href="{e(entry["href"])}">{e(entry["linkText"])}</a>'
            text = text.replace(e(entry["linkText"]), linked, 1)
        else:
            text = rich_text(entry["text"], links)
        rows.append(f"            <li>{text}</li>")
    return f'          <ul class="simple-list">\n' + "\n".join(rows) + "\n          </ul>"


def render_linked_list(item: dict[str, Any], links: list[dict[str, Any]]) -> str:
    return section(item["id"], item["title"], render_linked_list_body(item, links))


def subsection(title: str, body: str) -> str:
    nested_body = indent(body, 2)
    return f"""          <div class="subsection">
            <h3 class="subsection-title">{e(title)}</h3>
{nested_body}
          </div>"""


def render_experience(data: dict[str, Any]) -> str:
    inline_links = data.get("inlineLinks", [])
    body = "\n".join(
        [
            subsection(data["industrialProject"]["title"], render_expandable_entries_body(data["industrialProject"], inline_links)),
            subsection(data["workExperience"]["title"], render_expandable_entries_body(data["workExperience"], inline_links)),
            subsection(data["teaching"]["title"], render_expandable_entries_body(data["teaching"], inline_links)),
            subsection(data["invitedTalk"]["title"], render_linked_list_body(data["invitedTalk"], inline_links)),
            subsection(data["service"]["title"], render_linked_list_body(data["service"], inline_links)),
        ]
    )
    return section("experience", "Experience", body)


def render_html(data: dict[str, Any]) -> str:
    meta = data["meta"]
    inline_links = data.get("inlineLinks", [])
    sections = "\n\n".join(
        [
            render_summary(data),
            render_timeline_section(data["education"], inline_links),
            render_publications(data),
            render_experience(data),
            render_awards(data),
            render_skills(data),
        ]
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{e(meta['description'])}" />
    <meta property="og:title" content="{e(meta['ogTitle'])}" />
    <meta property="og:description" content="{e(meta['ogDescription'])}" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="{e(meta['ogImage'])}" />
    <title>{e(meta['title'])}</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <div class="site-shell">
{render_profile(data)}

{render_nav(data)}

      <main>
{sections}
      </main>

      <footer>
        <p>{e(data['profile']['name'])} - <a href="mailto:{e(data['profile']['email'])}">{e(data['profile']['email'])}</a></p>
      </footer>
    </div>
  </body>
</html>
"""


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    OUTPUT_PATH.write_text(render_html(data), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} from {DATA_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
