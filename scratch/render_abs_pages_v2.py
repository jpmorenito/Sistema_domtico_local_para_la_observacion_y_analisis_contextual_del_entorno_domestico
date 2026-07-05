import fitz

pdf_path = "c:/Users/jacob/Downloads/TFG/Documento final/__memoria.pdf"
output_dir = "c:/Users/jacob/Downloads/TFG/Documento final/scratch"

abs_pages = [47, 48, 60, 61]

doc = fitz.open(pdf_path)

for page_num in abs_pages:
    idx = page_num - 1
    if idx < 0 or idx >= len(doc):
        continue
    page = doc.load_page(idx)
    zoom = 2.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    output_path = f"{output_dir}/render_abs_v2_{page_num}.png"
    pix.save(output_path)
    print(f"Renderizada página absoluta {page_num} en {output_path}")

print("Listo.")
