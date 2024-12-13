from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *
from lib_func import *

def main():
    text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    anchor_props = {"href" : "https://www.google.com", "target" : "_blank" }
    html_node = LeafNode("a", "this is an anchor", props=anchor_props)
    leaf_node1 = LeafNode("a", "this is an anchor", props=anchor_props)
    leaf_node2 = LeafNode("p", "this is a paragraph")
    child_list = [leaf_node1, leaf_node2]
    body_props = {"color" : "red"}
    parent_node = ParentNode("body", child_list, body_props)
    #print(parent_node.to_html())
    new_node = text_node_to_html_node(text_node)
    #print(new_node)
    #print(new_node.to_html())
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    #print(new_nodes)

main()