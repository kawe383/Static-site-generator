from textnode import *
from split_delimiter import *
from copystatic import *
from gen_content import *

def main():
    rm_public("public")
    copy("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    
main()