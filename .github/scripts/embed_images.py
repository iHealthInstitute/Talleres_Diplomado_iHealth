import json
import base64
import os
import re
from pathlib import Path

def embed_images_in_notebook(notebook_path):
    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Regular expression to find markdown image links: ![alt](path)
    img_regex = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    
    # Iterate over all cells
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'markdown':
            new_source = []
            for line in cell.get('source', []):
                # Find all images in the line
                matches = img_regex.findall(line)
                if matches:
                    for alt_text, img_path in matches:
                        # Resolve the image path relative to the notebook
                        img_full_path = os.path.join(img_path)
                        img_full_path = os.path.abspath(img_full_path)
                        
                        if os.path.isfile(img_full_path):
                            # Get the file extension to determine the MIME type
                            ext = Path(img_full_path).suffix.lower()
                            if ext == '.png':
                                mime = 'image/png'
                            elif ext in ['.jpg', '.jpeg']:
                                mime = 'image/jpeg'
                            elif ext == '.gif':
                                mime = 'image/gif'
                            elif ext == '.svg':
                                mime = 'image/svg+xml'
                            else:
                                print(f"Unsupported image format: {ext} for file {img_full_path}")
                                continue
                            
                            # Read and encode the image
                            with open(img_full_path, 'rb') as img_file:
                                encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
                            
                            # Create the HTML snippet
                            html_img = f'<div style="text-align:center;"><img src="data:{mime};base64,{encoded_string}" alt="{alt_text}"></div>'
                            
                            # Replace the markdown image with the HTML
                            markdown_img = f'![{alt_text}]({img_path})'
                            line = line.replace(markdown_img, html_img)
                        else:
                            print(f"Image file not found: {img_full_path}")
                new_source.append(line)
            cell['source'] = new_source

        # I want to remove the "#### **Ejercicio" from the notebook
    ejercicio_regex = re.compile(r'#### \*\*Ejercicio')
    # Count Ejercicio
    ejercicio_num = 1
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'markdown':
            new_source = []
            for line in cell.get('source', []):
                matches = ejercicio_regex.findall(line)
                if matches:
                    print(line)
                    new_source.append(f"#### **Ejercicio {ejercicio_num}** \n")
                    ejercicio_num += 1
                else:
                    new_source.append(line)
            cell['source'] = new_source
    
    # Save the modified notebook
    backup_path = notebook_path + '.bak'
    os.rename(notebook_path, backup_path)
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)
    
    print(f"Processed notebook saved as {notebook_path}")
    print(f"Original notebook backed up as {backup_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Embed images as base64 in a Jupyter Notebook.')
    parser.add_argument('notebook', help='Path to the .ipynb file')
    args = parser.parse_args()

    embed_images_in_notebook(args.notebook)