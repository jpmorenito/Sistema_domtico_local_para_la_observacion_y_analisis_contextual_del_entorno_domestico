with open('10_conclusiones.tex', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    ':} Se': ':} se',
    ':} Mediante': ':} mediante',
    ':} Toda': ':} toda',
    ':} Los': ':} los',
    ':} Con': ':} con',
    ':} El': ':} el',
    ':} Al': ':} al',
    ':} Reemplazar': ':} reemplazar',
    ':} Incorporar': ':} incorporar',
    ':} Configurar': ':} configurar',
    ':} Integrar': ':} integrar'
}

modified = content
for orig, rep in replacements.items():
    modified = modified.replace(orig, rep)

with open('10_conclusiones.tex', 'w', encoding='utf-8') as f:
    f.write(modified)

print("Capitalization fixed in 10_conclusiones.tex!")
