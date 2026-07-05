import re

with open('scratch/bold_occurrences.txt', 'r', encoding='utf-8') as f:
    content = f.read()

entries = content.split("--------------------------------------------------------------------------------\n")

suspicious = []

for entry in entries:
    if not entry.strip():
        continue
    
    # Parse entry
    file_match = re.search(r'File: (.*?) \| Line: (\d+)', entry)
    matches_match = re.search(r'Matches: (.*)', entry)
    text_match = re.search(r'Text: (.*)', entry)
    
    if file_match and matches_match and text_match:
        filename = file_match.group(1)
        line_num = int(file_match.group(2))
        matches = eval(matches_match.group(1))
        text = text_match.group(1)
        
        # Check if it's an item heading, e.g., "\item \textbf{something}"
        is_item_heading = False
        if text.startswith('\\item \\textbf{'):
            # It's an item heading. But let's check if there are OTHER bold matches in the same line!
            # If the only match is the one at the start, it's fine.
            # But if there are multiple matches, or if a match is not at the start, let's inspect.
            # Let's count occurrences of \textbf; if only 1, it's item heading.
            num_tb = text.count('\\textbf{')
            if num_tb == 1:
                is_item_heading = True
        
        # Check if it's in a table
        is_table = any(x in text for x in ['\\multicolumn', '\\centering', '&', '\\rowcolor', '\\textbf{Palabras clave:}', '\\textbf{Keywords:}'])
        
        # Check if it's a section
        is_section = any(x in text for x in ['\\section', '\\subsection', '\\subsubsection', '\\paragraph', '\\subparagraph'])
        
        if not (is_item_heading or is_table or is_section):
            suspicious.append({
                'file': filename,
                'line': line_num,
                'matches': matches,
                'text': text
            })

with open('scratch/suspicious_bolds.txt', 'w', encoding='utf-8') as out:
    out.write(f"Found {len(suspicious)} suspicious bold occurrences:\n\n")
    for s in suspicious:
        out.write(f"File: {s['file']} | Line: {s['line']}\n")
        out.write(f"Matches: {s['matches']}\n")
        out.write(f"Text: {s['text']}\n")
        out.write("="*60 + "\n")

print(f"Done. Wrote {len(suspicious)} suspicious bold occurrences to scratch/suspicious_bolds.txt")
