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
    rendered = [f"<strong>{e(author)}</strong>" if author == highlight else e(author) for author in authors]
    if len(rendered) <= 1:
        return "".join(rendered)
    return f"{', '.join(rendered[:-1])}, and {rendered[-1]}"


def paragraph(text: str, class_name: str | None = None) -> str:
    return f"<p{attrs(class_=class_name)}>{e(text)}</p>"


def simple_list(items: list[str]) -> str:
    lines = "\n".join(f"<li>{e(item)}</li>" for item in items)
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
    links = "\n".join(f"            {link(item)}" for item in profile["links"])
    return f"""      <header class="profile">
        <img src="{e(profile['photo'])}" alt="{e(profile['photoAlt'])}" />
        <div>
          <h1>{e(profile['name'])}</h1>
          <p class="role">{e(profile['role'])}</p>
          <p class="tagline">{e(profile['tagline'])}</p>
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
    paragraphs = "\n".join(f"          {paragraph(text)}" for text in summary["paragraphs"])
    return section(summary["id"], summary["title"], f"{paragraphs}\n{chips(summary['chips'])}")


def render_timeline_section(item: dict[str, Any]) -> str:
    rows = []
    for entry in item["entries"]:
        parts = [f"                <h3>{e(entry['title'])}</h3>"]
        if entry.get("subtitle"):
            parts.append(f'                <p class="muted">{e(entry["subtitle"])}</p>')
        for index, line in enumerate(entry.get("lines", [])):
            class_name = "muted" if index > 0 or len(entry.get("lines", [])) == 1 else None
            parts.append(f"                {paragraph(line, class_name)}")
        if entry.get("bullets"):
            parts.append(indent(simple_list(entry["bullets"]), 16))
        body = "\n".join(parts)
        rows.append(
            f"""            <article class="timeline-row">
              <div class="date">{e(entry['date'])}</div>
              <div>
{body}
              </div>
            </article>"""
        )
    timeline = f'          <div class="timeline">\n' + "\n".join(rows) + "\n          </div>"
    return section(item["id"], item["title"], timeline)


def render_publications(data: dict[str, Any]) -> str:
    item = data["publications"]
    rows = []
    for entry in item["entries"]:
        rows.append(
            f"""            <article class="publication">
              <div class="pub-year">{e(entry['year'])}</div>
              <div>
                <h3>{e(entry['title'])}</h3>
                <p class="authors">{author_list(entry['authors'], item['highlightAuthor'])}</p>
                <p class="venue">{e(entry['venue'])}</p>
              </div>
            </article>"""
        )
    body = f'          <div class="publication-list">\n' + "\n".join(rows) + "\n          </div>"
    return section(item["id"], item["title"], body)


def render_skills(data: dict[str, Any]) -> str:
    item = data["skills"]
    rows = [
        f"            <p><strong>{e(group['label'])}:</strong> {e(', '.join(group['items']))}</p>"
        for group in item["groups"]
    ]
    body = f'          <div class="skill-list">\n' + "\n".join(rows) + "\n          </div>"
    return section(item["id"], item["title"], body)


def render_awards(data: dict[str, Any]) -> str:
    item = data["awards"]
    cards = []
    for category in item["categories"]:
        awards = "\n".join(
            f'                <li>{e(award["text"])} <span class="date-inline">{e(award["date"])}</span></li>'
            for award in category["items"]
        )
        cards.append(
            f"""            <article class="mini-card">
              <h3>{e(category['title'])}</h3>
              <ul class="simple-list">
{awards}
              </ul>
            </article>"""
        )
    body = f'          <div class="card-grid two">\n' + "\n".join(cards) + "\n          </div>"
    return section(item["id"], item["title"], body)


def render_linked_list(item: dict[str, Any]) -> str:
    rows = []
    for entry in item["entries"]:
        if isinstance(entry, str):
            rows.append(f"            <li>{e(entry)}</li>")
            continue
        text = e(entry["text"])
        if entry.get("href") and entry.get("linkText"):
            linked = f'<a href="{e(entry["href"])}">{e(entry["linkText"])}</a>'
            text = text.replace(e(entry["linkText"]), linked, 1)
        rows.append(f"            <li>{text}</li>")
    body = f'          <ul class="simple-list">\n' + "\n".join(rows) + "\n          </ul>"
    return section(item["id"], item["title"], body)


def render_html(data: dict[str, Any]) -> str:
    meta = data["meta"]
    sections = "\n\n".join(
        [
            render_summary(data),
            render_timeline_section(data["education"]),
            render_publications(data),
            render_timeline_section(data["workExperience"]),
            render_timeline_section(data["industrialProject"]),
            render_timeline_section(data["researchExperience"]),
            render_skills(data),
            render_awards(data),
            render_timeline_section(data["teaching"]),
            render_linked_list(data["invitedTalk"]),
            render_linked_list(data["service"]),
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
