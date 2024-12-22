from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if not self.value:
            if self.tag != "img":
                raise ValueError("All leaf nodes must have a value")
            else:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        elif not self.tag:
            return self.value
        else:
            #render an HTML tag
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    