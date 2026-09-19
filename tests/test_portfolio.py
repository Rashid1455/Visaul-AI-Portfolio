import tempfile
import unittest
from pathlib import Path

from portfolio_storage import save_upload
from streamlit.testing.v1 import AppTest


class StorageTests(unittest.TestCase):
    def test_collision_preserves_original(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            first = save_upload(root, "photo.png", b"original")
            second = save_upload(root, "photo.png", b"replacement")
            self.assertNotEqual(first, second)
            self.assertEqual(first.read_bytes(), b"original")
            self.assertEqual(second.read_bytes(), b"replacement")

    def test_paths_stay_inside_library(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ("../../photo.png", r"..\..\photo.png", "CON.png"):
                saved = save_upload(root, name, b"image")
                self.assertEqual(saved.parent, root)
                self.assertTrue(saved.exists())

    def test_rejects_unsupported_and_empty_uploads(self):
        with tempfile.TemporaryDirectory() as folder:
            for name, data in (("script.py", b"code"), ("photo.png", b"")):
                with self.assertRaises(ValueError):
                    save_upload(Path(folder), name, data)
            self.assertEqual(list(Path(folder).iterdir()), [])


class AppTests(unittest.TestCase):
    def test_every_page_renders(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
        self.assertFalse(app.exception)
        for page in ("Portfolio", "Services", "Process", "About", "Contact"):
            app.sidebar.radio[0].set_value(page).run()
            self.assertFalse(app.exception, page)

    def test_inquiry_validation_and_draft(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
        app.sidebar.radio[0].set_value("Contact").run()
        app.text_input[0].set_value("   ")
        app.button[0].click().run()
        self.assertTrue(app.warning)
        app.text_input[0].set_value("Client")
        app.text_input[1].set_value("invalid")
        app.text_area[0].set_value("Campaign visuals")
        app.button[0].click().run()
        self.assertIn("valid email", app.warning[0].value)
        app.text_input[1].set_value("client@example.com")
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertIn("Campaign visuals", app.session_state["inquiry_draft"])
        app.run()
        self.assertIn("Campaign visuals", app.session_state["inquiry_draft"])
        app.text_input[1].set_value("invalid")
        app.button[0].click().run()
        self.assertNotIn("inquiry_draft", app.session_state)


if __name__ == "__main__":
    unittest.main()
