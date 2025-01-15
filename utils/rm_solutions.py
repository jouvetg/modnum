import nbformat
from nbconvert import NotebookExporter
import glob,os


def remove_solution_cells(notebook_path, output_path):
    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Remove cells tagged as 'solution'
    nb['cells'] = [cell for cell in nb['cells'] if 'solution' not in cell.get('metadata', {}).get('tags', [])]

    # Save the notebook without solution cells
    exporter = NotebookExporter()
    body, _ = exporter.from_notebook_node(nb)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(body)
        
f = glob.glob("??_exercice_solution.ipynb")[0]

print(f)

h = f.split('_solution')[0]  +'.ipynb'

if os.path.exists(h):
     os.remove(h)

remove_solution_cells(f,h)
