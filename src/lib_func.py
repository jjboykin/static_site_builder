import re

from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *

class HTMLBlock:
    block_type_paragraph = "paragraph"
    block_type_heading = "heading"
    block_type_code = "code"
    block_type_quote = "quote"
    block_type_olist = "ordered_list"
    block_type_ulist = "unordered_list"

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
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

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

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return HTMLBlock.block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return HTMLBlock.block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return HTMLBlock.block_type_paragraph
        return HTMLBlock.block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return HTMLBlock.block_type_paragraph
        return HTMLBlock.block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return HTMLBlock.block_type_paragraph
        return HTMLBlock.block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return HTMLBlock.block_type_paragraph
            i += 1
        return HTMLBlock.block_type_olist
    return HTMLBlock.block_type_paragraph

def markdown_to_html_node(markdown):
    children = []

    # Split the markdown into blocks (you already have a function for this)
    blocks = markdown_to_blocks(markdown)

    # Loop over each block:
    for block in blocks:
        # Determine the type of block (you already have a function for this)
        block_type = block_to_block_type(block)

        # Based on the type of block, create a new HTMLNode with the proper data
        match block_type:
            case HTMLBlock.block_type_paragraph:
                child_nodes = text_to_children(block)
                has_children = len(child_nodes) > 1
                if has_children:
                    node = ParentNode("p", children=child_nodes)
                else:
                    node = LeafNode("p", value=block)
            case HTMLBlock.block_type_heading:
                if block.startswith("# "):
                    heading_tag = "h1"
                elif block.startswith("## "):
                    heading_tag = "h2"
                elif block.startswith("### "):
                    heading_tag = "h3"
                elif block.startswith("#### "):
                    heading_tag = "h4"
                elif block.startswith("##### "):
                    heading_tag = "h5"
                elif block.startswith("###### "):
                    heading_tag = "h6"
                block = strip_markdown(block, HTMLBlock.block_type_heading)
                node = LeafNode(heading_tag, value=block)
            case HTMLBlock.block_type_code:
                block = strip_markdown(block, HTMLBlock.block_type_code)
                node = LeafNode("code", value=block)
                node = ParentNode("pre", children=node)
            case HTMLBlock.block_type_quote:
                block = strip_markdown(block, HTMLBlock.block_type_quote)
                node = LeafNode("blockquote", value=block)
            case HTMLBlock.block_type_olist:
                block = strip_markdown(block, HTMLBlock.block_type_olist)
                child_nodes = text_to_list_items(block)
                node = ParentNode("ol", children=child_nodes)
            case HTMLBlock.block_type_ulist:
                block = strip_markdown(block, HTMLBlock.block_type_ulist)
                child_nodes = text_to_list_items(block)
                node = ParentNode("ul", children=child_nodes)
            case _:
                raise Exception("Invalid block type")

        children.append(node)

    # Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
    return ParentNode("div", children)

def text_to_children(text):
    html_nodes = []

    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes

def text_to_list_items(block):
    html_nodes = []
    lines = block.split("\n")

    for line in lines:
        list_item = LeafNode("li", value=line)
        html_nodes.append(list_item)

    return html_nodes

def strip_markdown(block, block_type):
    match block_type:
        case HTMLBlock.block_type_heading:
            if block.startswith("# "):
                return block.replace("# ", "")
            if block.startswith("## "):
                return block.replace("## ", "")
            if block.startswith("### "):
                return block.replace("### ", "")
            if block.startswith("#### "):
                return block.replace("#### ", "")
            if block.startswith("##### "):
                return block.replace("##### ", "")
            if block.startswith("###### "):
                return block.replace("###### ", "")
        case HTMLBlock.block_type_code:
            return block.replace("```", "")
        case HTMLBlock.block_type_quote:
            return block.replace(">", "")
        case HTMLBlock.block_type_ulist:
            block = block.replace("* ", "")
            return block.replace("- ", "")
        case HTMLBlock.block_type_olist:
            lines = block.split("\n")
            i = 1
            for line in lines:
                line.replace(f"{i}. ", "")
                i += 1
            block = "\n".join(lines)
            return block