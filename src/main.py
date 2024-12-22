import shutil
import os

from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *
from lib_func import *

def main():
    #text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    #print(text_to_textnodes(text))

    copy_static("static/", "public/")
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content/", "template.html", "public/")
    
def copy_static(src, dst):

    # delete all the contents of the destination directory
    if os.path.exists(dst):
        print(f"Deleting directory {dst}")
        shutil.rmtree(dst)

    # copy all files and subdirectories, nested files, etc, logging the path of each file you copy
    if os.path.exists(src):
        dir_list = os.listdir(src)
        print(f"Creating directory {dst}")
        os.mkdir(dst)
        for item in dir_list:
            if os.path.isfile(os.path.join(src,item)):
                print(f"Copying file {item} from {os.path.join(src,item)} to {os.path.join(dst,item)}")
                shutil.copy(os.path.join(src,item), os.path.join(dst,item))
            else:
                copy_static(os.path.join(src,item), os.path.join(dst,item))

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Read the markdown file at from_path and store the contents in a variable.
    if os.path.isfile(from_path):
        with open(from_path) as f:
            md_file = f.read()

    else:
        raise Exception("Invalid path to markdown file")

    # Read the template file at template_path and store the contents in a variable.
    if os.path.isfile(template_path):
        with open(template_path) as f:
            template_file = f.read()
    else:
        raise Exception("Invalid path to template file")

    # Use your markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string.
    html_string = markdown_to_html_node(md_file).to_html()

    # Use the extract_title function to grab the title of the page.
    title = extract_title(md_file)

    # Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
    generated_html = (template_file.replace("{{ Title }}", title)).replace("{{ Content }}", html_string)

    # Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.
    print(f"Generating new HTML file at {dest_path}")
    if not os.path.exists(os.path.dirname(dest_path)):
        os.mkdir(os.path.dirname(dest_path))

    with open(dest_path, mode='w') as f:
        f.write(generated_html) 
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Crawl every entry in the content directory
    if os.path.exists(dir_path_content):
        dir_list = os.listdir(dir_path_content)
        
        for item in dir_list:
            # For each markdown file found...
            if os.path.isfile(os.path.join(dir_path_content,item)):
                if ".md" in item: 
                    # ...generate a new .html file using the template.html.
                    generate_page(os.path.join(dir_path_content,item), template_path, os.path.join(dest_dir_path,"index.html"))
            else:
                generate_pages_recursive(os.path.join(dir_path_content,item), template_path, os.path.join(dest_dir_path,item))
            
                

main()