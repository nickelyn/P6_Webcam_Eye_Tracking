import unittest
from src.window_title import WindowTitle


class TestWindowTitle(unittest.TestCase):
    def test_get_window_titles(self):
        titles = WindowTitle.get_titles_list()
        print(titles)
        self.assertIsNotNone(titles)

    def test_get_window(self):
        titles = WindowTitle.get_titles_list()
        window = WindowTitle(str(titles[0]))

        captured = window.get_window()
        # Should return 0, due to finding a hidden menu
        self.assertEqual(captured, None)


if __name__ == "__main__":
    unittest.main()
