from ast import match_case
from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text:str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if isinstance(other,TextNode):
            return (self.text == other.text and self.text_type == other.text_type and self.url == other.url)
        else:
            return False

    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if not isinstance(text_node.text_type, TextType):
        raise TypeError("input txt type is not supported")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag = None,value =text_node.text)
        case TextType.BOLD:
            return LeafNode(tag ="b", value =text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag ="i", value =text_node.text)
        case TextType.CODE:
            return LeafNode(tag ="code", value =text_node.text)
        case TextType.LINK:
            return LeafNode(tag ="a", value =text_node.text, props={"href": f'{text_node.url}'})
        case TextType.IMAGE:
            return LeafNode(tag ="img", value = "", props={"src": f'{text_node.url}', "alt": f'{text_node.text}'})
