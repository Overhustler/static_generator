from textnode import *
import constants
from mainfuctions import copy_directory, delete_and_remake_dir, generate_page, generate_pages_recursive

def main():
    delete_and_remake_dir(constants.PUBLICPATH)
    copy_directory(constants.STATICPATH, constants.PUBLICPATH)
    generate_pages_recursive("content/", "template.html", "public/")
if __name__ == "__main__":
    main()