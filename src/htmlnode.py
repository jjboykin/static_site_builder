class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        string_result = ""
        if self.props:
            result = [f"{key}='{value}'" for key, value in self.props.items()]
            string_result = " " + " ".join(result)
        return string_result
    
    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        return False
    
    def __repr__(self):
        obj_out = "{ \n"
        obj_out += f"'tag': {self.tag}\n"
        obj_out += f"'value': {self.value}\n"
        obj_out += f"'children': {self.children}\n"
        obj_out += f"'props': {self.props}\n"
        obj_out += "}}"
        return obj_out