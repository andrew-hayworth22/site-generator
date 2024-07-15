from extraction import extract_markdown_images, extract_markdown_links
import unittest

class TestExtraction(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]

        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_single(self):
        text = "This is text with a link [to google](https://www.google.com)"
        expected = [("to google", "https://www.google.com")]

        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_multiple(self):
        text = "This is text with a link [to google](https://www.google.com) and [to youtube](https://www.youtube.com)"
        expected = [("to google", "https://www.google.com"), ("to youtube", "https://www.youtube.com")]

        self.assertListEqual(extract_markdown_links(text), expected)