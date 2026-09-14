
from enum import Enum
from split_delimiter import *
from textnode import *



def markdown_to_blocks(markdown):
    result = []
    strings = markdown.split("\n\n")
    for string in strings:
        stripped = string.strip()
        if stripped != "":
            result.append(stripped)
    return result

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith(("```\n")) and block.endswith(("```")):
        return BlockType.CODE
    lines = block.split("\n")
    if all(line.startswith((">")) for line in lines):
            return BlockType.QUOTE
    if all(line.startswith(("- ")) for line in lines):
            return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    nodes_list = text_to_textnodes(text)
    html_nodes = []
    for node in nodes_list:
        new_html_node = text_node_to_html_node(node)
        html_nodes.append(new_html_node)
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_node_list = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            split_block = block.split("\n")
            joined_block = " ".join(split_block)
            child_nodes = text_to_children(joined_block)
            paragraph_node = ParentNode("p", child_nodes)
            html_node_list.append(paragraph_node)
        elif block_type == BlockType.HEADING:
            counter = 0
            for char in block:
                if char == "#":
                    counter += 1
                else:
                    break
            child_nodes = text_to_children(block[counter+1:])
            heading_node = ParentNode(f"h{counter}", child_nodes)
            html_node_list.append(heading_node)
        elif block_type == BlockType.QUOTE:
            split_block = block.split("\n")
            stripped_block = []
            for line in split_block:
                stripped_block.append(line.strip("> "))
            joined_block = " ".join(stripped_block)
            child_nodes = text_to_children(joined_block)
            quote_node = ParentNode("blockquote", child_nodes)
            html_node_list.append(quote_node)
        elif block_type == BlockType.UNORDERED_LIST:
            split_block = block.split("\n")
            inner_block = []
            for line in split_block:
                children = text_to_children(line.strip("- "))
                inner_child = ParentNode("li", children)
                inner_block.append(inner_child)
            unordered_node = ParentNode("ul", inner_block)
            html_node_list.append(unordered_node)
        elif block_type == BlockType.ORDERED_LIST:
            split_block = block.split("\n")
            inner_block = []
            for line in split_block:
                index = line.index(".")
                children = text_to_children(line[index+2:])
                inner_child = ParentNode("li", children)
                inner_block.append(inner_child)
            ordered_node = ParentNode("ol", inner_block)
            html_node_list.append(ordered_node)
        elif block_type == BlockType.CODE:
            code_text = block[4:-3]
            node = TextNode(code_text, TextType.TEXT)
            html_node = text_node_to_html_node(node)
            parent_one = ParentNode("code", [html_node])
            code_node = ParentNode("pre", [parent_one])
            html_node_list.append(code_node)
    return ParentNode("div", html_node_list)
            

def extract_title(markdown):
    split = markdown.split("\n")
    for line in split:
        if line.startswith("# "):
            header = line[2:]
            return header.strip()
    raise Exception("no header")