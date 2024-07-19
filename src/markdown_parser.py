import re

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
    if re.match(r"^#{1,6} ", block) is not None:
        return block_type_header
    if re.match(r"^```(?:.|\n)*?```$", block):
        return block_type_code
    if re.match(r"^> .*?", block, re.MULTILINE):
        return block_type_quote
    if re.match(r"^- .*?", block, re.MULTILINE):
        return block_type_unordered_list
    if re.match(r"\d+\. .*?", block):
        return block_type_ordered_list
    return block_type_paragraph