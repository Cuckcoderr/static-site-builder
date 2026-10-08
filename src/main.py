from functions import *
import sys


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static_to_public("./static", "./docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


main()
