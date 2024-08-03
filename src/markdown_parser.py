import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_to_textnodes, TextNode

block_type_paragraph = "paragraph"
block_type_header = "header"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(map(lambda x: x.strip(), blocks))

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return block_type_header
    if re.match(r"^```(?:.|\n)*?```$", block):
        return block_type_code
    if re.match(r"^> .*?", block, re.MULTILINE):
        return block_type_quote
    if re.match(r"^\* .*?", block, re.MULTILINE):
        return block_type_unordered_list
    if re.match(r"^\d+\. .*?", block):
        return block_type_ordered_list
    return block_type_paragraph

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes_map = map(lambda x: x.to_html_node(), text_nodes)
    return list(html_nodes_map)

def create_paragraph_node(block):
    nodes = text_to_children(block)
    return ParentNode("p", nodes)

def create_header_node(block):
    text = re.findall(r"^(#{1,6}) (.*)", block)[0]
    children = text_to_children(text[1])
    return ParentNode(f"h{len(text[0])}", children)

def create_code_node(block):
    text = re.findall(r"^```(.*)```$", block, re.DOTALL)[0]
    children = text_to_children(text)
    return ParentNode("code", children)

def create_quote_node(block):
    split_block = block.split("\n")
    removed_start = list(map(lambda x: re.findall(r"^> (.*)", x, re.DOTALL)[0], split_block))
    text = "\n".join(removed_start)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def create_unordered_list_node(block):
    split_block = block.split("\n")
    removed_start = list(map(lambda x: re.findall(r"^\* (.*)", x, re.DOTALL)[0], split_block))
    children = list(map(lambda x: ParentNode("li", text_to_children(x)), removed_start))
    return ParentNode("ul", children)

def create_ordered_list_node(block):
    split_block = block.split("\n")
    removed_start = list(map(lambda x: re.findall(r"^(?:\d+\.) (.*)", x, re.DOTALL)[0], split_block))
    children = list(map(lambda x: ParentNode("li", text_to_children(x)), removed_start))
    return ParentNode("ol", children)

def markdown_to_html_node(markdown):
    children_nodes = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == block_type_paragraph:
            children_nodes.append(create_paragraph_node(block))
        elif block_type == block_type_header:
            children_nodes.append(create_header_node(block))
        elif block_type == block_type_code:
            children_nodes.append(create_code_node(block))
        elif block_type == block_type_quote:
            children_nodes.append(create_quote_node(block))
        elif block_type == block_type_unordered_list:
            children_nodes.append(create_unordered_list_node(block))
        elif block_type == block_type_ordered_list:
            children_nodes.append(create_ordered_list_node(block))

    return ParentNode("div", children_nodes)

def extract_title(markdown):
    title = re.findall("# (.*)", markdown)
    if len(title) == 0:
        raise Exception("No title found in markdown")
    
    return title[0]