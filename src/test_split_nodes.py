import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ])

    def test_split_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
        ])

    def test_split_italic_delimiter(self):
        node = TextNode("This is *italic* text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.NORMAL),
        ])

    def test_no_delimiter(self):
        node = TextNode("This is plain text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

class TestSplitNodesImage(unittest.TestCase):
    def test_split_image(self):
        node = TextNode("This is text with an image ![alt text](https://example.com/image.png)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with an image ", TextType.NORMAL),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")
        ])

    def test_split_multiple_images(self):
        node = TextNode("Image one ![one](https://example.com/one.png) and image two ![two](https://example.com/two.png)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("Image one ", TextType.NORMAL),
            TextNode("one", TextType.IMAGE, "https://example.com/one.png"),
            TextNode(" and image two ", TextType.NORMAL),
            TextNode("two", TextType.IMAGE, "https://example.com/two.png")
        ])

    def test_no_images(self):
        node = TextNode("This is text with no images.", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

class TestSplitNodesLink(unittest.TestCase):
    def test_split_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
        ])

    def test_split_multiple_links(self):
        node = TextNode("Link one [one](https://example.com/one) and link two [two](https://example.com/two)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("Link one ", TextType.NORMAL),
            TextNode("one", TextType.LINK, "https://example.com/one"),
            TextNode(" and link two ", TextType.NORMAL),
            TextNode("two", TextType.LINK, "https://example.com/two")
        ])

    def test_no_links(self):
        node = TextNode("This is text with no links.", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

if __name__ == "__main__":
    unittest.main()