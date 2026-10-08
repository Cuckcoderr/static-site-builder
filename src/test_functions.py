import unittest
from textnode import *
from htmlnode import *
from functions import *

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_bold(self):
        old_nodes = [
            TextNode("This is **bold** text", TextType.TEXT)
        ]

        new_nodes = split_nodes_delimiter(
            old_nodes,
            "**",
            TextType.BOLD
        )

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_italic(self):
        old_nodes = [
            TextNode("This is *italic* text", TextType.TEXT)
        ]

        new_nodes = split_nodes_delimiter(
            old_nodes,
            "*",
            TextType.ITALIC
        )

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_code(self):
        old_nodes = [
            TextNode("Run `print()` here", TextType.TEXT)
        ]

        new_nodes = split_nodes_delimiter(
            old_nodes,
            "`",
            TextType.CODE
        )

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "Run ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "print()")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

        self.assertEqual(new_nodes[2].text, " here")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_multiple_formatted_sections(self):
        old_nodes = [
            TextNode(
                "This is **bold** and **more bold**",
                TextType.TEXT
            )
        ]

        new_nodes = split_nodes_delimiter(
            old_nodes,
            "**",
            TextType.BOLD
        )

        self.assertEqual(len(new_nodes), 4)

        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[3].text, "more bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)

    def test_text_without_delimiter(self):
        old_nodes = [
            TextNode("This is normal text", TextType.TEXT)
        ]

        new_nodes = split_nodes_delimiter(
            old_nodes,
            "**",
            TextType.BOLD
        )

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is normal text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_empty_text_between_delimiters(self):
        old_nodes = [
            TextNode("Hello **** world", TextType.TEXT)
        ]

        new_nodes = split_nodes_delimiter(
            old_nodes,
            "**",
            TextType.BOLD
        )

        self.assertEqual(len(new_nodes), 2)

        self.assertEqual(new_nodes[0].text, "Hello ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, " world")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

    def test_non_text_node_is_not_split(self):
        old_nodes = [
            TextNode("already bold", TextType.BOLD)
        ]

        new_nodes = split_nodes_delimiter(
            old_nodes,
            "**",
            TextType.BOLD
        )

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "already bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_mixed_text_nodes(self):
        old_nodes = [
            TextNode("This is **bold**", TextType.TEXT),
            TextNode("already italic", TextType.ITALIC),
            TextNode(" and `code`", TextType.TEXT)
        ]

        new_nodes = split_nodes_delimiter(
            old_nodes,
            "**",
            TextType.BOLD
        )

        self.assertEqual(len(new_nodes), 4)

        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

        self.assertEqual(new_nodes[2].text, "already italic")
        self.assertEqual(new_nodes[2].text_type, TextType.ITALIC)

        self.assertEqual(new_nodes[3].text, " and `code`")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)

    def test_missing_closing_delimiter(self):
        old_nodes = [
            TextNode("This is **bold", TextType.TEXT)
        ]

        with self.assertRaises(Exception):
            split_nodes_delimiter(
                old_nodes,
                "**",
                TextType.BOLD
            )


class TestMarkdownExtraction(unittest.TestCase):

    # ---------- Images ----------

    def test_extract_one_image(self):
        text = "sdgsd![rick roll](https://i.imgur.com/aKaOqIh.gif) dsgg"

        result = extract_markdown_images(text)

        self.assertEqual(
            result,
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        )

    def test_extract_multiple_images(self):
        text = (
            "fngfng ![cat](cat.png) "
            "some text "
            "![dog](dog.png)"
        )

        result = extract_markdown_images(text)

        self.assertEqual(
            result,
            [
                ("cat", "cat.png"),
                ("dog", "dog.png")
            ]
        )

    def test_extract_image_with_empty_alt_text(self):
        text = "![](image.png)"

        result = extract_markdown_images(text)

        self.assertEqual(result, [("", "image.png")])

    def test_no_images(self):
        text = "This is just some text."

        result = extract_markdown_images(text)

        self.assertEqual(result, [])

    def test_links_are_not_images(self):
        text = "[Google](https://google.com)"

        result = extract_markdown_images(text)

        self.assertEqual(result, [])


    # ---------- Links ----------

    def test_extract_one_link(self):
        text = "[Google](https://google.com)hnn "

        result = extract_markdown_links(text)

        self.assertEqual(
            result,
            [("Google", "https://google.com")]
        )

    def test_extract_multiple_links(self):
        text = (
            "[Google](https://google.com) "
            "some text "
            "[OpenAI](https://openai.com)"
        )

        result = extract_markdown_links(text)

        self.assertEqual(
            result,
            [
                ("Google", "https://google.com"),
                ("OpenAI", "https://openai.com")
            ]
        )

    def test_extract_link_with_empty_text(self):
        text = "[](https://google.com)"

        result = extract_markdown_links(text)

        self.assertEqual(
            result,
            [("", "https://google.com")]
        )

    def test_no_links(self):
        text = "This is just some text."

        result = extract_markdown_links(text)

        self.assertEqual(result, [])

    def test_images_are_not_links(self):
        text = "![Google logo](logo.png)"

        result = extract_markdown_links(text)

        self.assertEqual(result, [])

    def test_mixed_links_and_images(self):
        text = (
            "[Google](https://google.com) "
            "![Google logo](logo.png) "
            "[OpenAI](https://openai.com)"
        )

        links = extract_markdown_links(text)
        images = extract_markdown_images(text)

        self.assertEqual(
            links,
            [
                ("Google", "https://google.com"),
                ("OpenAI", "https://openai.com")
            ]
        )

        self.assertEqual(
            images,
            [
                ("Google logo", "logo.png")
            ]
        )

class TestTextNodeCreation(unittest.TestCase):
    def test_list_of_nodes_from_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        result = text_to_textnodes(text)

        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

class TestMarkdownBlocktoblock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

  This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == "__main__":
    unittest.main()
