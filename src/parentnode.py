from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        value=None
        super().__init__(tag, value, children, props)

    def to_html(self):
        
        if not self.tag:
            raise ValueError("Error: there is no tag")
        if not self.children:
            raise ValueError("Error:there are no children")
        html_string = ""
        for i in self.children:
            html_string += f"{i.to_html()}"
        return f"<{self.tag}>{html_string}</{self.tag}>"