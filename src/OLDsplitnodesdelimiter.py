from textnode import TextNode,TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []


    for old_node in old_nodes:

        if old_node.text_type is not TextType.TEXT:
            nodes.append(old_node)
            continue

        normal_text = ""
        delimiter_text = ""
        delimiter_editing = False

        for char in old_node.text:
            if char == delimiter:
                delimiter_editing = not delimiter_editing
                if normal_text != "":
                    nodes.append(TextNode(normal_text, TextType.TEXT))
                    normal_text = ""
                    continue

                if delimiter_text != "":
                    nodes.append(TextNode(delimiter_text, text_type))
                    delimiter_text = ""
                    continue

            elif delimiter_editing:
                delimiter_text += char

            else:
                normal_text += char

        if normal_text != "":
            nodes.append(TextNode(normal_text, TextType.TEXT))
                    
        if delimiter_editing is True:
            raise Exception("no closing delimiter found")

    return nodes

node = TextNode("This is text with a `code block` word", TextType.TEXT)
new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
print(new_nodes)