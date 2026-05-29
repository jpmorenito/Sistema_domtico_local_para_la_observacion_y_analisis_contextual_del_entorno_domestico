import re

def search_in_file(filepath):
    print(f"=== SEARCHING IN {filepath} ===")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if any(kw in line.lower() for kw in ['gpio', 'pin', 'define', 'const int', 'd26', 'd27', 'd32', 'd4', 'rele', 'ldr', 'dht11']):
            # Print line and its surroundings
            print(f"Line {i+1}: {line.strip()}")

search_in_file('B_manual_tecnico_codigo.tex')
search_in_file('9_planos_esquemas.tex')
