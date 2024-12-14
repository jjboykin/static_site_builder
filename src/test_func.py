import unittest

from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *
from lib_func import *

class TestFunctionLibrary(unittest.TestCase):
    def test_text_to_html_node(self):
        text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        new_node = text_node_to_html_node(text_node)
        expected_output = "<b>This is a text node</b>"
        self.assertTrue(new_node.to_html() == expected_output)

    def test_split_text_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result1 = TextNode("This is text with a ", TextType.TEXT)
        expected_result2 = TextNode("code block", TextType.CODE)
        expected_result3 = TextNode(" word", TextType.TEXT)
        expected_result = [expected_result1, expected_result2, expected_result3]
        self.assertTrue(new_nodes == expected_result)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertTrue(result == expected_result)
        
              
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)" 
        result = extract_markdown_links(text)
        expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertTrue(result == expected_result)