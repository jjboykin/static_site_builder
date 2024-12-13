from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *

def main():
    text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    anchor_props = {"href" : "https://www.google.com", "target" : "_blank" }
    html_node = LeafNode("a", "this is an anchor", props=anchor_props)
    leaf_node1 = LeafNode("a", "this is an anchor", props=anchor_props)
    leaf_node2 = LeafNode("p", "this is a paragraph")
    child_list = [leaf_node1, leaf_node2]
    body_props = {"color" : "red"}
    parent_node = ParentNode("body", child_list, body_props)
    print(parent_node.to_html())
    new_node = text_node_to_html_node(text_node)
    print(new_node)
    print(new_node.to_html())

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.NORMAL:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINKS:
            return LeafNode(tag="a", value=text_node.text, props={"href" : text_node.url})
        case TextType.IMAGES:
            return LeafNode(tag="img", value=None, props={"src" : text_node.url, "alt" : text_node.text})
        case _:
            raise Exception("Invalid text type")

main()