import unittest

from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_urldiffnone(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This", TextType.TEXT, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        self.assertNotEqual(node, node2)

    def text_urldifferent(self):
        node = TextNode("This is a text node", TextType.LINK, "https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        self.assertNotEqual(node, node2)

    def test_all_different(self):
        node = TextNode("This is a text node", TextType.LINK, "https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository")
        node2 = TextNode("This", TextType.IMAGE, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_text_type_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "b")
        self.assertEqual(html.value, "bold text")

    def test_text_type_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "i")
        self.assertEqual(html.value, "italic text")

    def test_text_type_code(self):
        node = TextNode("code here", TextType.CODE)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "code")
        self.assertEqual(html.value, "code here")

    def test_text_type_link(self):
        node = TextNode("Google", TextType.LINK, url="https://google.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.value, "Google")
        self.assertEqual(html.props, {"href": "https://google.com"})

    def test_text_type_image(self):
        node = TextNode("An image", TextType.IMAGE, url="img.png")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.value, "")
        self.assertEqual(html.props, {"src": "img.png", "alt": "An image"})

    def test_invalid_text_type_raises(self):
        class Fake: pass
        node = TextNode("hello", Fake)  # not a TextType enum
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


