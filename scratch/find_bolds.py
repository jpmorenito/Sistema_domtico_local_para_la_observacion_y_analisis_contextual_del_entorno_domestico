import os
import re

tex_files = [f for f in os.listdir('.') if f.endswith('.tex')]
occurrences = []

for filename in tex_files:
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        matches = re.findall(r'\\textbf\{([^}]+)\}', line)
        if matches:
            occurrences.append({
                'file': filename,
                'line': i,
                'matches': matches,
                'text': line.strip()
            })

# Write to file
with open('scratch/bold_occurrences.txt', 'w', encoding='utf-8') as out:
    for occ in occurrences:
        out.write(f"File: {occ['file']} | Line: {occ['line']}\n")
        out.write(f"Matches: {occ['matches']}\n")
        out.write(f"Text: {occ['text']}\n")
        out.write("-" * 80 + "\n")

print(f"Done. Found {len(occurrences)} lines with \\textbf.")
