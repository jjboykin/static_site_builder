import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        test_props = {"href": "https://www.google.com", "target": "_blank" }
        node = HTMLNode("a", "this is an anchor", props=test_props)
        node2 = HTMLNode("a", "this is an anchor", props=test_props)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        test_props = {"href": "https://www.google.com", "target": "_blank" }
        node = HTMLNode("a", "this is an anchor", props=test_props)
        node2 = HTMLNode("p", "this is a paragraph")
        self.assertNotEqual(node, node2)

    def test_props_to_html_leading_space(self):
        test_props = {"href": "https://www.google.com", "target": "_blank" }
        node = HTMLNode("a", "this is an anchor", props=test_props)
        html = node.props_to_html()
        self.assertTrue(html[0]==" ")

if __name__ == "__main__":
    unittest.main()