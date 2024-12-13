import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        test_props = {"href": "https://www.google.com", "target": "_blank" }
        node = LeafNode("a", "this is an anchor", props=test_props)
        node2 = LeafNode("a", "this is an anchor", props=test_props)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        test_props = {"href": "https://www.google.com", "target": "_blank" }
        node = LeafNode("a", "this is an anchor", props=test_props)
        node2 = LeafNode("p", "this is a paragraph")
        self.assertNotEqual(node, node2)

    def test_props_to_html_leading_space(self):
        test_props = {"href": "https://www.google.com", "target": "_blank" }
        node = LeafNode("a", "this is an anchor", props=test_props)
        html = node.props_to_html()
        self.assertTrue(html[0]==" ")

    def test_to_html_output(self):
        test_props = {"href": "https://www.google.com", "target": "_blank" }
        node = LeafNode("a", "this is an anchor", props=test_props)
        html = node.to_html()
        print(html)
        self.assertTrue(html=="<a href='https://www.google.com' target='_blank'>this is an anchor</a>")

if __name__ == "__main__":
    unittest.main()