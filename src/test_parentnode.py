import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        anchor_props = {"href": "https://www.google.com", "target": "_blank" }
        leaf_node1 = LeafNode("a", "this is an anchor", props=anchor_props)
        leaf_node2 = LeafNode("p", "this is a paragraph")
        child_list = [leaf_node1, leaf_node2]
        body_props = {"color" : "red"}
        parent_node1 = ParentNode("body", child_list, props=body_props)
        parent_node2 = ParentNode("body", child_list, props=body_props)
        self.assertEqual(parent_node1, parent_node2)

    def test_to_html_output(self):
        anchor_props = {"href": "https://www.google.com", "target": "_blank" }
        leaf_node1 = LeafNode("a", "this is an anchor", props=anchor_props)
        leaf_node2 = LeafNode("p", "this is a paragraph")
        child_list = [leaf_node1, leaf_node2]
        body_props = {"color" : "red"}
        parent_node = ParentNode("body", child_list, body_props)
        html = parent_node.to_html()
        print(html)
        self.assertTrue(html=="<body color='red'><a href='https://www.google.com' target='_blank'>this is an anchor</a><p>this is a paragraph</p></body>")

if __name__ == "__main__":
    unittest.main()