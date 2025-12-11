from enum import Enum
import re
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    if re.match(r"#{1,6}\s\S", block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif(check_if_ordered_list(block)):
        return BlockType.ORDERED_LIST
    elif re.fullmatch(r"(>.*\n?)+", block):
        return BlockType.QUOTE
    elif re.fullmatch(r"(-\s.*\n?)+", block):
        return BlockType.UNORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def check_if_ordered_list(block_str):
    i = 1
    for line in block_str.split(f"\n"):
        if not line.startswith(f"{i}. "):
            return False
        i += 1
    return True