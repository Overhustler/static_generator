from textnode import *
import re
from blocktypes import *
from parentnode import ParentNode
from leafnode import LeafNode
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Invalid markup syntax")
        
        if node.text.count(delimiter) == 0:
            new_nodes.append(node)
            continue

        text_list = node.text.split(delimiter)
        temp_nodes = []

        for index, text in enumerate(text_list):
            
            if index % 2 != 0:
                temp_nodes.append(TextNode(text, text_type))
            else:
                temp_nodes.append(TextNode(text, TextType.TEXT))
        new_nodes.extend(temp_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        new_string = ""
        first_iter = True

        for i in images:
            if first_iter:
                string_tuple = node.text.partition(f"![{i[0]}]({i[1]})")
                first_iter = False
            else:
                string_tuple = new_string.partition(f"![{i[0]}]({i[1]})")

            new_string = string_tuple[2]

            if string_tuple[1] != "":
                if string_tuple[0] != "":
                    new_nodes.append(TextNode(string_tuple[0], TextType.TEXT))
                new_nodes.append(TextNode(i[0], TextType.IMAGE, i[1]))
            else:
                new_nodes.append(TextNode(i[0], TextType.IMAGE, i[1]))
                first_iter = True

        if new_string != "":
            new_nodes.append(TextNode(new_string, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        new_string = ""
        first_iter = True
        
        for i in links:
            if first_iter:
                string_tuple = node.text.partition(f"[{i[0]}]({i[1]})")
                first_iter = False
            else:
                string_tuple = new_string.partition(f"[{i[0]}]({i[1]})")

            new_string = string_tuple[2]

            if string_tuple[1] != "":
                if string_tuple[0] != "":
                    new_nodes.append(TextNode(string_tuple[0], TextType.TEXT))
                new_nodes.append(TextNode(i[0], TextType.LINK, i[1]))
            else:
                new_nodes.append(TextNode(i[0], TextType.LINK, i[1]))
                first_iter = True

        if new_string != "":
            new_nodes.append(TextNode(new_string, TextType.TEXT))

    return new_nodes
def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split("\n\n")]
    non_empty_blocks = [item for item in blocks if item]
    return non_empty_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    processed_blocks = []

    for block in blocks:
        type =  block_to_block_type(block)
        processed_blocks.append(process_block(type, block))
    
    html_file = ParentNode("div", processed_blocks)
    return html_file

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def process_block(block_type, block):
     block_node = None
     match block_type:
        case BlockType.PARAGRAPH:
            block_node = ParentNode("p", text_to_children(block))
            return block_node

        case BlockType.HEADING:
            split_block = structure_heading(block)
            htag = "h" + str(split_block[0])
            block_node = ParentNode(htag, text_to_children(split_block[1]))
            return block_node

        case BlockType.CODE:
            block_node = ParentNode("pre", structure_code(block))
            return block_node

        case BlockType.QUOTE:
            stripped_block = structure_quote(block)
            block_node = ParentNode("blockquote", text_to_children(stripped_block))
            return block_node

        case BlockType.UNORDERED_LIST:
            block_node = ParentNode("ul", text_to_children(structure_list(block)))
            return block_node

        case BlockType.ORDERED_LIST:
            block_node = ParentNode("ol", text_to_children(structure_list(block)))
            return block_node

        case _:
            raise ValueError(f"Unknown block type: {block_type}")
    
def structure_heading(block):
    seperated_hashtags = block.split(" ", 1)
    hashtags = seperated_hashtags[0]
    rest_of_block = seperated_hashtags[1].lstrip()
    num_of =  hashtags.count("#")
    return num_of, rest_of_block

def structure_quote(block):
    new_block = ""
    for line in block.split("\n"):
        new_block += line.split(" ", 1)[1].lstrip()
    return new_block

def structure_list(block):
    nodes = []
    for line in block.split("\n"):
        nodes.append(ParentNode("li", text_to_children(line)))
    return nodes
def structure_code(block):
    block_text = block[4:-4]
    code_textnode = TextNode(block_text, TextType.CODE)
    code_node = text_node_to_html_node(code_textnode)
    return code_node