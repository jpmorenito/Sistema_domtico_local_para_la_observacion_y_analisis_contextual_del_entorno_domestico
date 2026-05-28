with open('__memoria.log', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print("Searching for LaTeX errors:")
for i, line in enumerate(lines):
    if line.startswith('! '):
        print(f"Line {i+1}: {line.strip()}")
        # print the next few lines for context
        for j in range(1, 6):
            if i + j < len(lines):
                print(f"  {lines[i+j].strip()}")
