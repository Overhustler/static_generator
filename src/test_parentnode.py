import unittest
from parentnode import ParentNode
from leafnode import LeafNode
class TestParentNode(unittest.TestCase):
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
    def test_to_html_multiple_children(self):
        c1 = LeafNode("span", "one")
        c2 = LeafNode("span", "two")
        parent = ParentNode("div", [c1, c2])
        self.assertEqual(parent.to_html(), "<div><span>one</span><span>two</span></div>")

    def test_error_no_tag(self):
        c1 = LeafNode("span", "child")
        parent = ParentNode(None, [c1])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_error_no_children(self):
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_nested_parent_nodes_three_levels(self):
        lvl3 = LeafNode("i", "deep")
        lvl2 = ParentNode("b", [lvl3])
        lvl1 = ParentNode("span", [lvl2])
        root = ParentNode("div", [lvl1])
        self.assertEqual(root.to_html(), "<div><span><b><i>deep</i></b></span></div>")

    def test_children_are_rendered_in_order(self):
        c1 = LeafNode("span", "A")
        c2 = LeafNode("span", "B")
        c3 = LeafNode("span", "C")
        parent = ParentNode("div", [c1, c2, c3])
        self.assertEqual(parent.to_html(), "<div><span>A</span><span>B</span><span>C</span></div>")