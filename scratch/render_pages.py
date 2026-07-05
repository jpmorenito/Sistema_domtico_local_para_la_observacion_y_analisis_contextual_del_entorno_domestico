import fitz  # PyMuPDF
import os

pdf_path = "c:/Users/jacob/Downloads/TFG/Documento final/__memoria.pdf"
output_dir = "c:/Users/jacob/Downloads/TFG/Documento final/scratch"

pages_to_render = [21, 31, 39, 40, 43, 45]  # Páginas en base 1

if not os.path.exists(pdf_path):
    print(f"Error: {pdf_path} no existe")
    exit(1)

doc = fitz.open(pdf_path)
print(f"Total páginas en el PDF: {len(doc)}")

for page_num in pages_to_render:
    idx = page_num - 1  # base 0
    if idx < 0 or idx >= len(doc):
        print(f"Error: La página {page_num} está fuera de rango")
        continue
    
    page = doc.load_page(idx)
    # Renderizar a alta resolución (zoom factor 2)
    zoom = 2.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    output_path = os.path.join(output_dir, f"pagina_{page_num}.png")
    pix.save(output_path)
    print(f"Renderizada página {page_num} en: {output_path}")

print("Proceso de renderizado completado.")
