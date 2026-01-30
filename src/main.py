from textnode import *
import constants
from mainfuctions import copy_directory, delete_and_remake_dir, generate_page, generate_pages_recursive
import sys
def main():
    sys_arg_lenth = len(sys.argv)
    basepath = ""
    if sys_arg_lenth < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    delete_and_remake_dir(constants.PUBLICPATH)
    copy_directory(constants.STATICPATH, constants.PUBLICPATH)
    generate_pages_recursive("content/", "template.html", constants.PUBLICPATH, basepath)
if __name__ == "__main__":
    main()