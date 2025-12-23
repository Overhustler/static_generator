import unittest
from textnode import TextNode, TextType
from functions import *

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_simple_pair(self):
        old = [TextNode("This is *bold* text", TextType.TEXT)]
        result = split_nodes_delimiter(old, "*", TextType.BOLD)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(result[2], TextNode(" text", TextType.TEXT))

    def test_multiple_pairs(self):
        old = [TextNode("A *bold* and *strong* test", TextType.TEXT)]
        result = split_nodes_delimiter(old, "*", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("A ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("strong", TextType.BOLD),
            TextNode(" test", TextType.TEXT),
        ])

    def test_no_delimiters(self):
        old = [TextNode("No markup here", TextType.TEXT)]
        result = split_nodes_delimiter(old, "*", TextType.BOLD)
        self.assertEqual(result, old)  # unchanged

    def test_non_text_nodes_are_unchanged(self):
        old = [
            TextNode("skip me", TextType.BOLD),
            TextNode("normal *text*", TextType.TEXT)
        ]
        result = split_nodes_delimiter(old, "*", TextType.ITALIC)

        # First should be unchanged
        self.assertEqual(result[0], TextNode("skip me", TextType.BOLD))

        # second should be split
        self.assertEqual(result[1], TextNode("normal ", TextType.TEXT))
        self.assertEqual(result[2], TextNode("text", TextType.ITALIC))

    def test_raises_on_odd_number_of_delimiters(self):
        old = [TextNode("Bad *syntax", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old, "*", TextType.BOLD)

    def test_handles_empty_sections(self):
        old = [TextNode("*bold*", TextType.TEXT)]
        result = split_nodes_delimiter(old, "*", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ])

    def test_combines_with_multiple_nodes(self):
        old = [
            TextNode("START *one*", TextType.TEXT),
            TextNode("MIDDLE", TextType.TEXT),
            TextNode("*two* END", TextType.TEXT)
        ]
        result = split_nodes_delimiter(old, "*", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("START ", TextType.TEXT),
            TextNode("one", TextType.BOLD),
            TextNode("", TextType.TEXT),
            TextNode("MIDDLE", TextType.TEXT),
            TextNode("", TextType.TEXT),
            TextNode("two", TextType.BOLD),
            TextNode(" END", TextType.TEXT),
        ])
    def test_extract_single_image(self):
        text = "Here is an image ![alt text](img.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "img.png")])

    def test_extract_multiple_images(self):
        text = "![a](1.png) and ![b](2.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [
            ("a", "1.png"),
            ("b", "2.jpg"),
        ])

    def test_extract_image_empty_alt(self):
        text = "![ ](x.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [(" ", "x.png")])

    def test_extract_images_no_match(self):
        text = "no images here"
        self.assertEqual(extract_markdown_images(text), [])

    # ---------- LINK TESTS ----------

    def test_extract_single_link(self):
        text = "Go to [Google](https://google.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("Google", "https://google.com")])

    def test_extract_multiple_links(self):
        text = "[A](a.com) and [B](b.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [
            ("A", "a.com"),
            ("B", "b.com")
        ])

    def test_extract_link_empty_text(self):
        text = "[](empty.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("", "empty.com")])

    def test_extract_links_no_match(self):
        text = "this has no links"
        self.assertEqual(extract_markdown_links(text), [])

    # ---------- MIXED CONTENT TESTS ----------

    def test_link_does_not_capture_images(self):
        text = "Image: ![pic](photo.jpg) and link: [site](url)"
        result_links = extract_markdown_links(text)
        result_imgs = extract_markdown_images(text)

        self.assertEqual(result_links, [("site", "url")])
        self.assertEqual(result_imgs, [("pic", "photo.jpg")])

    def test_image_does_not_capture_links(self):
        text = "Normal link [x](link.com)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_mixed_multiple(self):
        text = (
            "Image1 ![img1](1.jpg) link1 [a](a.com) "
            "Image2 ![img2](2.png) link2 [b](b.org)"
        )
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)

        self.assertEqual(images, [
            ("img1", "1.jpg"),
            ("img2", "2.png")
        ])

        self.assertEqual(links, [
            ("a", "a.com"),
            ("b", "b.org")
        ])
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
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_single_image_middle(self):
        nodes = [TextNode("Hello ![alt](img.png) world", TextType.TEXT)]
        result = split_nodes_image(nodes)

        self.assertEqual(result, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "img.png"),
            TextNode(" world", TextType.TEXT),
        ])

    def test_single_image_start(self):
        nodes = [TextNode("![pic](x.jpg) after", TextType.TEXT)]
        result = split_nodes_image(nodes)

        self.assertEqual(result, [
            TextNode("pic", TextType.IMAGE, "x.jpg"),
            TextNode(" after", TextType.TEXT),
        ])

    def test_single_image_end(self):
        nodes = [TextNode("before ![pic](x.jpg)", TextType.TEXT)]
        result = split_nodes_image(nodes)

        self.assertEqual(result, [
            TextNode("before ", TextType.TEXT),
            TextNode("pic", TextType.IMAGE, "x.jpg"),
        ])

    def test_multiple_images(self):
        nodes = [TextNode("A ![1](1.png) B ![2](2.jpg) C", TextType.TEXT)]
        result = split_nodes_image(nodes)

        self.assertEqual(result, [
            TextNode("A ", TextType.TEXT),
            TextNode("1", TextType.IMAGE, "1.png"),
            TextNode(" B ", TextType.TEXT),
            TextNode("2", TextType.IMAGE, "2.jpg"),
            TextNode(" C", TextType.TEXT),
        ])

    def test_no_images(self):
        nodes = [TextNode("nothing here", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(result, nodes)

    def test_non_text_node_passes_through(self):
        nodes = [
            TextNode("ignore me", TextType.BOLD),
            TextNode("![alt](x)", TextType.TEXT),
        ]
        result = split_nodes_image(nodes)

        self.assertEqual(result[0], TextNode("ignore me", TextType.BOLD))
        self.assertEqual(result[1:], [
            TextNode("alt", TextType.IMAGE, "x"),
        ])

    def test_single_link_middle(self):
        nodes = [TextNode("Go to [site](url) now", TextType.TEXT)]
        result = split_nodes_link(nodes)

        self.assertEqual(result, [
            TextNode("Go to ", TextType.TEXT),
            TextNode("site", TextType.LINK, "url"),
            TextNode(" now", TextType.TEXT),
        ])

    def test_single_link_start(self):
        nodes = [TextNode("[home](index.html) here", TextType.TEXT)]
        result = split_nodes_link(nodes)

        self.assertEqual(result, [
            TextNode("home", TextType.LINK, "index.html"),
            TextNode(" here", TextType.TEXT),
        ])

    def test_single_link_end(self):
        nodes = [TextNode("click [here](x)", TextType.TEXT)]
        result = split_nodes_link(nodes)

        self.assertEqual(result, [
            TextNode("click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "x"),
        ])

    def test_multiple_links(self):
        nodes = [TextNode("[A](a) and [B](b)", TextType.TEXT)]
        result = split_nodes_link(nodes)

        self.assertEqual(result, [
            TextNode("A", TextType.LINK, "a"),
            TextNode(" and ", TextType.TEXT),
            TextNode("B", TextType.LINK, "b"),
        ])

    def test_no_links(self):
        nodes = [TextNode("plain text", TextType.TEXT)]
        self.assertEqual(split_nodes_link(nodes), nodes)

    def test_non_text_node_passes_through(self):
        nodes = [
            TextNode("skip", TextType.ITALIC),
            TextNode("[x](y)", TextType.TEXT)
        ]
        result = split_nodes_link(nodes)

        self.assertEqual(result[0], TextNode("skip", TextType.ITALIC))
        self.assertEqual(result[1:], [
            TextNode("x", TextType.LINK, "y")
        ])
        def test_all_features(self):
            text = "Hello **bold** _italic_ `code` ![img](url) and [link](url2)"
            result = text_to_textnodes(text)

            expected = [
                TextNode("Hello ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url2"),
            ]
            self.assertEqual(result, expected)

class TestMarkdownToBlocks(unittest.TestCase):

    def test_simple_two_blocks(self):
        md = "This is block one.\n\nThis is block two."
        result = markdown_to_blocks(md)
        self.assertEqual(result, ["This is block one.", "This is block two."])

    def test_multiple_blank_lines(self):
        md = "Line 1\n\n\n\nLine 2"
        result = markdown_to_blocks(md)
        self.assertEqual(result, ["Line 1", "Line 2"])

    def test_blocks_with_whitespace(self):
        md = "  Block A   \n\n   Block B   "
        result = markdown_to_blocks(md)
        self.assertEqual(result, ["Block A", "Block B"])

    def test_single_block(self):
        md = "Only one block of text"
        result = markdown_to_blocks(md)
        self.assertEqual(result, ["Only one block of text"])

    def test_empty_string(self):
        md = ""
        result = markdown_to_blocks(md)
        self.assertEqual(result, [])

    def test_whitespace_only(self):
        md = "   \n   \n"
        result = markdown_to_blocks(md)
        self.assertEqual(result, [])

    def test_three_blocks(self):
        md = "A\n\nB\n\nC"
        result = markdown_to_blocks(md)
        self.assertEqual(result, ["A", "B", "C"])

    def test_block_with_internal_newlines(self):
        md = "Line1\nLine2\n\nNext block"
        result = markdown_to_blocks(md)
        self.assertEqual(result, ["Line1\nLine2", "Next block"])

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_single_paragraph(self):
        md = "Hello world"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>Hello world</p></div>"
        )

    def test_multiple_paragraphs(self):
        md = "First paragraph\n\nSecond paragraph"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>First paragraph</p><p>Second paragraph</p></div>"
        )

    def test_heading(self):
        md = "# Heading one"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading one</h1></div>"
        )

    def test_code_block(self):
        md = "```\nprint('hi')\n```"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>print('hi')</code></pre></div>"
        )

    def test_quote(self):
        md = "> quoted text"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>quoted text</blockquote></div>"
        )

    def test_unordered_list(self):
        md = "- item one\n- item two"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>item one</li><li>item two</li></ul></div>"
        )

    def test_ordered_list(self):
        md = "1. first\n2. second"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>first</li><li>second</li></ol></div>"
        )

    def test_mixed_blocks(self):
        md = "# Title\n\nParagraph text\n\n- a\n- b"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><p>Paragraph text</p><ul><li>a</li><li>b</li></ul></div>"
        )
if __name__ == "__main__":
    unittest.main()