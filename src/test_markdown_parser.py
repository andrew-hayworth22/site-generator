import unittest
from markdown_parser import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_header,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list
)

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
