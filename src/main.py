import os
import shutil
from markdown_parser import markdown_to_html_node, extract_title
from htmlnode import HTMLNode

def main():
    copy_directory("./static", "./public")
    generate_pages("./content", "./template.html", "./public")

def copy_directory(source_path, destination_path):
    if not os.path.exists(source_path):
        raise Exception("Source path does not exist")

    if os.path.exists(destination_path):
        print(f"Removing {destination_path}")
        shutil.rmtree(destination_path)
    
    print(f"Creating directory: {destination_path}")
    os.mkdir(destination_path)

    files = os.listdir(source_path)
    for file in files:
        source_file_path = f"{source_path}/{file}"
        destination_file_path = os.path.join(destination_path, file)

        if os.path.isdir(source_file_path):
            copy_directory(source_file_path, destination_file_path)
        else:
            print(f"Creating file: {destination_file_path}")
            shutil.copy(source_file_path, destination_file_path)

def generate_page(source_path, template_path, destination_path):
    if not os.path.exists(source_path):
        raise Exception(f"Markdown file {source_path} does not exist")

    if not os.path.exists(template_path):
        raise Exception(f"Template file {template_path} does not exist")

    print(f"Generating page from {source_path} to {destination_path} using {template_path}")

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    markdown_file = open(source_path)
    html_file = open(os.path.join(destination_path, "index.html"), "w")
    template_file = open(template_path)

    markdown = markdown_file.read()
    template = template_file.read()

    html_node = markdown_to_html_node(markdown)

    html = html_node.to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    html_file.write(template)

    markdown_file.close()
    html_file.close()

def generate_pages(source_path, template_path, destination_path):
    if not os.path.exists(source_path):
        raise Exception(f"Directory {source_path} does not exist")
    
    files = os.listdir(source_path)
    for file in files:
        if not file.endswith(".md"):
            raise Exception(f"Malformed file in content directory: {file}")

        route_name = file.replace(".md", "")

        source_file_path = os.path.join(source_path, file)
        if source_file_path.find("index.md") != -1:
            destination_file_path = destination_path
        else:
            destination_file_path = os.path.join(destination_path, route_name)

        generate_page(source_file_path, template_path, destination_file_path)

main()