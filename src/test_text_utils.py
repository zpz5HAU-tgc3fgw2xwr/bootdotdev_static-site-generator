import unittest
from textnode import TextNode, TextType
from text_utils import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_text_to_textnodes_no_formatting(self):
        text = "This is plain text with no formatting."
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode(text, TextType.NORMAL)])

    def test_text_to_textnodes_only_bold(self):
        text = "This is **bold** text."
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.NORMAL),
        ])

    def test_text_to_textnodes_only_italic(self):
        text = "This is *italic* text."
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.NORMAL),
        ])

    def test_text_to_textnodes_only_code(self):
        text = "This is `code` text."
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.NORMAL),
        ])

    def test_text_to_textnodes_only_image(self):
        text = "This is an image ![alt text](https://example.com/image.png)."
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is an image ", TextType.NORMAL),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(".", TextType.NORMAL),
        ])

    def test_text_to_textnodes_only_link(self):
        text = "This is a link [to boot dev](https://www.boot.dev)."
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(".", TextType.NORMAL),
        ])

if __name__ == "__main__":
    unittest.main()
