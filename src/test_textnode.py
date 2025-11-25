import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()