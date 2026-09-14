import os
from markdown_blocks import *
from htmlnode import *



def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        contents_from_path = f.read()
    with open(template_path) as f:
        contents_temp_path = f.read()
    html_node_from_path = markdown_to_html_node(contents_from_path)
    result = html_node_from_path.to_html()
    title = extract_title(contents_from_path)
    page = contents_temp_path.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", result)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')
    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_content = os.listdir(dir_path_content)
    for entry in dir_content:
        full_path = os.path.join(dir_path_content, entry)
        dest_entry = entry.replace(".md", ".html")
        destination_path = os.path.join(dest_dir_path, dest_entry)
        if os.path.isfile(full_path):
            generate_page(full_path, template_path, destination_path, basepath)
        else:
            generate_pages_recursive(full_path, template_path, destination_path, basepath)
