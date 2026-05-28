import re

files_to_search = ["4_diseno_sistema.tex", "5_seleccion_tecnologias.tex", "A_manual_usuario.tex"]
keywords = ["pin", "sensor", "rele", "laser", "modelo", "ldr", "puerta", "esquema"]

for f in files_to_search:
    print(f"=== {f} ===")
    with open(f, "r", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()
        for idx, line in enumerate(lines, 1):
            if any(kw.lower() in line.lower() for kw in keywords) and ("dht" in line.lower() or "ld" in line.lower() or "ky" in line.lower() or "relay" in line.lower() or "g3mb" in line.lower() or "laser" in line.lower() or "reed" in line.lower()):
                print(f"  {idx}: {line.strip()}")
