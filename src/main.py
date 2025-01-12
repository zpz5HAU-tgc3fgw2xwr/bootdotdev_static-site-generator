import os
import shutil
from textnode import TextNode, TextType
from markdown_utils import markdown_to_html_node

def copy_directory(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

def extract_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    raise Exception("No H1 title found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    
    full_html = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + '.html')
                generate_page(from_path, template_path, dest_path)

def main():
    # Delete anything in the 'public' directory
    copy_directory('static', 'public')
    
    # Generate pages for every markdown file in the 'content' directory
    generate_pages_recursive('content', 'template.html', 'public')
    
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()