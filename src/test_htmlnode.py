import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_prop_return_empty(self):
        node = HTMLNode()
        node_prop_val = node.props_to_html()
        self.assertTrue(node_prop_val == "")

    def test_prop_format(self):
        prop = {
        "href": "https://www.google.com",
        "target": "_blank",
        }
        node = HTMLNode(props=prop)
        str = node.props_to_html()
    
        self.assertTrue(str == ' href="https://www.google.com" target="_blank"')
    
    def test_repr_output(self):
        prop = {
        "href": "https://www.google.com",
        "target": "_blank",
        }
        node = HTMLNode(tag="<p>", value="The paragraph", props=prop)
        self.assertTrue(f"{node}" == "HTMLNode(tag=<p>, value=The paragraph, children=None, props={'href': 'https://www.google.com', 'target': '_blank'})")