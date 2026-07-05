import fitz

pdf_path = "c:/Users/jacob/Downloads/TFG/Documento final/__memoria.pdf"
doc = fitz.open(pdf_path)

targets = {
    "fig:edge_privacy": "Arquitectura de red aislada",
    "fig:diagrama_clases": "Diagrama de clases UML",
    "tab:esquema_relacional_1": "Diccionario de datos (Parte I",
    "tab:esquema_relacional_2": "Diccionario de datos (Parte II",
    "fig:diagrama_flujo_general": "Diagrama de flujo general",
    "fig:diagrama_flujo_fsm": "fusión en la FSM del Servidor"
}

output_dir = "c:/Users/jacob/Downloads/TFG/Documento final/scratch"

for label, keyword in targets.items():
    found_pages = []
    for idx, page in enumerate(doc):
        text = page.get_text()
        if keyword.lower() in text.lower():
            found_pages.append(idx + 1)  # base 1
            
            # Renderizar la página encontrada
            zoom = 2.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            output_path = f"{output_dir}/render_{label.replace(':', '_')}.png"
            pix.save(output_path)
            print(f"Encontrado {label} en página absoluta {idx + 1}. Renderizado en: {output_path}")

print("Completado.")
