import os
import re

tex_files = {
    "introduccion": "c:/Users/jacob/Downloads/TFG/Documento final/1_introduccion.tex",
    "contexto": "c:/Users/jacob/Downloads/TFG/Documento final/2_contexto_estado_arte.tex",
    "requisitos": "c:/Users/jacob/Downloads/TFG/Documento final/3_analisis_requisitos.tex",
    "diseno": "c:/Users/jacob/Downloads/TFG/Documento final/4_diseno_sistema.tex",
    "seleccion": "c:/Users/jacob/Downloads/TFG/Documento final/5_seleccion_tecnologias.tex",
    "implantacion": "c:/Users/jacob/Downloads/TFG/Documento final/6_plan_implantacion.tex",
    "evaluacion": "c:/Users/jacob/Downloads/TFG/Documento final/7_evaluacion_sistema.tex"
}

def check_file_for_words(file_path, words):
    if not os.path.exists(file_path):
        return f"File {file_path} does not exist"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    found = []
    for word in words:
        matches = list(re.finditer(re.escape(word), content, re.IGNORECASE))
        if matches:
            found.append((word, len(matches)))
    return found

print("=== CHECKING FOR SPECIFIC HARDWARE IN REQUIREMENTS ===")
req_words = ["esp32", "raspberry", "esphome", "home assistant", "home-assistant"]
found_in_reqs = check_file_for_words(tex_files["requisitos"], req_words)
print("In 3_analisis_requisitos.tex:")
print(found_in_reqs)

print("\n=== CHECKING FOR SYSTEM DESIGN CONTENT (E-R, Class, Procedural) ===")
# We want to check if 4_diseno_sistema.tex contains:
# - Diagrama Entidad-Relación (diagrama_er.png or similar)
# - Modelo/diagrama de clases (diagrama_clases)
# - Tablas de atributos/métodos (tabular and descriptions)
# - Diagrama de flujo general y subdiagramas
with open(tex_files["diseno"], "r", encoding="utf-8") as f:
    diseno_content = f.read()

checks = {
    "Diagrama E-R": "diagrama_er" in diseno_content,
    "Diagrama de Clases": "diagrama_clases" in diseno_content or "diagrama_clases_firmware" in diseno_content,
    "Modelo de Módulos (Tabla Ambiente)": "tab:mod_nodo_ambiente" in diseno_content,
    "Modelo de Módulos (Tabla Escritorio)": "tab:mod_nodo_escritorio" in diseno_content,
    "Modelo de Módulos (Tabla Puerta)": "tab:mod_nodo_puerta" in diseno_content,
    "Modelo de Módulos (Tabla Servidor)": "tab:mod_motor_contexto" in diseno_content,
    "Diagrama de Flujo General": "diagrama_flujo_general" in diseno_content,
    "Diagrama de Flujo FSM / Subdiagramas": "diagrama_flujo_fsm_parte1" in diseno_content or "diagrama_flujo_fsm" in diseno_content
}

for name, val in checks.items():
    print(f"{name}: {'YES' if val else 'NO'}")

print("\n=== CHECKING FOR COMPONENT SELECTION JUSTIFICATION ===")
# We want to check if 5_seleccion_tecnologias.tex contains selection justification (price, support, etc.)
with open(tex_files["seleccion"], "r", encoding="utf-8") as f:
    seleccion_content = f.read()

checks_seleccion = {
    "Justificación de Raspberry Pi": "Raspberry Pi 4 Model B" in seleccion_content and "memoria RAM" in seleccion_content,
    "Justificación de ESP32": "ESP32" in seleccion_content and "Espressif Systems" in seleccion_content,
    "Criterios de selección (precio, etc.)": "criterios" in seleccion_content or "viabilidad económica" in seleccion_content
}

for name, val in checks_seleccion.items():
    print(f"{name}: {'YES' if val else 'NO'}")
