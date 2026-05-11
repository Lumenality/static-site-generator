import unittest

from htmlnode import HTMLNode,LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode()
        node2 = HTMLNode(None,None,None,None)
        node3 = HTMLNode("a", None, None, {
            "href": '"https://www.google.com"',
            "target": "_blank",
        })

        self.assertEqual(node1.tag, node2.tag)
        self.assertNotEqual(node1.tag,node3.tag)
        self.assertNotEqual(node2.props,node3.props)
        print(node1)
        print(node3.props_to_html())

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        print(node.to_html())
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

if __name__ == "__main__":
    unittest.main()