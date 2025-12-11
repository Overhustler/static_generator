import unittest
from blocktypes import block_to_block_type, check_if_ordered_list, BlockType


class TestBlockToBlockType(unittest.TestCase):

    # ---------- HEADING TESTS ----------
    def test_heading_level_1(self):
        block = "# Heading text"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_level_6(self):
        block = "###### Six levels deep"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_invalid(self):
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    # ---------- CODE BLOCK TESTS ----------
    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_single_line(self):
        block = "```print('hi')```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_missing_end(self):
        block = "```\nprint('hello')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    # ---------- ORDERED LIST TESTS ----------
    def test_ordered_list_valid(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_single(self):
        block = "1. only one"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_number(self):
        block = "1. first\n3. wrong numbering"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_bad_format(self):
        block = "1. first\n2 second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    # ---------- UNORDERED LIST TESTS ----------
    def test_unordered_list_single(self):
        block = "- item one"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid(self):
        block = "-item missing space"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    # ---------- QUOTE TESTS ----------
    def test_quote_single_line(self):
        block = "> a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multiple_lines(self):
        block = "> line one\n> line two"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_invalid_missing_second_arrow(self):
        block = "> line one\nline two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    # ---------- PARAGRAPH TESTS ----------
    def test_paragraph_simple(self):
        block = "This is normal text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_with_markdown_inside(self):
        block = "Text with **bold** but still a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_string(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        

class TestCheckIfOrderedList(unittest.TestCase):

    def test_valid_ordered_list(self):
        block = "1. one\n2. two\n3. three"
        self.assertTrue(check_if_ordered_list(block))

    def test_single_item(self):
        block = "1. only one"
        self.assertTrue(check_if_ordered_list(block))

    def test_wrong_numbering(self):
        block = "1. first\n3. second"
        self.assertFalse(check_if_ordered_list(block))

    def test_bad_format_no_space(self):
        block = "1.one\n2.two"
        self.assertFalse(check_if_ordered_list(block))

    def test_empty(self):
        self.assertFalse(check_if_ordered_list(""))

    def test_mixed_content(self):
        block = "1. item\ntext"
        self.assertFalse(check_if_ordered_list(block))