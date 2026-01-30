import os
import shutil
import logging
from datetime import datetime
from constants import LOGPATH
from functions import markdown_to_html_node
from pathlib import Path
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
    content = read_file(markdown)
    lines = content.splitlines()
    heading = ""
    for line in lines:
        if line.startswith("# "):
            heading = line
            break
    if heading == "":
        raise ValueError("There is no H1 heading")
    heading = heading[1:].strip()
    return heading

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file_str = read_file(from_path)
    template_file_str = read_file(template_path)
    html_content = markdown_to_html_node(from_file_str)
    title = extract_title(from_path)
    template_file_str = template_file_str.replace("{{ Title }}", title)
    template_file_str = template_file_str.replace("{{ Content }}", html_content.to_html())
    template_file_str = template_file_str.replace(f'href="/', f'href="{basepath}')
    template_file_str = template_file_str.replace(f'src="/', f'src="{basepath}')
    dir_path = os.path.dirname(dest_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    try:
        # 'with' automatically handles opening and closing the file
        with open(dest_path, 'w') as file:
            file.write(template_file_str)

    except FileNotFoundError:
        # Handles cases where the directory might not exist (Python 3.4+)
        print(f"Error: The directory for '{filename}' was not found.")
    except PermissionError:
        # Handles cases with insufficient permissions to write to the file/location
        print(f"Error: Permission denied when trying to write to '{filename}'.")
    except IOError as e:
        # General I/O error handling (e.g., disk full, other OS errors)
        print(f"Error: An I/O error occurred: {e}")
    except Exception as e:
        # Catches any other unexpected exceptions
        print(f"An unexpected error occurred: {e}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    base_path = Path(dir_path_content)
    md_files = list(base_path.rglob('*.md'))
    md_file_strings = [str(p) for p in md_files]
    for file in md_file_strings:
        p = Path(file)
        relative = p.relative_to(dir_path_content)
        dest = Path(dest_dir_path) / relative
        dest = dest.with_suffix(".html")
        generate_page(file, template_path, str(dest), basepath)

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return content