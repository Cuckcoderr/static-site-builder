import unittest
from htmlnode import *

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_node_with_one_child(self):
            node = ParentNode("p",[LeafNode(None, "Hello world")])
            self.assertEqual(
                node.to_html(),
                "<p>Hello world</p>"
            )

    def test_parent_node_with_multiple_children(self):
        node = ParentNode("div",[LeafNode("b", "Hello"),LeafNode(None, " world")])

        self.assertEqual(
            node.to_html(),
            "<div><b>Hello</b> world</div>"
        )

    def test_parent_node_with_nested_parent(self):
        node = ParentNode("div",[ParentNode("p",[LeafNode(None, "Hello")])])

        self.assertEqual(
            node.to_html(),
            "<div><p>Hello</p></div>"
        )

    def test_parent_node_with_multiple_nested_children(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [LeafNode(None, "First")]
                ),
                ParentNode(
                    "p",
                    [LeafNode(None, "Second")]
                ),
            ]
        )

        self.assertEqual(
            node.to_html(),
            "<div><p>First</p><p>Second</p></div>"
        )

    def test_parent_node_without_tag(self):
        node = ParentNode(
            None,
            [LeafNode(None, "Hello")]
        )

        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_without_children(self):
        node = ParentNode(
            "div",
            None
        )

        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "Hello")],
            {"class": "container", "id": "main"}
        )

        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main">Hello</div>'
        )

    def test_parent_node_with_nested_parent_and_leaf_props(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode(
                            "a",
                            "Click here",
                            {"href": "https://example.com", "target": "_blank"}
                        )
                    ]
                )
            ]
        )

        self.assertEqual(
            node.to_html(),
            '<div><p><a href="https://example.com" target="_blank">Click here</a></p></div>'
        )


if __name__ == "__main__":
    unittest.main()
