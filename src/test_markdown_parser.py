import unittest
from markdown_parser import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    block_type_paragraph,
    block_type_header,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list
)
from htmlnode import HTMLNode, ParentNode, LeafNode

class TestMarkdownToBlocks(unittest.TestCase):
    def test_new_line(self):
        text = "This is some markdown\nFor a test!"
        expected = [
            "This is some markdown\nFor a test!"
        ]

        self.assertListEqual(markdown_to_blocks(text), expected)
    
    def test_eliminated_empty_space(self):
        text = "  \t  This is some markdown \n\n   For a test!"
        expected = [
            "This is some markdown",
            "For a test!"
        ]

        self.assertListEqual(markdown_to_blocks(text), expected)

    def test_multiple_line_blocks(self):
        text = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]

        self.assertListEqual(markdown_to_blocks(text), expected)

class TestBlockToBlockType(unittest.TestCase):
    def test_header_1(self):
        block = "# header 1"
        expected = block_type_header

        self.assertEqual(block_to_block_type(block), expected)
    def test_header_6(self):
        block = "###### header 6"
        expected = block_type_header

        self.assertEqual(block_to_block_type(block), expected)
    def test_header_7_is_paragraph(self):
        block = "####### header 7"
        expected = block_type_paragraph

        self.assertEqual(block_to_block_type(block), expected)
    def test_malformed_header_is_paragraph(self):
        block = "#header 1"
        expected = block_type_paragraph

        self.assertEqual(block_to_block_type(block), expected)
    def test_code_block(self):
        block = "```code block```"
        expected = block_type_code

        self.assertEqual(block_to_block_type(block), expected)
    def test_code_block_multine(self):
        block = "```code block\nthis is another line\n of code```"
        expected = block_type_code

        self.assertEqual(block_to_block_type(block), expected)
    def test_malformed_code_block_is_paragraph(self):
        block = "```code block\nthis is another line"
        expected = block_type_paragraph

        self.assertEqual(block_to_block_type(block), expected)
    def test_quote_block(self):
        block = "> this is a quote"
        expected = block_type_quote

        self.assertEqual(block_to_block_type(block), expected)
    def test_quote_block_multiline(self):
        block = "> this is a quote\n> this is a new line"
        expected = block_type_quote

        self.assertEqual(block_to_block_type(block), expected)
    def test_malformed_quote_block_is_paragraph(self):
        block = ">this is a quote\n> this is a new line"
        expected = block_type_paragraph

        self.assertEqual(block_to_block_type(block), expected)
    def test_unordered_list(self):
        block = "- this is an unordered list item"
        expected = block_type_unordered_list

        self.assertEqual(block_to_block_type(block), expected)
    def test_unordered_list_multiline(self):
        block = "- this is an unordered list item\n- this is the next item"
        expected = block_type_unordered_list

        self.assertEqual(block_to_block_type(block), expected)
    def test_malformed_unordered_list_is_paragraph(self):
        block = "-this is an unordered list item\n- this is the next item"
        expected = block_type_paragraph

        self.assertEqual(block_to_block_type(block), expected)
    def test_ordered_list(self):
        block = "1. this is an ordered list item"
        expected = block_type_ordered_list

        self.assertEqual(block_to_block_type(block), expected)
    def test_ordered_list_multiline(self):
        block = "1. this is an ordered list item\n21. this is the next item"
        expected = block_type_ordered_list

        self.assertEqual(block_to_block_type(block), expected)
    def test_malformed_ordered_list_is_paragraph(self):
        block = "1.this is an ordered list item\n- this is the next item"
        expected = block_type_paragraph

        self.assertEqual(block_to_block_type(block), expected)
    def test_paragraph(self):
        block = "This is a paragraph of test.\nThis is going to be awesome"
        expected = block_type_paragraph

        self.assertEqual(block_to_block_type(block), expected)

class TestMarkdownToHTMLNodes(unittest.TestCase):
    def test_all(self):
        markdown = "hello world!\n\n# This is a header 1\n\n## Header 2 **IMPORTANT**\n\n### Header 3\n\n#### Header 4\n\n##### Header 5\n\n###### Header 6\n\n```let x = 1;\nlet y = 5;```\n\n> This\n> is a\n> *block quote*\n\n- Here are three items\n- Second\n- Third\n\n1. First\n2. Second\n3. Third"
        expected = ParentNode("div", [
            ParentNode("p", [
                LeafNode("hello world!")
            ]),
            ParentNode("h1", [
                LeafNode("This is a header 1")
            ]),
            ParentNode("h2", [
                LeafNode("Header 2 "),
                LeafNode("IMPORTANT", "b")
            ]),
            ParentNode("h3", [
                LeafNode("Header 3")
            ]),
            ParentNode("h4", [
                LeafNode("Header 4")
            ]),
            ParentNode("h5", [
                LeafNode("Header 5")
            ]),
            ParentNode("h6", [
                LeafNode("Header 6")
            ]),
            ParentNode("code", [
                LeafNode("let x = 1;\nlet y = 5;")
            ]),
            ParentNode("blockquote", [
                LeafNode("This\nis a\n"),
                LeafNode("block quote", "i")
            ]),
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode("Here are three items")
                ]),
                ParentNode("li", [
                    LeafNode("Second")
                ]),
                ParentNode("li", [
                    LeafNode("Third")
                ])
            ]),
            ParentNode("ol", [
                ParentNode("li", [
                    LeafNode("First")
                ]),
                ParentNode("li", [
                    LeafNode("Second")
                ]),
                ParentNode("li", [
                    LeafNode("Third")
                ])
            ])
        ])

        result = markdown_to_html_node(markdown)

        self.assertEqual(result, expected)

    def test_text_block(self):
        markdown = "hello world!"
        expected = ParentNode("div", [
            ParentNode("p", [
                LeafNode("hello world!")
            ])
        ])

        result = markdown_to_html_node(markdown)

        self.assertEqual(result, expected)

    def test_headers(self):
        markdown = "# This is a header 1\n\n## Header 2 **IMPORTANT**\n\n### Header 3\n\n#### Header 4\n\n##### Header 5\n\n###### Header 6"
        expected = ParentNode("div", [
            ParentNode("h1", [
                LeafNode("This is a header 1")
            ]),
            ParentNode("h2", [
                LeafNode("Header 2 "),
                LeafNode("IMPORTANT", "b")
            ]),
            ParentNode("h3", [
                LeafNode("Header 3")
            ]),
            ParentNode("h4", [
                LeafNode("Header 4")
            ]),
            ParentNode("h5", [
                LeafNode("Header 5")
            ]),
            ParentNode("h6", [
                LeafNode("Header 6")
            ])
        ])

        result = markdown_to_html_node(markdown)

        self.assertEqual(result, expected)