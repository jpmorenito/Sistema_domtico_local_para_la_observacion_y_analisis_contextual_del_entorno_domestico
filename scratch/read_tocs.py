import os
try:
    import fitz  # PyMuPDF
except ImportError:
    print("Installing PyMuPDF...")
    os.system("pip install PyMuPDF")
    import fitz

def dump_toc(pdf_path):
    print(f"--- TOC for {os.path.basename(pdf_path)} ---")
    try:
        doc = fitz.open(pdf_path)
        toc = doc.get_toc()
        for item in toc:
            lvl, title, page = item
            print(f"{'  ' * (lvl - 1)}{title} (Page {page})")
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

dump_toc(r"C:\Users\jacob\Downloads\TFG\Memoria_JSS_2025_TFG_unsigned.pdf")
dump_toc(r"C:\Users\jacob\Downloads\TFG\TFG-Irene-Casares_V-FINAL.pdf")
