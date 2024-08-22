import os
import subprocess
import threading
import shutil

css_style = """
<style>
    /* slides */
    .reveal .slides {
        padding: 0 !important;
        margin: auto !important;
        width: 100% !important;
        height: 100% !important;
    }
    .reveal .slides .present.stack {
        overflow-y: scroll !important;
        overflow-x : hidden !important;
    }
    .reveal .slides .jp-Cell {
        margin-right: 15px !important;
        margin-left :3% !important;
    }
    .reveal .slides .jp-CodeCell .jp-CodeMirrorEditor  {
        overflow-x : scroll !important;
        padding-right:30px !important;
    }
    .reveal .slides .jp-CodeCell .jp-InputPrompt  {
        width: 90px !important;
    }
    .reveal .slides .jp-CodeCell .jp-CodeMirrorEditor pre {
        box-shadow: 0px 0px 0px rgba(0,0,0,0) !important;
    }

    .reveal .slides .jp-MarkdownCell .jp-InputPrompt {
        width: 0px !important;
        padding: 0 !important;
    }
    .reveal .slides .jp-MarkdownCell .jp-RenderedMarkdown {
        margin: 0 0 0 30px !important;
    }
    .reveal .slides .jp-MarkdownCell h1 {
        margin-left: 7% !important;
        font-weight: bold !important;
    }
    .reveal .slides .jp-MarkdownCell h2 {
        font-weight: bold !important;
    }
    .reveal .slides .jp-MarkdownCell h3 {
        font-weight: bold !important;
    }
    .reveal .slides .jp-MarkdownCell h4 {
        font-weight: bold !important;
    }
</style>
"""

def add_custom_css_to_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()

    content = content.replace('</head>', f'{css_style}</head>')

    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(content)

def convert_notebook_to_slide(input_path, output_path):
    subprocess.run([
        'jupyter', 'nbconvert', input_path, 
        '--to', 'slides', 
        '--output-dir', output_path
    ])

    slide_file = os.path.join(output_path, os.path.basename(input_path).replace('.ipynb', '.slides.html'))
    if os.path.exists(slide_file):
        add_custom_css_to_html(slide_file)

def convert_notebooks_to_slides(directory, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    threads = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb'):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, directory)
                output_path = os.path.join(output_dir, relative_path)
                
                if not os.path.exists(output_path):
                    os.makedirs(output_path)

                thread = threading.Thread(target=convert_notebook_to_slide, args=(input_path, output_path))
                thread.start()
                threads.append(thread)
    
    # 모든 스레드가 완료될 때까지 대기
    for thread in threads:
        thread.join()

# 슬라이드로 변환할 노트북 파일이 있는 디렉토리 경로를 설정하세요.
notebook_dir = './book/contents'
output_dir = './slides'

convert_notebooks_to_slides(notebook_dir, output_dir)
print('All notebooks have been recursively converted to slides with custom styles.')
