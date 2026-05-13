import unittest
from textnode import TextType,TextNode
from splitnodesdelimiter import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        print(new_nodes)
        self.assertEqual(new_nodes,[TextNode('This is text with a ', TextType.TEXT, None), TextNode('code block', TextType.CODE, None), TextNode(' word', TextType.TEXT, None)])

if __name__ == "__main__":
    unittest.main()