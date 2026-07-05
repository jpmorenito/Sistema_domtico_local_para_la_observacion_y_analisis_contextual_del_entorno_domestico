import fitz

doc = fitz.open(r"c:\Users\jacob\Downloads\TFG\Documento final\__memoria.pdf")
print("Total pages:", len(doc))

tables = ["tab:trazabilidad", "tab:mod_nodo_ambiente", "tab:mod_nodo_escritorio", 
          "tab:mod_nodo_puerta", "tab:mod_motor_contexto", "tab:esquema_relacional_1", 
          "tab:esquema_relacional_2", "tab:protocolos_osi", "tab:hw_central", 
          "tab:pir_vs_mmwave_comp", "tab:sw_domotica", "tab:ha_instalacion", 
          "tbl:consumo_electrico", "tbl:presupuesto_hardware", "tbl:presupuesto_software", 
          "tbl:mano_obra", "tbl:resumen_presupuesto"]

found = {}
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    
    # We can search for the caption texts or the numbers.
    # Since we can't search for labels in the PDF directly, let's search for unique words:
    # "Matriz de trazabilidad"
    # "Perfil de consumo eléctrico"
    # "Presupuesto desglosado"
    # "Presupuesto de licencias"
    # "Presupuesto estimado de mano"
    # "Resumen económico"
    
    queries = {
        "trazabilidad": "Matriz de trazabilidad",
        "consumo": "Perfil de consumo",
        "hardware": "Presupuesto desglosado",
        "software": "Presupuesto de licencias",
        "mano_obra": "Presupuesto estimado",
        "resumen": "Resumen económico"
    }
    
    for key, q in queries.items():
        if q in text:
            found[key] = page_num + 1

print("Found table pages:", found)
