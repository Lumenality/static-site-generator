
import os
import sys
from shutil import copy, rmtree

from generate_content import generate_pages_recursive

STATIC_DIR = 'static'
CONTENT_PATH = "content"
TEMPLATE_PATH = "template.html"
DEST_PATH = "docs"

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"

def main():
    # Check if the static directory exists
    if not os.path.exists(STATIC_DIR):
        print(f"The '{STATIC_DIR}' directory does not exist.")
        return

    # Check if the static directory is empty
    if not os.listdir(STATIC_DIR):
        print(f"The '{STATIC_DIR}' directory is empty. Nothing to deploy.")
        return

    print(f"The '{STATIC_DIR}' directory is ready for deployment.")
    print(f"Copying files from '{STATIC_DIR}' to '{DEST_PATH}'...\n")
    copy_all(STATIC_DIR, DEST_PATH)
    
    # Run a printout for all files in the public directory
    print(f"Files now in '{DEST_PATH}' directory:")
    for root, dirs, files in os.walk(DEST_PATH):
        for file in files:
            print(os.path.join(root, file))
    
    # Generate a site from two files (markdown and template)
    generate_pages_recursive(CONTENT_PATH, TEMPLATE_PATH, DEST_PATH, basepath)

def copy_all(source_dir, dest_dir):
    # Remove the destination directory if it exists
    if os.path.exists(dest_dir):
        rmtree(dest_dir)
    # Create the destination directory
    os.makedirs(dest_dir)
    # Copy all files and directories from the source to the destination
    for item in os.listdir(source_dir):
        src_path = os.path.join(source_dir, item)
        dst_path = os.path.join(dest_dir, item)
        if os.path.isdir(src_path):
            copy_all(src_path, dst_path)
        else:
            copy(src_path, dst_path)
    print(f"All files copied from '{source_dir}' to '{dest_dir}' successfully.\n")

if __name__ == "__main__":
    main()