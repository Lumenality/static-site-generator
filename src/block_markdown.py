from enum import Enum

from inline_markdown import text_to_children
from htmlnode import ParentNode, LeafNode
from textnode import TextType, TextNode, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    """
    Output: List of stripped lines of markdown text
    """
    split_markdown = markdown.split("\n\n")
    result = []
    for line in split_markdown:
        line = line.strip()
        if line == "":
            continue
        result.append(line)

    return result


def markdown_to_html_node(markdown_text):
    blocks = markdown_to_blocks(markdown_text)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_block_type(markdown_text):
    headings = [
        "#",
        "##",
        "###",
        "####",
        "#####",
        "######",
    ]
    code_blocks = "```"
    quote_blocks = ">"
    unordered_lists = "- "
    ordered_lists = "1"
    if markdown_text.split(" ", 1)[0] in headings:
        # result = markdown_text.split(" ",1)[1]
        return BlockType.HEADING

    if (
        markdown_text.split("\n", 1)[0][:3] == code_blocks
        and markdown_text[-3:] == code_blocks
    ):
        # result = f"ICH BIN CODE: {markdown_text.split("\n",1)[1][:-3]}".strip()
        return BlockType.CODE

    if markdown_text[0] == quote_blocks:
        for line in markdown_text.split("\n"):
            if line.strip()[0] != quote_blocks:
                return BlockType.PARAGRAPH

        return BlockType.QUOTE

    if markdown_text[:2] == unordered_lists:
        for line in markdown_text.split("\n"):
            if not line.startswith(unordered_lists):
                return BlockType.PARAGRAPH

        return BlockType.UNORDERED_LIST

    if markdown_text[0] == ordered_lists:
        counter = 1
        for line in markdown_text.split("\n"):
            if not line.startswith(f"{counter}. "):
                return BlockType.PARAGRAPH

            counter += 1

        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_children(block.replace("\n"," ")))

        case BlockType.HEADING:
            heading_level = len(block.split(" ", 1)[0])
            return ParentNode(
                f"h{heading_level}", text_to_children(block.split(" ", 1)[1])
            )

        case BlockType.CODE:
            code_node = TextNode((block.split("\n", 1)[1][:-3]), TextType.CODE)
            return ParentNode("pre", [text_node_to_html_node(code_node)])

        case BlockType.QUOTE:
            lines = []
            for line in block.split("\n"):
                lines.append(line[1:])
            quote = " ".join(lines)
            return ParentNode("blockquote", text_to_children(quote))

        case BlockType.UNORDERED_LIST:
            list_items = []

            for line in block.split("\n"):
                item_text = line[2:]
                list_items.append(ParentNode("li", text_to_children(item_text)))

            return ParentNode("ul", list_items)

        case BlockType.ORDERED_LIST:
            list_items = []

            for line in block.split("\n"):
                _, item_text = line.split(" ", 1)
                list_items.append(ParentNode("li", text_to_children(item_text)))

            return ParentNode("ol", list_items)

        case _:
            raise ValueError(f"unknown text node type: {block_type}")

# quote = ">Ernest\n>Hemingway"
# print(block_to_html_node(quote,block_to_block_type(quote)).to_html())
# unordered_list = "- item 1\n- item 2\n- item 3"
# print(block_to_html_node(unordered_list,block_to_block_type(unordered_list)).to_html())
# ordered_list = "1. item 1\n2. item 2\n3. item 3"
# print(block_to_html_node(ordered_list,block_to_block_type(ordered_list)).to_html())
