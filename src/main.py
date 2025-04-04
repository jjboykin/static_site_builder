import shutil
import os
import sys

from copystatic import *
from gencontent import *

from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    if len(sys.argv) != 2 :
        base_path = "/"
    else:
        base_path = sys.argv[1]
    if base_path == "":
        base_path = "/"
    print(f"Base path: {base_path}")
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating content...")
    generate_pages_recursive(base_path, dir_path_content, template_path, dir_path_public)
    
main()