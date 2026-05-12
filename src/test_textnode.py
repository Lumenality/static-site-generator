import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("print(hello world)", TextType.CODE)
        node4 = TextNode("This is a text node", TextType.BOLD,None)
        node5 = TextNode("print(hello world)", TextType.CODE,"https://www.learnpython.org/en/Hello%2C_World%21")

        self.assertEqual(node, node2)
        self.assertNotEqual(node,node3)
        self.assertNotEqual(node2,node3)
        self.assertEqual(node,node4)
        self.assertNotEqual(node3,node5)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()