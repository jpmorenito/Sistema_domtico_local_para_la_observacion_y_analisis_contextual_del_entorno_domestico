import os
import re

# Find all .tex files
tex_files = [f for f in os.listdir('.') if f.endswith('.tex')]

citations_in_text = set()

# Regular expression to find \cite{key1,key2,...}
cite_pattern = re.compile(r'\\cite\{([^}]+)\}')

for filename in tex_files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove comments to avoid counting citations in commented out lines
    # (LaTeX comments start with %) but be careful with \%
    # A simple way: find comments and remove them
    # But since \% exists, we must handle that or keep it simple.
    lines = content.split('\n')
    cleaned_content = []
    for line in lines:
        # Check if line contains a comment character '%' not preceded by '\'
        # Let's do a simple split or regex
        comment_start = -1
        for idx, char in enumerate(line):
            if char == '%':
                if idx == 0 or line[idx-1] != '\\':
                    comment_start = idx
                    break
        if comment_start != -1:
            line = line[:comment_start]
        cleaned_content.append(line)
    
    content_no_comments = '\n'.join(cleaned_content)
    
    # Find all matches
    for match in cite_pattern.finditer(content_no_comments):
        keys = match.group(1).split(',')
        for key in keys:
            citations_in_text.add(key.strip())

# Find all keys in referencias.bib
bib_keys = set()
key_pattern = re.compile(r'@\w+\{([^,]+),')

with open('referencias.bib', 'r', encoding='utf-8') as f:
    bib_content = f.read()

for match in key_pattern.finditer(bib_content):
    bib_keys.add(match.group(1).strip())

# Compare
missing_in_bib = citations_in_text - bib_keys
unused_in_bib = bib_keys - citations_in_text

print(f"Total citations found in text: {len(citations_in_text)}")
print(f"Total keys found in .bib: {len(bib_keys)}")
print("\n--- Missing in referencias.bib (cited but not defined) ---")
if missing_in_bib:
    for key in missing_in_bib:
        print(f" - {key}")
else:
    print("None!")

print("\n--- Unused in referencias.bib (defined but not cited) ---")
if unused_in_bib:
    for key in unused_in_bib:
        print(f" - {key}")
else:
    print("None!")
