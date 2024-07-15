from htmlnode import LeafNode

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