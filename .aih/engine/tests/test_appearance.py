import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from appearance import validate_appearance
from contracts import Error

CUSTOM = {"theme": "custom", "size": 16, "custom": {"name": "Clear copy", "mode": "light", "font": "system", "heading": "system", "colors": {"bg": "#f4f6f8", "surface": "#ffffff", "raised": "#edf1f5", "text": "#172337", "muted": "#536279", "border": "#cbd4df", "accent": "#2457be", "on-accent": "#ffffff", "positive": "#166544", "warning": "#805212", "danger": "#b12c3b", "focus": "#855bce"}}}

class AppearanceTests(unittest.TestCase):
    def test_supported_presets_and_custom_contrast(self):
        for theme in ("clear", "midnight", "warm", "contrast", "system"):
            self.assertEqual(validate_appearance({"theme": theme, "size": 22})["theme"], theme)
        self.assertEqual(validate_appearance(CUSTOM), CUSTOM)

    def test_arbitrary_css_and_remote_font_rejected(self):
        for section, key, value in (("custom", "font", "url(https://example.invalid/font)"), ("colors", "bg", "expression(alert(1))"), ("custom", "css", "body { display:none }")):
            item = copy.deepcopy(CUSTOM)
            target = item["custom"]["colors"] if section == "colors" else item["custom"]
            target[key] = value
            with self.subTest(key=key), self.assertRaises(Error):
                validate_appearance(item)

    def test_contrast_failure_names_pair_and_preserves_draft(self):
        item = copy.deepcopy(CUSTOM)
        item["custom"]["colors"]["text"] = "#ffffff"
        with self.assertRaises(Error) as exc:
            validate_appearance(item)
        self.assertEqual(exc.exception.code, "appearance-contrast")
        self.assertEqual(exc.exception.details["foreground"], "text")
        self.assertEqual(item["custom"]["colors"]["text"], "#ffffff")

    def test_unsupported_size_and_missing_colors(self):
        for size in (13, 23, True, "16", 16.5):
            with self.subTest(size=size), self.assertRaises(Error):
                validate_appearance({"theme": "clear", "size": size})
        item = copy.deepcopy(CUSTOM)
        del item["custom"]["colors"]["focus"]
        with self.assertRaises(Error):
            validate_appearance(item)

if __name__ == '__main__':
    unittest.main()
