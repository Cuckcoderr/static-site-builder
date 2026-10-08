
class HTMLNode():

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list['HTMLNode'] | None = None,
        props: dict[str, str] | None = None
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):

        raise NotImplementedError("not yet coded")

    def props_to_html(self)-> str:
        if self.props is None:
            return ""
        else:
            html = ""
            for i in self.props:
                html += f' {i}="{self.props[i]}"'
            return html

    def __repr__(self)-> str:
        return f'tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}'

class LeafNode(HTMLNode):

    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None
    ):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value == None:
            raise  ValueError("all leaf nodes must have some value")
        else:
            if self.tag == None:
                return f'{self.value}'
            else:
                return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list['HTMLNode'],
        props: dict[str, str] | None = None
    ):
        super().__init__(tag=tag,value=None, children=children, props=props)

    def to_html(self) -> str:
        if self.tag == None:
            raise  ValueError("all parent nodes must have some tag")

        if self.children == None:
            raise  ValueError("all parent nodes must have child nodes")

        inside_node: str = f'<{self.tag}{self.props_to_html()}>{"".join(x.to_html() for x in self.children)}</{self.tag}>'
        return inside_node
