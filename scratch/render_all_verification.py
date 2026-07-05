import fitz

pdf_path = "c:/Users/jacob/Downloads/TFG/Documento final/__memoria.pdf"
output_dir = "c:/Users/jacob/Downloads/TFG/Documento final/scratch"

doc = fitz.open(pdf_path)
print(f"Total paginas: {len(doc)}")

# Renderizar páginas de la 45 a la 55
for p in range(45, 56):
    idx = p - 1
    if idx < 0 or idx >= len(doc):
        continue
    page = doc.load_page(idx)
    zoom = 2.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    output_path = f"{output_dir}/verify_page_{p}.png"
    pix.save(output_path)
    print(f"Renderizada pag {p} en {output_path}")

# Renderizar páginas de la 65 a la 75
for p in range(65, 76):
    idx = p - 1
    if idx < 0 or idx >= len(doc):
        continue
    page = doc.load_page(idx)
    zoom = 2.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    output_path = f"{output_dir}/verify_page_{p}.png"
    pix.save(output_path)
    print(f"Renderizada pag {p} en {output_path}")
