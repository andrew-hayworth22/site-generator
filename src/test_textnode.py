import unittest
from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq_true_no_url(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    def test_eq_true_with_url(self):
        node = TextNode("This is a text node", "bold", "https://www.example.com")
        node2 = TextNode("This is a text node", "bold", "https://www.example.com")
        self.assertEqual(node, node2)
    def test_eq_false_no_url(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)
    def test_eq_false_without_url(self):
        node = TextNode("This is a text node", "bold", "https://www.example.com")
        node2 = TextNode("This is a text", "bold", "https://www.example.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()