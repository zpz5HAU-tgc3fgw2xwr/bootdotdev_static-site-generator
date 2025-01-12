import unittest
from src.main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
        self.assertEqual(extract_title("# Hello\n## World"), "Hello")
        self.assertEqual(extract_title("# Hello\nContent\n## World"), "Hello")
        with self.assertRaises(Exception):
            extract_title("## No H1 title")

if __name__ == "__main__":
    unittest.main()
