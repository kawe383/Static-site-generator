import unittest
from split_delimiter import *


class TestSplitDelimiter(unittest.TestCase):

    def test_eq(self):
        old_node1 = TextNode("I hate **this** so much", TextType.TEXT)
        
        old_nodes = [old_node1]
        self.assertEqual(split_nodes_delimiter(old_nodes, "**", TextType.BOLD), [TextNode("I hate ", TextType.TEXT), TextNode("this", TextType.BOLD), TextNode(" so much", TextType.TEXT)])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_images_2(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_all_formats(self):
        text = (
            "This is **bold**, _italic_, `code`, "
            "[link](https://example.com), and "
            "![image](image.png)."
        )
        
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(", and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "image.png"),
            TextNode(".", TextType.TEXT),
        ]
        
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()