from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def block_to_block_type(block):
    if block.startswith("#"):
        if block.startswith("# "):
            return "heading1"
        elif block.startswith("## "):
            return "heading2"
        elif block.startswith("### "):
            return "heading3"
        elif block.startswith("#### "):
            return "heading4"
        elif block.startswith("##### "):
            return "heading5"
        elif block.startswith("###### "):
            return "heading6"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif all(line.startswith(">") for line in block.split("\n")):
        return "quote"
    elif all(line.startswith(("* ", "- ")) for line in block.split("\n")):
        return "unordered_list"
    elif all(line.split(". ")[0].isdigit() and int(line.split(". ")[0]) == idx + 1 for idx, line in enumerate(block.split("\n"))):
        return "ordered_list"
    else:
        return "paragraph"