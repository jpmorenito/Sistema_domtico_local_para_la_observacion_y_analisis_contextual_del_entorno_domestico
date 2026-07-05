import os
import re

tex_files = [f for f in os.listdir('.') if f.endswith('.tex')]
cite_pattern = re.compile(r'\\cite\{([^}]+)\}')

citations_extracted = []

for filename in tex_files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove comments
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        comment_start = -1
        for idx, char in enumerate(line):
            if char == '%':
                if idx == 0 or line[idx-1] != '\\':
                    comment_start = idx
                    break
        if comment_start != -1:
            line = line[:comment_start]
        cleaned_lines.append(line)
    
    content_clean = '\n'.join(cleaned_lines)
    
    # Split content by paragraphs (double newlines)
    paragraphs = content_clean.split('\n\n')
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        
        matches = cite_pattern.findall(paragraph)
        if matches:
            # Clean up whitespace inside paragraph
            paragraph_clean = re.sub(r'\s+', ' ', paragraph)
            citations_extracted.append({
                'file': filename,
                'keys': matches,
                'text': paragraph_clean
            })

with open('scratch/citations_paragraphs.txt', 'w', encoding='utf-8') as out:
    for idx, item in enumerate(citations_extracted, 1):
        out.write(f"#{idx} | File: {item['file']} | Cited Keys: {item['keys']}\n")
        out.write(f"Text:\n{item['text']}\n")
        out.write("="*80 + "\n")

print(f"Done. Extracted {len(citations_extracted)} paragraphs containing citations.")
