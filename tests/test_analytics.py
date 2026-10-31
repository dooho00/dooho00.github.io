import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

from build import render_html


class AnalyticsTests(unittest.TestCase):
    def test_homepage_includes_one_cloudflare_beacon(self):
        class ScriptParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.beacons = []

            def handle_starttag(self, tag, attrs):
                attributes = dict(attrs)
                if tag == "script" and "data-cf-beacon" in attributes:
                    self.beacons.append(attributes)

        root = Path(__file__).resolve().parents[1]
        data = json.loads((root / "data/site.json").read_text())
        parser = ScriptParser()
        parser.feed(render_html(data))
        self.assertEqual(len(parser.beacons), 1)
        beacon = parser.beacons[0]
        self.assertEqual(beacon["type"], "module")
        self.assertEqual(beacon["src"], "https://static.cloudflareinsights.com/beacon.min.js")
        self.assertEqual(json.loads(beacon["data-cf-beacon"]),
                         {"token": "5cff3b02801c4313a30e323efab74b1c"})


if __name__ == "__main__":
    unittest.main()
