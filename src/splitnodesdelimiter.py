from textnode import TextNode,TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []


    for old_node in old_nodes:

        if old_node.text_type is not TextType.TEXT:
            nodes.append(old_node)
            continue

        split_parts = old_node.text.split(delimiter)
        
        if len(split_parts) %2 == 0 :
            raise Exception("no closing delimiter found")

        for i in range(len(split_parts)):
            if i % 2 == 0:
                nodes.append(TextNode(split_parts[i], TextType.TEXT))
            else:
                nodes.append(TextNode(split_parts[i], text_type))
                    
    return nodes
