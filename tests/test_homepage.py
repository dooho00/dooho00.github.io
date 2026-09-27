import json
import unittest
from html import escape
from pathlib import Path
from xml.etree import ElementTree

from build import render_html, render_models, render_timeline_section
from PIL import Image


class HomepageTests(unittest.TestCase):
    def test_model_reading_order_and_links(self):
        root = Path(__file__).resolve().parents[1]
        data = json.loads((root / "data/site.json").read_text())
        section = ElementTree.fromstring(render_models(data))
        rows = section.findall(".//article")
        self.assertEqual(len(rows), len(data["models"]["entries"]))
        for row, entry in zip(rows, data["models"]["entries"]):
            self.assertEqual([child.get("class") for child in row],
                             ["model-heading", None, "model-links"])
            self.assertEqual(row.find("p").text, entry["description"])
            self.assertEqual([link.get("href") for link in row.findall("./div[@class='model-links']/a")],
                             [link["href"] for link in entry["links"]])

    def test_education_reading_order(self):
        root = Path(__file__).resolve().parents[1]
        data = json.loads((root / "data/site.json").read_text())
        section = ElementTree.fromstring(render_timeline_section(data["education"], data["inlineLinks"]))
        rows = section.findall(".//article")
        self.assertEqual(len(rows), len(data["education"]["entries"]))
        for row, entry in zip(rows, data["education"]["entries"]):
            self.assertEqual([child.get("class") for child in row],
                             ["timeline-heading", "date", "timeline-details"])
            self.assertEqual("".join(row[0].find("h3").itertext()), entry["title"])
            self.assertIn(entry["date"], "".join(row[1].itertext()))
            for line in entry.get("lines", []):
                self.assertIn(line, "".join(row[2].itertext()))

    def test_publication_layout_preserves_content_and_links(self):
        root = Path(__file__).resolve().parents[1]
        data = json.loads((root / "data/site.json").read_text())
        html = render_html(data)
        entries = data["publications"]["entries"]
        self.assertEqual(html.count('class="publication-heading"'), len(entries))
        self.assertEqual(html.count('class="publication-meta"'), len(entries))
        for entry in entries:
            self.assertIn(escape(entry["title"], quote=True), html)
            for link in entry["links"]:
                self.assertIn(f'href="{escape(link["href"], quote=True)}"', html)
        self.assertIn('aria-label="Profile links"', html)
        self.assertIn('aria-label="Section navigation"', html)

    def test_paper_previews_have_matching_dialogs_and_real_figures(self):
        root = Path(__file__).resolve().parents[1]
        data = json.loads((root / "data/site.json").read_text())
        html = render_html(data)
        for index, entry in enumerate(data["publications"]["entries"]):
            preview = entry["preview"]
            self.assertIn(f'data-dialog="paper-{index}"', html)
            self.assertIn(f'id="paper-{index}"', html)
            self.assertIn(f'aria-labelledby="paper-{index}-title"', html)
            self.assertIn(escape(preview["summary"], quote=True), html)
            self.assertIn(f'href="{escape(preview["source"], quote=True)}"', html)
            self.assertTrue(preview["alt"])
            with Image.open(root / preview["image"]) as image:
                self.assertEqual(image.size, (preview["width"], preview["height"]))


if __name__ == "__main__":
    unittest.main()
