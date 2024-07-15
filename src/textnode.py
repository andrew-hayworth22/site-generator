from htmlnode import LeafNode
from extraction import extract_markdown_images, extract_markdown_links

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def  __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def to_html_node(self):
        if self.text_type == text_type_text:
            return LeafNode(self.text)
        if self.text_type == text_type_bold:
            return LeafNode(self.text, "b")
        if self.text_type == text_type_italic:
            return LeafNode(self.text, "i")
        if self.text_type == text_type_code:
            return LeafNode(self.text, "code")
        if self.text_type == "link":
            return LeafNode(self.text, "a", {"href": self.url})
        if self.text_type == "image":
            return LeafNode("", "img", {"src": self.url, "alt": self.text})
        raise Exception("Invalid text node type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)

        strings = old_node.text.split(delimiter)
        if len(strings) % 2 == 0:
            raise Exception("Invalid Markdown syntax")
        
        for idx in range(len(strings)):
            if len(strings[idx]) == 0:
                continue

            if idx % 2 == 0:
                new_nodes.append(TextNode(strings[idx], "text"))
            else:
                new_nodes.append(TextNode(strings[idx], text_type))
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        string = old_node.text
        for image in images:
            split_strings = string.split(f"![{image[0]}]({image[1]})", 1)
            new_nodes.append(TextNode(split_strings[0], text_type_text))
            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            string = split_strings[1]
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        string = old_node.text
        for link in links:
            split_strings = string.split(f"[{link[0]}]({link[1]})", 1)
            new_nodes.append(TextNode(split_strings[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            string = split_strings[1]
    return new_nodes