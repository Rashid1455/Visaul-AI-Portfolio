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
    def test_home_navigation_and_gallery_filters(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=15).run()
        app.button(key="home-inquiry").click().run()
        self.assertEqual(app.sidebar.radio[0].value, "Contact")
        self.assertFalse(app.exception)
        app.sidebar.radio[0].set_value("Portfolio").run()
        image_count, video_count = len(app.get("image")), len(app.get("video"))
        for choice, images, videos in (("Images", image_count, 0), ("Videos", 0, video_count), ("All work", image_count, video_count)):
            app.get("button_group")[0].set_value(choice).run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.get("image")), images)
            self.assertEqual(len(app.get("video")), videos)

    def test_every_page_renders(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=15).run()
        self.assertFalse(app.exception)
        for page in ("Portfolio", "Services", "Process", "About", "Contact"):
            app.sidebar.radio[0].set_value(page).run()
            self.assertFalse(app.exception, page)

    def test_inquiry_validation_and_draft(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=15).run()
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
        app.sidebar.radio[0].set_value("Home").run()
        app.sidebar.radio[0].set_value("Contact").run()
        self.assertEqual(app.text_input[0].value, "Client")
        self.assertEqual(app.text_input[1].value, "client@example.com")
        self.assertEqual(app.text_area[0].value, "Campaign visuals")
        app.text_input[1].set_value("invalid")
        app.button[0].click().run()
        self.assertNotIn("inquiry_draft", app.session_state)


if __name__ == "__main__":
    unittest.main()
