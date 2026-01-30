from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        children = None
        super().__init__(tag, value, children, props)

    def to_html(self):
        # 1. text node
        if self.tag is None:
            if self.value is None:
                raise ValueError()
            return self.value

        # 2. build props string from self.props (if any)
        props_string = ""
        if self.props is not None:
            for key, value in self.props.items():
                props_string += f' {key}="{value}"'
        # 3. img node – no inner value
        if self.tag == "img":
            return f"<img{props_string}>"

        # 4. normal element: require non-None value
        if self.value is None:
            raise ValueError()
        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"