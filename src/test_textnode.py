import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://local.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://local.dev")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://local.dev")
        node2 = TextNode("This is a different text node", TextType.BOLD, "http://local.dev")
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://local.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "http://local.dev")
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://local.dev")
        node2 = TextNode("This is a different text node", TextType.BOLD, "http://local.com")
        self.assertNotEqual(node, node2)

    def test_other(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)

if __name__ == "__main__":
    unittest.main()
