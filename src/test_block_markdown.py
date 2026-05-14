import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_html_node


class TestBlockMarkdown(unittest.TestCase):
    def test_block_to_block_type_recognizes_block_types(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(
            block_to_block_type("> Quote line\n> Another line"), BlockType.QUOTE
        )
        self.assertEqual(
            block_to_block_type("- item\n- item 2"), BlockType.UNORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("1. first\n2. second"), BlockType.ORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("A normal paragraph."), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_returns_paragraph_for_non_block_prefixes(self):
        self.assertEqual(block_to_block_type("Not a heading #tag"), BlockType.PARAGRAPH)
        self.assertEqual(
            block_to_block_type("1 item, but not a list"), BlockType.PARAGRAPH
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
