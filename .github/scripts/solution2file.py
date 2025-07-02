import json
import os; os.system('clear')
import re
from pathlib import Path

def embed_images_in_notebook(notebook_path):
    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Regular expression to find "# <CODE>" comment in cell
    code_regex = re.compile(r'# <CODE>')

    if notebook_path.endswith('_solution.ipynb'):
        print("This is a solution notebook")
    else:
        print("This is not a solution notebook")
        return
    
    # Iterate over all cells
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':
            new_source = []
            print("-"*50)
            for line in cell.get('source', []):
                print(line)
                # Find all images in the line
                matches = code_regex.findall(line)
                if matches:
                    print(matches)
                    print(line)
                    new_source.append(line)
                    break

                new_source.append(line)
            cell['source'] = new_source




    notebook_path = notebook_path.replace('_solution.ipynb', '.ipynb')
    
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)
    

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Embed images as base64 in a Jupyter Notebook.')
    parser.add_argument('notebook', help='Path to the .ipynb file')
    args = parser.parse_args()

    embed_images_in_notebook(args.notebook)