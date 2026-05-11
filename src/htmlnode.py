class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        result = []
        for k,v in self.props.items():
            result.append(f"{k}={v}")
        return " ".join(result)
    
    def __repr__(self):
        return f"{self.tag}\n{self.value}\n{self.children}\n{self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag is None:
            return self.value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag} {self.props}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"{self.tag}\n{self.value}\n{self.props}"