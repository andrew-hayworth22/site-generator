import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode

class TestHTMLNode(unittest.TestCase):
    def test_eq_true(self):
        props = {"class": "antialiased"}
        node = HTMLNode("body", "Hello world!", None, props.copy())
        node2 = HTMLNode("body", "Hello world!", None, props.copy())

        self.assertEqual(node, node2)

    def test_eq_false(self):
        props = {"class": "antialiased"}
        node = HTMLNode("p", "Hello world!", None, props.copy())
        node2 = HTMLNode("body", "Hello world!", None, props.copy())

        self.assertNotEqual(node, node2)

    def test_props_to_html_no_props(self):
        props = None
        node = HTMLNode("body", "Hello world!", None, props)
        expected = ""

        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_empty_props(self):
        props = {}
        node = HTMLNode("body", "Hello world!", None, props)
        expected = ""

        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_one_prop(self):
        props = {"class": "antialiased"}
        node = HTMLNode("body", "Hello world!", None, props)
        expected = " class=\"antialiased\""

        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_multiple_props(self):
        props = {"class": "antialiased", "style": "color: red"}
        node = HTMLNode("body", "Hello world!", None, props)
        expected = " class=\"antialiased\" style=\"color: red\""

        self.assertEqual(node.props_to_html(), expected)

class TestLeafNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = LeafNode("Some test text")
        expected = "Some test text"

        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_tag(self):
        node = LeafNode("Some test text", "p")
        expected = "<p>Some test text</p>"

        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_props(self):
        props = {"style": "color: red", "class": "antialiasing"}
        node = LeafNode("Some test text", "p", props)
        expected = "<p style=\"color: red\" class=\"antialiasing\">Some test text</p>"

        self.assertEqual(node.to_html(), expected)

    def test_to_html_error_no_value(self):
        node = LeafNode(None, "p")

        self.assertRaises(ValueError, node.to_html)

class TestParentNode(unittest.TestCase):
    def test_to_html_leaf_child(self):
        props = {"style": "color: red", "class": "antialiasing"}
        children = [
            LeafNode("Hello")
        ]
        node = ParentNode("div", children, props)
        expected = "<div style=\"color: red\" class=\"antialiasing\">Hello</div>"

        self.assertEqual(node.to_html(), expected)

    def test_to_html_leaf_children(self):
        props = {"style": "color: red", "class": "antialiasing"}
        children = [
            LeafNode("Hello"),
            LeafNode("paragraph", "p", props)
        ]
        node = ParentNode("div", children, props)
        expected = "<div style=\"color: red\" class=\"antialiasing\">Hello<p style=\"color: red\" class=\"antialiasing\">paragraph</p></div>"

        self.assertEqual(node.to_html(), expected)

    def test_to_html_parent_children(self):
        props = {"style": "color: red", "class": "antialiasing"}
        children = [
            LeafNode("Hello"),
            LeafNode("paragraph", "p", props),
            ParentNode("div", [LeafNode("text")])
        ]
        node = ParentNode("div", children, props)
        expected = "<div style=\"color: red\" class=\"antialiasing\">Hello<p style=\"color: red\" class=\"antialiasing\">paragraph</p><div>text</div></div>"

        self.assertEqual(node.to_html(), expected)

    def test_to_html_error_no_tag(self):
        children = [
            LeafNode("Hello")
        ]
        node = ParentNode(None, children)

        self.assertRaises(ValueError, node.to_html)

    def test_to_html_error_no_children(self):
        node = ParentNode("div", None)

        self.assertRaises(ValueError, node.to_html)

    def test_to_html_error_empty_children(self):
        children = []
        node = ParentNode("div", children)

        self.assertRaises(ValueError, node.to_html)