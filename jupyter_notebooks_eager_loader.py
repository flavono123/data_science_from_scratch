""" run a following cell first
%%javascript
var kernel = IPython.notebook.kernel;
var body = document.body,  
    attribs = body.attributes;
var command = "theNotebook = " + "'"+attribs['data-notebook-name'].value+"'";
kernel.execute(command);
"""
### JUPYTER NOTEBOOK EAGER LOAD ###
import io, os, sys, types
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell

files = !ls *.ipynb
files = sorted(files, key=lambda f: int(f.split('.')[0]))
files = filter(lambda file: file != theNotebook, files)

nbs = []
for file in files:
    with io.open(file, 'r', encoding='utf-8') as f:
        nbs.append(read(f, 4))
        
each_code_cells = []
for nb in nbs:
    each_code_cells.append(filter(lambda c: c['cell_type'] == 'code', nb.cells))
    
for code_cells in each_code_cells:
    for code_cell in code_cells:
        code = InteractiveShell.instance().input_transformer_manager.transform_cell(code_cell.source)
        try:
            if code.split("\n")[0] == '### JUPYTER NOTEBOOK EAGER LOAD ###': continue
            get_ipython().run_cell_magic('capture', '', code)
        except RuntimeError:
            continue
