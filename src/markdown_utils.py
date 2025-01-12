import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import block_to_block_type

def extract_markdown_images(text):
    pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

def text_to_children(text):
    # This function converts inline markdown text to a list of HTMLNode objects
    # For simplicity, let's assume it is already implemented
    nodes = []
    while text:
        if text.startswith("**"):
            end = text.find("**", 2)
            if end == -1:
                nodes.append(HTMLNode("text", children=[text]))
                break
            nodes.append(HTMLNode("strong", children=[HTMLNode("text", children=[text[2:end]])]))
            text = text[end + 2:]
        elif text.startswith("*") and not text.startswith("**"):
            end = text.find("*", 1)
            if end == -1:
                nodes.append(HTMLNode("text", children=[text]))
                break
            nodes.append(HTMLNode("em", children=[HTMLNode("text", children=[text[1:end]])]))
            text = text[end + 1:]
        else:
            end = min((text.find(c) for c in ["**", "*"] if text.find(c) != -1), default=len(text))
            nodes.append(HTMLNode("text", children=[text[:end]]))
            text = text[end:]
    return nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", children=[])

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type.startswith("heading"):
            level = int(block_type[-1])
            node = LeafNode(f"h{level}", block[level + 1:].strip())
        elif block_type == "code":
            node = ParentNode("pre", [LeafNode("code", block[3:-3].strip())])
        elif block_type == "quote":
            node = ParentNode("blockquote", [LeafNode(None, block.replace("> ", "").strip())])
        elif block_type == "unordered_list":
            node = ParentNode("ul", [ParentNode("li", [LeafNode(None, item[2:].strip())]) for item in block.split("\n")])
        elif block_type == "ordered_list":
            node = ParentNode("ol", [ParentNode("li", [LeafNode(None, item.split(". ", 1)[1].strip())]) for item in block.split("\n")])
        else:
            node = LeafNode("p", block.strip())

        parent_node.children.append(node)

    return parent_node
