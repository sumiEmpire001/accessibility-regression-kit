import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


def luminance(hex_color):
    values = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    values = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
    return .2126 * values[0] + .7152 * values[1] + .0722 * values[2]


class MarkupTests(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / "index.html").read_text()
        self.css = (ROOT / "styles.css").read_text()
        self.doc = Document(self.html)
    def test_document_has_language_viewport_and_title(self):
        self.assertIn(("html", {"lang": "en"}), self.doc.elements)
        self.assertIn('name="viewport"', self.html)
        self.assertRegex(self.html, r"<title>[^<]+</title>")
    def test_ids_are_unique(self):
        ids = [a["id"] for _, a in self.doc.elements if "id" in a]
        self.assertEqual(len(ids), len(set(ids)))
    def test_anchor_targets_exist(self):
        ids = {a["id"] for _, a in self.doc.elements if "id" in a}
        for tag, a in self.doc.elements:
            if tag == "a" and a.get("href", "").startswith("#"):
                self.assertIn(a["href"][1:], ids)
    def test_form_controls_have_explicit_or_wrapped_labels(self):
        labels = {a["for"] for t, a in self.doc.elements if t == "label" and "for" in a}
        for tag, a in self.doc.elements:
            if tag in ("input", "select") and a.get("type") != "radio":
                self.assertIn(a["id"], labels)
        for radio in ("theme-system", "theme-light", "theme-dark"):
            self.assertRegex(self.html, '<label><input id="' + radio + '"')
    def test_help_references_exist(self):
        ids = {a["id"] for _, a in self.doc.elements if "id" in a}
        for _, a in self.doc.elements:
            for reference in a.get("aria-describedby", "").split():
                self.assertIn(reference, ids)
    def test_runtime_is_html_and_css_only(self):
        self.assertNotRegex(self.html, r"<script\b|\sonclick=")
        self.assertNotIn("@import", self.css)
        self.assertNotRegex(self.html, r'(?:src|href)="https?://')
    def test_native_required_validation_is_present(self):
        inputs = {a["id"]: a for tag, a in self.doc.elements if tag == "input"}
        self.assertIn("required", inputs["sample-name"])
        self.assertIn("required", inputs["sample-email"])
        self.assertEqual(inputs["sample-email"]["type"], "email")
    def test_skip_link_and_semantic_landmarks(self):
        tags = [tag for tag, _ in self.doc.elements]
        self.assertEqual(tags.count("main"), 1)
        self.assertEqual(tags.count("h1"), 1)
        self.assertIn('class="skip" href="#main"', self.html)
        self.assertIn('id="main" tabindex="-1"', self.html)
    def test_disclosures_keep_native_semantics(self):
        self.assertEqual(self.html.count("<details>"), self.html.count("<summary>"))
        self.assertGreaterEqual(self.html.count("<details>"), 2)
    def test_motion_focus_and_responsive_rules_exist(self):
        for token in ("prefers-reduced-motion", ":focus-visible", "max-width:620px", "max-width:900px"):
            self.assertIn(token, self.css)
    def test_light_and_dark_text_tokens_meet_contrast_threshold(self):
        for foreground, background in (("#182a23", "#f4f3ee"), ("#4e6258", "#ffffff"), ("#f1f4ec", "#10201a"), ("#b8c8bd", "#182e24"), ("#ffffff", "#14583f"), ("#10201a", "#a9d6b9")):
            values = sorted((luminance(foreground), luminance(background)))
            self.assertGreaterEqual((values[1] + .05) / (values[0] + .05), 4.5)
    def test_no_backend_or_saved_progress_is_claimed(self):
        self.assertIn("No application backend", self.html)
        self.assertIn("not saved", self.html)


if __name__ == "__main__":
    unittest.main()
