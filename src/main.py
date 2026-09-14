from textnode import *
from split_delimiter import *
from copystatic import *
from gen_content import *
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    rm_public("docs")
    copy("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    

main()