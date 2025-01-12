from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_dict(self):
        return {
            "tag": self.tag,
            "children": [child.to_dict() if isinstance(child, HTMLNode) else child for child in self.children],
            "props": self.props
        }

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this!")

    def props_to_html(self):
        return ''.join(f' {key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        props_str = '{' + ', '.join(f'"{key}": "{value}"' for key, value in self.props.items()) + '}'
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={props_str})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        else:
            props_str = self.props_to_html()
            if self.tag == "img":
                return f"<{self.tag}{props_str} />"
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a tag")
        if children is None:
            raise ValueError("ParentNode must have children")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        children_html = ''.join(child.to_html() for child in self.children)
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("Unsupported TextType")