import unittest
from textnode import TextNode, TextType, block_to_block_type

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.example.com")
        self.assertNotEqual(node, node2)

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading 1"), "heading1")
        self.assertEqual(block_to_block_type("## Heading 2"), "heading2")
        self.assertEqual(block_to_block_type("### Heading 3"), "heading3")
        self.assertEqual(block_to_block_type("#### Heading 4"), "heading4")
        self.assertEqual(block_to_block_type("##### Heading 5"), "heading5")
        self.assertEqual(block_to_block_type("###### Heading 6"), "heading6")
        self.assertEqual(block_to_block_type("```\ncode block\n```"), "code")
        self.assertEqual(block_to_block_type("> quote line 1\n> quote line 2"), "quote")
        self.assertEqual(block_to_block_type("* item 1\n* item 2"), "unordered_list")
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), "unordered_list")
        self.assertEqual(block_to_block_type("1. item 1\n2. item 2"), "ordered_list")
        self.assertEqual(block_to_block_type("This is a normal paragraph."), "paragraph")

if __name__ == "__main__":
    unittest.main()