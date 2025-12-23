import os
import shutil
import logging
from datetime import datetime
from constants import LOGPATH

def copy_directory(source_dir, destination_dir):

    with os.scandir(source_dir) as entries:

        for entry in entries:

            if entry.is_file():
                try:
                    shutil.copyfile(entry.path, f"{destination_dir}/{entry.name}")
                except FileNotFoundError:
                    print(f"Error: Source file '{entry.path}' not found.")
                except PermissionError:
                    print(f"Error: Permission denied for destination directory '{destination_dir}'.")
                except Exception as e:
                    print(f"An error occurred: {e}")

            if entry.is_dir():
                new_dir_path = f"{destination_dir}/{entry.name}"
                try:
                    os.mkdir(new_dir_path)
                except FileExistsError:
                    print(f"Directory '{entry.path}' already exists")
                except OSError as e:
                    print(f"OS error: {e}")
                copy_directory(entry.path, new_dir_path)


def delete_and_remake_dir(directory_path):

    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print(f"Deleted existing directory: {directory_path}")

    else:
        print(f"Directory not found, proceeding to create: {directory_path}")

    os.makedirs(directory_path)
    
def extract_title(markdown):
    pass