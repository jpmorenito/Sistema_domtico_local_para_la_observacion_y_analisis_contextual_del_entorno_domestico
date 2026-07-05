import fitz

pdf_path = "c:/Users/jacob/Downloads/TFG/Documento final/__memoria.pdf"
output_dir = "c:/Users/jacob/Downloads/TFG/Documento final/scratch"

doc = fitz.open(pdf_path)

target_labels = ["62", "63", "64"]

for i, page in enumerate(doc):
    label = page.get_label()
    if label in target_labels:
        zoom = 1.5
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        output_path = f"{output_dir}/verify_new_page_{label}.png"
        pix.save(output_path)
        print(f"Rendered absolute page {i+1} (printed page {label}) to {output_path}")
