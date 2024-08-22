import os
import json
import base64
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def convert_attachment_to_data_uri(cell):
    if 'attachments' in cell:
        for attachment_name, attachment_data in cell['attachments'].items():
            for mime_type, base64_data in attachment_data.items():
                data_uri = f"data:{mime_type};base64,{base64_data}"
                if isinstance(cell['source'], list):
                    cell['source'] = [line.replace(f"attachment:{attachment_name}", data_uri) for line in cell['source']]
                else:
                    cell['source'] = cell['source'].replace(f"attachment:{attachment_name}", data_uri)
        del cell['attachments']
    return cell

def process_ipynb_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        notebook = json.load(file)
    
    for cell in notebook.get('cells', []):
        if cell['cell_type'] == 'markdown':
            cell = convert_attachment_to_data_uri(cell)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(notebook, file, ensure_ascii=False, indent=2)
    print(f"Processed {file_path}")

def process_notebook_files(directory):
    with ThreadPoolExecutor() as executor:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.ipynb'):
                    file_path = os.path.join(root, file)
                    executor.submit(process_ipynb_file, file_path)

# Use the function to process the 'book/' directory
process_notebook_files('book/')
