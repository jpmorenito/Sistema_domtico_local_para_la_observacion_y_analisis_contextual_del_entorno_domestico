import fitz

pdf_path = "c:/Users/jacob/Downloads/TFG/Documento final/__memoria.pdf"
doc = fitz.open(pdf_path)

for idx, page in enumerate(doc):
    text = page.get_text()
    if "figura 20" in text.lower() or "figura 21" in text.lower() or "diagrama_flujo_fsm" in text.lower() or "bucle de ejecución" in text.lower() or "fusión en la fsm" in text.lower():
        print(f"Página absoluta {idx + 1} (impreso {page.rect}): contiene palabras clave.")
        
        # Renderizar
        zoom = 2.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        pix.save(f"c:/Users/jacob/Downloads/TFG/Documento final/scratch/check_page_{idx+1}.png")
        print(f"Renderizada página absoluta {idx+1} en scratch/check_page_{idx+1}.png")
