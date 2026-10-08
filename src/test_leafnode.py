import unittest
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_to_html_with_tag(self):
        node = LeafNode("p", "Hello")
        self.assertEqual(node.to_html(), "<p>Hello</p>")

    def test_to_html_with_props(self):
        node = LeafNode(
            "a",
            "Click me",
            {"href": "https://example.com"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com">Click me</a>'
        )

    def test_to_html_without_tag(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), "Hello")

    def test_to_html_without_value(self):
        node = LeafNode("p", None)

        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
