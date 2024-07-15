from textnode import TextNode, split_nodes_delimiter
def main():
    test_node = TextNode("*testing* *text* nodes", "text", "https://www.google.com")
    strings = split_nodes_delimiter([test_node], "*", "bold")
    print(strings)
main()