import re

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

def extract_markdown_images(text):
    # images
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    # regular links
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def split_nodes_image(old_nodes):
    nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            nodes.append(old_node)
            continue
        node_text = old_node.text
        images = extract_markdown_images(node_text)
        if len(images) == 0:
            nodes.append(old_node)
            continue
        for image in images:
            sections = node_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                nodes.append(TextNode(sections[0], TextType.TEXT))
            nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            node_text = sections[1]
        if node_text != "":
            nodes.append(TextNode(node_text, TextType.TEXT))
    return nodes

def split_nodes_link(old_nodes):
    nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            nodes.append(old_node)
            continue
        node_text = old_node.text
        links = extract_markdown_links(node_text)
        if len(links) == 0:
            nodes.append(old_node)
            continue
        for link in links:
            sections = node_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                nodes.append(TextNode(sections[0], TextType.TEXT))
            nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            node_text = sections[1]

        if node_text != "":
            nodes.append(TextNode(node_text, TextType.TEXT))
    return nodes

def text_to_textnodes(text):
    original_text_node = TextNode(text, TextType.TEXT)
    nodes = [original_text_node]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes