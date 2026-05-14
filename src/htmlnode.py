class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
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
        for k, v in self.props.items():
            result.append(f'{k}="{v}"')
        return " " + " ".join(result) if result else ""

    def __repr__(self):
        return f"{self.tag}\n{self.value}\n{self.children}\n{self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            return self.value

        if self.tag in {"img", "br", "hr", "input", "meta", "link"}:
            return f"<{self.tag}{self.props_to_html()} />"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"{self.tag}\n{self.value}\n{self.props}"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("all parent nodes must have a tag")
        if self.children is None:
            raise ValueError("children are missing")
        value = ""
        for child in self.children:
            value += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{value}</{self.tag}>"
