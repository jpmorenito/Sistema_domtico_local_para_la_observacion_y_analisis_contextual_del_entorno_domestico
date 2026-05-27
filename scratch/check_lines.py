with open('10_conclusiones.tex', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        print(f"Line {idx+1}: {repr(line)}")
