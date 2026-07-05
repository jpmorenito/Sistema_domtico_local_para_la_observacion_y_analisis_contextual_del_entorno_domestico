import fitz

pdf_path = "c:/Users/jacob/Downloads/TFG/Documento final/__memoria.pdf"
output_dir = "c:/Users/jacob/Downloads/TFG/Documento final/scratch"

doc = fitz.open(pdf_path)

for p in range(60, 73):
    idx = p - 1
    if idx < 0 or idx >= len(doc):
        continue
    page = doc.load_page(idx)
    zoom = 2.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    output_path = f"{output_dir}/check_page_tec_{p}.png"
    pix.save(output_path)
    print(f"Renderizada pag {p} en {output_path}")
