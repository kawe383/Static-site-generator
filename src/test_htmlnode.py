import unittest
from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq_props(self):
        node = HTMLNode(props={"class": "greeting", "href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' class="greeting" href="https://boot.dev"')

    def test_eq_None(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr_htmlnode(self):
        props = {'class': 'greeting', 'href': 'https://boot.dev'}
        node = HTMLNode(tag="p", value="joeking", props={"class": "greeting", "href": "https://boot.dev"})
        self.assertEqual(node.__repr__(), f"HTMLNode(p, joeking, None, {props})")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_LeafNode_no_value(self):
        node = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_tag_none(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_with_props(self):
        node = LeafNode("p", "Hello, world!", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<p href="https://boot.dev">Hello, world!</p>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")
        
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], props={"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><span>child</span></div>')


if __name__ == "__main__":
    unittest.main()