import unittest
from textnode import (
    TextNode,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
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
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_eq_true_with_url(self):
        node = TextNode("This is a text node", text_type_bold, "https://www.example.com")
        node2 = TextNode("This is a text node", text_type_bold, "https://www.example.com")
        self.assertEqual(node, node2)

    def test_eq_false_no_url(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_italic)
        self.assertNotEqual(node, node2)

    def test_eq_false_without_url(self):
        node = TextNode("This is a text node", text_type_bold, "https://www.example.com")
        node2 = TextNode("This is a text", text_type_bold, "https://www.example.com")
        self.assertNotEqual(node, node2)

    def test_text_to_html_node(self):
        text_node = TextNode("hello world", text_type_text)
        expected = LeafNode("hello world") 
        
        self.assertEqual(text_node.to_html_node(), expected)

    def test_bold_to_html_node(self):
        text_node = TextNode("hello world", text_type_bold)
        expected = LeafNode("hello world", "b") 
        
        self.assertEqual(text_node.to_html_node(), expected)

    def test_italic_to_html_node(self):
        text_node = TextNode("hello world", text_type_italic)
        expected = LeafNode("hello world", "i") 
        
        self.assertEqual(text_node.to_html_node(), expected)

    def test_code_to_html_node(self):
        text_node = TextNode("hello world", text_type_code)
        expected = LeafNode("hello world", text_type_code) 
        
        self.assertEqual(text_node.to_html_node(), expected)

    def test_link_to_html_node(self):
        text_node = TextNode("hello world", text_type_link, "https://example.com")
        expected = LeafNode("hello world", "a", {"href": "https://example.com"}) 
        
        self.assertEqual(text_node.to_html_node(), expected)

    def test_image_to_html_node(self):
        text_node = TextNode("hello world", text_type_image, "https://example.com")
        expected = LeafNode("", "img", {"src": "https://example.com", "alt": "hello world"}) 
        
        self.assertEqual(text_node.to_html_node(), expected)

    def test_text_to_html_node_error(self):
        text_node = TextNode("hello world", "nope")
        
        self.assertRaises(Exception, text_node.to_html_node) 

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_italics_inside(self):
        nodes = [
            TextNode("This *text* is in italics", text_type_text)
        ]
        expected = [
            TextNode("This ", text_type_text),
            TextNode("text", text_type_italic),
            TextNode(" is in italics", text_type_text)
        ]

        self.assertListEqual(split_nodes_delimiter(nodes, "*", text_type_italic), expected)

    def test_italics_outside(self):
        nodes = [
            TextNode("*This text* is in *italics*", text_type_text)
        ]
        expected = [
            TextNode("This text", text_type_italic),
            TextNode(" is in ", text_type_text),
            TextNode("italics", text_type_italic)
        ]

        self.assertListEqual(split_nodes_delimiter(nodes, "*", text_type_italic), expected)

    def test_bold(self):
        nodes = [
            TextNode("This text is **bold**", text_type_text)
        ]
        expected = [
            TextNode("This text is ", text_type_text),
            TextNode("bold", text_type_bold),
        ]

        self.assertListEqual(split_nodes_delimiter(nodes, "**", text_type_bold), expected)

    def test_exception_end(self):
        nodes = [
            TextNode("This text is bold**", text_type_text)
        ]

        self.assertRaises(Exception, split_nodes_delimiter, nodes)

    def test_exception_start(self):
        nodes = [
            TextNode("**This text is bold", text_type_text)
        ]

        self.assertRaises(Exception, split_nodes_delimiter, nodes)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("This *text* is in italics", text_type_text),
            TextNode("This text is not in italics", text_type_text),
            TextNode("This *text* is in italics", text_type_text),
        ]
        expected = [
            TextNode("This ", text_type_text),
            TextNode("text", text_type_italic),
            TextNode(" is in italics", text_type_text),
            TextNode("This text is not in italics", text_type_text),
            TextNode("This ", text_type_text),
            TextNode("text", text_type_italic),
            TextNode(" is in italics", text_type_text),
        ]

        self.assertListEqual(split_nodes_delimiter(nodes, "*", text_type_italic), expected)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_single_image(self):
        nodes = [
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type_text)
        ]
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif")
        ]

        self.assertListEqual(split_nodes_image(nodes), expected)

    def test_split_multiple_images(self):
        nodes = [
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text)
        ]
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", text_type_text),
            TextNode("obi wan", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]

        self.assertListEqual(split_nodes_image(nodes), expected)

    def test_split_no_images(self):
        nodes = [
            TextNode("No images to see here", text_type_text)
        ]
        expected = [
            TextNode("No images to see here", text_type_text)
        ]

        self.assertListEqual(split_nodes_image(nodes), expected)

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("No images to see here", text_type_text),
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text)
        ]
        expected = [
            TextNode("No images to see here", text_type_text),
            TextNode("This is text with a ", text_type_text),
            TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", text_type_text),
            TextNode("obi wan", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]

        self.assertListEqual(split_nodes_image(nodes), expected)

class TestSplitLink(unittest.TestCase):
    def test_split_single_link(self):
        nodes = [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev)", text_type_text)
        ]
        expected = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev")
        ]

        self.assertListEqual(split_nodes_link(nodes), expected)

    def test_split_multiple_links(self):
        nodes = [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)", text_type_text)
        ]
        expected = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode("to youtube", text_type_link, "https://www.youtube.com"),
        ]

        self.assertListEqual(split_nodes_link(nodes), expected)

    def test_split_no_links(self):
        nodes = [
            TextNode("No links to show here!", text_type_text)
        ]
        expected = [
            TextNode("No links to show here!", text_type_text)
        ]

        self.assertListEqual(split_nodes_link(nodes), expected)

    def test_split_link_multiple_nodes(self):
        nodes = [
            TextNode("No links to show here!", text_type_text),
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)", text_type_text),
            TextNode("This is text with a link [to boot dev](https://www.boot.dev)", text_type_text)
        ]
        expected = [
            TextNode("No links to show here!", text_type_text),
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode("to youtube", text_type_link, "https://www.youtube.com"),
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev")
        ]

        self.assertListEqual(split_nodes_link(nodes), expected)

if __name__ == "__main__":
    unittest.main()