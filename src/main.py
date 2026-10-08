from functions import *



def main():
    copy_static_to_public("./static", "./public")
    generate_pages_recursive("content", "template.html", "public")


main()
