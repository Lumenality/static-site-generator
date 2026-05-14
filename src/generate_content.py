import os

from block_markdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.split(" ",1)[1]
    raise Exception("no title found!")

def generate_page(from_path, template_path, dest_path, basepath = "/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Create directory for dest_path if the files do not exist
    dir_name = os.path.dirname(dest_path)
    os.makedirs(dir_name, exist_ok=True)

    with open(from_path,'r') as markdown, open(template_path, 'r') as template, open(dest_path,'w') as html_result:
        markdown_text = markdown.read()
        markdown_html = markdown_to_html_node(markdown_text).to_html()
        page_title = extract_title(markdown_text)
        output_html = template.read().replace("{{ Title }}", page_title).replace("{{ Content }}", markdown_html)
        output_html = output_html.replace('href="/',f'href="{basepath}').replace('src="/',f'src="{basepath}')
        html_result.write(output_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath = "/"):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            filepath = os.path.join(root, file)
            relative_path = os.path.relpath(filepath, dir_path_content)
            if file.endswith((".md")):
                html_relative_path = relative_path.replace(".md", ".html")
                dest_path = os.path.join(dest_dir_path,html_relative_path)
                
                generate_page(filepath,template_path,dest_path,basepath)

if __name__ == "__main__":
    # DEPRECATED DEBUG generate_pages_recursive("content/",None,None)
    print("Running generate_content for debugging")