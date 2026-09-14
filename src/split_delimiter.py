from htmlnode import *
from textnode import *
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
        if node.text_type == TextType.TEXT:
            split_node = node.text.split(delimiter)
            if len(split_node) % 2 == 0:
                raise ValueError("invalid markdown")
            for i in range(len(split_node)):
                if split_node[i] == "":
                    continue
                if i % 2 == 0:
                    new_list.append(TextNode(split_node[i], TextType.TEXT)) 
                else:
                    new_list.append(TextNode(split_node[i], text_type))
    return new_list
        
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
        if node.text_type == TextType.TEXT:
            split_node = extract_markdown_images(node.text)
            if split_node == []:
                new_list.append(node)
                continue
            current_text = node.text
            for image_alt, image_url in split_node:
                sections = current_text.split(f"![{image_alt}]({image_url})", 1)
                if sections[0] != "":
                    new_list.append(TextNode(sections[0], TextType.TEXT))
                new_list.append(TextNode(image_alt, TextType.IMAGE, image_url))
                current_text = sections[1]
            if current_text != "":
                new_list.append(TextNode(current_text, TextType.TEXT))
    return new_list
                


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
        if node.text_type == TextType.TEXT:
            split_node = extract_markdown_links(node.text)
            if split_node == []:
                new_list.append(node)
                continue
            current_text = node.text
            for link_anchor, link_url in split_node:
                sections = current_text.split(f"[{link_anchor}]({link_url})", 1)
                if sections[0] != "":
                    new_list.append(TextNode(sections[0], TextType.TEXT))
                new_list.append(TextNode(link_anchor, TextType.LINK, link_url))
                current_text = sections[1]
            if current_text != "":
                new_list.append(TextNode(current_text, TextType.TEXT))
    return new_list


def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    node = split_nodes_delimiter(node, "**", TextType.BOLD)
    node = split_nodes_delimiter(node, "_", TextType.ITALIC)
    node = split_nodes_delimiter(node, "`", TextType.CODE)
    node = split_nodes_image(node)
    node = split_nodes_link(node)
    return node


