from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for node in old_nodes:
        # If an "old node" is not a TextType.TEXT type, just add it to the new list as-is, we only attempt to split "text" type objects (not bold, italic, etc).
        if not node.text_type == TextType.TEXT:
            nodes.append(node)
        else:
            # If a matching closing delimiter is not found, just raise an exception with a helpful error message, that's invalid Markdown syntax.
            if not node.text.count(delimiter) % 2 == 0:
                raise Exception("Invalid Markdown syntax")
            
            node_tokens = node.text.split(delimiter)
            i = 0
            for token in node_tokens:
                if token:
                    #print(token)
                    if i % 2 == 0:
                        nodes.append(TextNode(token,TextType.TEXT))
                    else:
                        nodes.append(TextNode(token,text_type))
                    i += 1
    return nodes