import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_initializes_with_defaults(self):
        node = HTMLNode()

        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_initializes_with_values(self):
        children = [HTMLNode(tag="p", value="Hello")]
        props = {"class": "container", "id": "main"}

        node = HTMLNode(
            tag="div",
            value="Hello",
            children=children,
            props=props,
        )

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_props_to_html_with_no_props(self):
        node = HTMLNode(tag="div")

        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_one_prop(self):
        node = HTMLNode(
            tag="div",
            props={"class": "container"},
        )

        self.assertEqual(
            node.props_to_html(),
            ' class="container"'
        )

    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(
            tag="div",
            props={
                "class": "container",
                "id": "main",
            },
        )

        self.assertEqual(
            node.props_to_html(),
            ' class="container" id="main"'
        )

    def test_repr(self):
        node = HTMLNode(
            tag="div",
            value="Hello",
            props={"class": "container"},
        )

        expected = (
            "tag: div\n"
            "value: Hello\n"
            "children: None\n"
            "props: {'class': 'container'}"
        )

        self.assertEqual(repr(node), expected)

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="div", value="Hello")

        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
