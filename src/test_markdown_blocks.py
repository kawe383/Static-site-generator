import unittest
from markdown_blocks import *

class TestMarkdownBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
        
        def test_code(self):
            block = "```\nprint('Hello World')\n```"
            assert block_to_block_type(block) == BlockType.CODE


        def test_quote(self):
            block = "> This is a quote\n> This is another line"
            assert block_to_block_type(block) == BlockType.QUOTE


        def test_unordered_list(self):
            block = "- Item 1\n- Item 2\n- Item 3"
            assert block_to_block_type(block) == BlockType.UNORDERED_LIST


        def test_ordered_list(self):
            block = "1. Item 1\n2. Item 2\n3. Item 3"
            assert block_to_block_type(block) == BlockType.ORDERED_LIST


        def test_paragraph(self):
            block = "This is a normal paragraph."
            assert block_to_block_type(block) == BlockType.PARAGRAPH

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
            
        def test_extract_title(self):
            markdown = "# Hello World"
            self.assertEqual(extract_title(markdown), "Hello World")

        def test_extract_title_with_whitespace(self):
            markdown = "#   Hello World   "
            self.assertEqual(extract_title(markdown), "Hello World")

        def test_extract_title_no_header(self):
            markdown = "This is just a paragraph."
            with self.assertRaises(Exception):
                extract_title(markdown)

if __name__ == "__main__":
    unittest.main()