import re

from textnode import TextNode, TextType, text_node_to_html_node


# Regex extratction of markdown for files and images from text
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


# Splitter functions
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            nodes.append(old_node)
            continue

        split_parts = old_node.text.split(delimiter)

        if len(split_parts) % 2 == 0:
            raise Exception("no closing delimiter found")

        for i in range(len(split_parts)):
            if i % 2 == 0:
                nodes.append(TextNode(split_parts[i], TextType.TEXT))
            else:
                nodes.append(TextNode(split_parts[i], text_type))

    return nodes


def split_nodes_image(old_nodes):
    images = []
    nodes = []

    for node in old_nodes:
        original_text = node.text

        images = extract_markdown_images(node.text)

        if len(images) == 0:
            nodes.append(node)
            continue

        # sections = []
        remaining_text = original_text
        for image_alt, image_link in images:
            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            remaining_text = sections[1]

            if len(sections) == 1:
                nodes.append(TextNode(sections[0], TextType.TEXT))
                continue

            if sections[0] != "":
                nodes.append(TextNode(sections[0], TextType.TEXT))

            nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

        # Append the remainder text at the end if there is any
        if remaining_text != "":
            nodes.append(TextNode(remaining_text, TextType.TEXT))

    return nodes


def split_nodes_link(old_nodes):
    links = []
    nodes = []

    for node in old_nodes:
        original_text = node.text

        links = extract_markdown_links(node.text)

        if len(links) == 0:
            nodes.append(node)
            continue

        # sections = []
        remaining_text = original_text
        for link_text, link in links:
            sections = remaining_text.split(f"[{link_text}]({link})", 1)
            remaining_text = sections[1]

            if len(sections) == 1:
                nodes.append(TextNode(sections[0], TextType.TEXT))
                continue

            if sections[0] != "":
                nodes.append(TextNode(sections[0], TextType.TEXT))

            nodes.append(TextNode(link_text, TextType.LINK, link))

        # Append the remainder text at the end if there is any
        if remaining_text != "":
            nodes.append(TextNode(remaining_text, TextType.TEXT))

    return nodes


def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    text_nodes_bold_split = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    text_nodes_italic_split = split_nodes_delimiter(
        text_nodes_bold_split, "_", TextType.ITALIC
    )
    text_nodes_code_split = split_nodes_delimiter(
        text_nodes_italic_split, "`", TextType.CODE
    )
    text_nodes_image_split = split_nodes_image(text_nodes_code_split)
    text_nodes_link_split = split_nodes_link(text_nodes_image_split)

    return text_nodes_link_split


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children


if __name__ == "__main__":
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    split_node = split_nodes_image([node])
    print(split_node)
