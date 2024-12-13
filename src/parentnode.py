from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        elif not self.children:
            raise ValueError("All parent nodes must have a child")
        else:
            #render an HTML tag and its children
            children_html =""
            for child in self.children:
                children_html += child.to_html() 
            '''This should be a recursive method (each recursion being called on a nested child node). 
            I iterated over all the children and called to_html on each, concatenating the results and 
            injecting them between the opening and closing tags of the parent.
            '''
            return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"