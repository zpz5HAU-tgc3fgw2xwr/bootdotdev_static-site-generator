from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.NORMAL:
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    if part:
                        new_nodes.append(TextNode(part, TextType.NORMAL))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.NORMAL:
            parts = re.split(pattern, node.text)
            for i in range(0, len(parts), 3):
                if parts[i]:
                    new_nodes.append(TextNode(parts[i], TextType.NORMAL))
                if i + 1 < len(parts):
                    new_nodes.append(TextNode(parts[i + 1], TextType.IMAGE, parts[i + 2]))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.NORMAL:
            parts = re.split(pattern, node.text)
            for i in range(0, len(parts), 3):
                if parts[i]:
                    new_nodes.append(TextNode(parts[i], TextType.NORMAL))
                if i + 1 < len(parts):
                    new_nodes.append(TextNode(parts[i + 1], TextType.LINK, parts[i + 2]))
        else:
            new_nodes.append(node)
    return new_nodes
