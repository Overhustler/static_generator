from textnode import *
import constants
from mainfuctions import copy_directory, delete_and_remake_dir

def main():
    delete_and_remake_dir(constants.PUBLICPATH)
    copy_directory(constants.STATICPATH, constants.PUBLICPATH)
    
if __name__ == "__main__":
    main()