import os

from block_markdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.split(" ",1)[1]
    raise Exception("no title found!")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Create directory for dest_path if the files do not exist
    dir_name = os.path.dirname(dest_path)
    os.makedirs(dir_name, exist_ok=True)

    with open(from_path,'r') as markdown, open(template_path, 'r') as template, open(dest_path,'w') as html_result:
        markdown_text = markdown.read()
        markdown_html = markdown_to_html_node(markdown_text).to_html()
        page_title = extract_title(markdown_text)
        output_html = template.read().replace("{{ Title }}", page_title).replace("{{ Content }}", markdown_html)
        html_result.write(output_html)
