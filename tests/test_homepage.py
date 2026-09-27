import json
import unittest
from html import escape
from pathlib import Path

from build import render_html
from PIL import Image


class HomepageTests(unittest.TestCase):
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
