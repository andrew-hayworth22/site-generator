import unittest
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)
from htmlnode import LeafNode

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

    def test_text_to_html_node(self):
        text_node = TextNode("hello world", "text")
        expected = LeafNode("hello world") 
        
        self.assertEqual(text_node.to_html_node(), expected)

    def test_bold_to_html_node(self):
        text_node = TextNode("hello world", "bold")
        expected = LeafNode("hello world", "b") 
        
        self.assertEqual(text_node.to_html_node(), expected)

    def test_italic_to_html_node(self):
        text_node = TextNode("hello world", "italic")
        expected = LeafNode("hello world", "i") 
        
        self.assertEqual(text_node.to_html_node(), expected)

    def test_code_to_html_node(self):
        text_node = TextNode("hello world", "code")
        expected = LeafNode("hello world", "code") 
        
        self.assertEqual(text_node.to_html_node(), expected)

    def test_link_to_html_node(self):
        text_node = TextNode("hello world", "link", "https://example.com")
        expected = LeafNode("hello world", "a", {"href": "https://example.com"}) 
        
        self.assertEqual(text_node.to_html_node(), expected)

    def test_image_to_html_node(self):
        text_node = TextNode("hello world", "image", "https://example.com")
        expected = LeafNode("", "img", {"src": "https://example.com", "alt": "hello world"}) 
        
        self.assertEqual(text_node.to_html_node(), expected)

    def test_text_to_html_node_error(self):
        text_node = TextNode("hello world", "nope")
        
        self.assertRaises(Exception, text_node.to_html_node) 

if __name__ == "__main__":
    unittest.main()