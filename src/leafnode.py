from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        children = None
        super().__init__(tag, value, children, props)

    def to_html(self):
        if not self.value:
            raise ValueError()
        elif not self.tag:
            return self.value
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"