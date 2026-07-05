import os
import subprocess

aux_exts = ['.aux', '.out', '.lof', '.toc', '.log', '.bbl', '.blg', '.fdb_latexmk', '.fls', '.synctex.gz']
base_name = '__memoria'

for ext in aux_exts:
    path = base_name + ext
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"Removed: {path}")
        except Exception as e:
            print(f"Error removing {path}: {e}")

print("Running pdflatex (run 1)...")
subprocess.run(['pdflatex', '-interaction=nonstopmode', '-shell-escape', '__memoria.tex'], cwd='.')

print("Running bibtex...")
subprocess.run(['bibtex', '__memoria'], cwd='.')

print("Running pdflatex (run 2)...")
subprocess.run(['pdflatex', '-interaction=nonstopmode', '-shell-escape', '__memoria.tex'], cwd='.')

print("Running pdflatex (run 3)...")
subprocess.run(['pdflatex', '-interaction=nonstopmode', '-shell-escape', '__memoria.tex'], cwd='.')
