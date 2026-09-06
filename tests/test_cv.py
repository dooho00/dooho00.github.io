import copy
import json
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

from build_cv import build_cv


ROOT = Path(__file__).resolve().parents[1]


class CVTests(unittest.TestCase):
    def test_content_links_and_regeneration(self):
        data = json.loads((ROOT / "data/site.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "cv.pdf"
            build_cv(data, output)
            reader = PdfReader(output)
            self.assertLessEqual(len(reader.pages), 2)
            self.assertEqual(len(reader.pages[0].images), 1)
            content = " ".join(" ".join(page.extract_text().split()) for page in reader.pages)
            links = {
                str(annotation.get_object().get("/A", {}).get("/URI", ""))
                for page in reader.pages for annotation in page.get("/Annots", [])
            }
            self.assertIn(data["profile"]["role"], content)
            for publication in data["publications"]["entries"]:
                self.assertIn(publication["title"], content)
                for link in publication.get("links", []):
                    self.assertIn(link["href"], links)
            for section in ("workExperience", "industrialProject", "teaching"):
                for entry in data[section]["entries"]:
                    self.assertIn(entry["description"], content)
            for award in data["awards"]["items"]:
                self.assertIn(award["text"], content)
            for page in reader.pages:
                self.assertAlmostEqual(float(page.mediabox.width), 595.28, places=1)
                self.assertAlmostEqual(float(page.mediabox.height), 841.89, places=1)
            self.assertNotIn("\ufffd", content)
            original = output.read_bytes()
            build_cv(data, output)
            self.assertEqual(original, output.read_bytes())

            updated = copy.deepcopy(data)
            updated["publications"]["entries"][0]["title"] = "Updated research & reproducible <results>"
            build_cv(updated, output)
            updated_content = " ".join(page.extract_text() for page in PdfReader(output).pages)
            self.assertIn("Updated research & reproducible <results>", updated_content)
            self.assertNotIn(data["publications"]["entries"][0]["title"], updated_content)


if __name__ == "__main__":
    unittest.main()
