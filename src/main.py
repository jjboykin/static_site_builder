from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *
from lib_func import *

def main():
    #text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    #print(text_to_textnodes(text))

    full_markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
    print("Markdown:")
    print(full_markdown)
    print("HTML:")
    print(markdown_to_html_node(full_markdown).to_html())
    

main()