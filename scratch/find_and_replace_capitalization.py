import os
import re

tex_files = [f for f in os.listdir('.') if f.endswith('.tex')]
tex_files = [f for f in tex_files if not f.startswith('__memoria_temp') and f != 'ALMCACENAMIENTO_TEMPORAL.tex']

lowercase_replacements = {
    r'\bHardware\b': 'hardware',
    r'\bSoftware\b': 'software',
    r'\bServidor\b': 'servidor',
    r'\bCliente\b': 'cliente',
    r'\bEnrutador\b': 'enrutador',
    r'\bMicrocontrolador\b': 'microcontrolador',
    r'\bSensor\b': 'sensor',
    r'\bRelé\b': 'relé',
    r'\bDiodo\b': 'diodo',
    r'\bLáser\b': 'láser',
    r'\bBanda\b': 'banda',
    r'\bFrecuencia\b': 'frecuencia',
    r'\bLatencia\b': 'latencia',
    r'\bConsumo\b': 'consumo',
    r'\bEnergía\b': 'energía',
    r'\bCoste\b': 'coste',
    r'\bPresupuesto\b': 'presupuesto',
    r'\bLicencia\b': 'licencia',
    # Do not include Internet as it can be considered a proper noun in many contexts.
}

# Regex to check if a word is preceded by a period, colon, item, or command/braces start
def should_replace(match, text):
    start = match.start()
    word = match.group(0)
    
    # Check context
    # Get preceding text in the same paragraph (up to 50 characters)
    preceding = text[max(0, start - 60):start]
    
    # Ignore if inside a LaTeX command name (like \Hardware) or macro definition
    if preceding.strip().endswith('\\') or re.search(r'\\[a-zA-Z]+$', preceding):
        return False
        
    # Ignore if inside a macro argument that shouldn't be touched (like label, ref, cite, url, texttt, lstinline)
    # Check if the word is inside curly braces preceded by a command like \label{...Word...}
    # A simple way is to check if the last open brace '{' is preceded by a command we don't want to touch
    open_braces = [m.start() for m in re.finditer(r'{', text[:start])]
    close_braces = [m.start() for m in re.finditer(r'}', text[:start])]
    if len(open_braces) > len(close_braces):
        # We are inside curly braces. Let's find the command preceding the last open brace
        last_open = open_braces[-1]
        pre_brace = text[max(0, last_open - 30):last_open].strip()
        # Commands to ignore: label, ref, cite, url, texttt, lstinline, input, include, graphicspath, documentclass, usepackage, bibliographystyle, bibliography, begin, end, shorthandoff, shorthandon, caption, section, subsection, subsubsection, author, director
        ignored_macros = [
            '\\label', '\\ref', '\\cite', '\\url', '\\texttt', '\\lstinline', '\\input', '\\include',
            '\\graphicspath', '\\documentclass', '\\usepackage', '\\bibliographystyle', '\\bibliography',
            '\\begin', '\\end', '\\shorthandoff', '\\shorthandon', '\\caption', '\\section', '\\subsection',
            '\\subsubsection', '\\author', '\\director', '\\newcommand', '\\renewcommand', '\\fancyhead', '\\fancyfoot',
            '\\hspace', '\\vspace', '\\addappheadtotoc', '\\appendixpage', '\\color', '\\definecolor'
        ]
        if any(pre_brace.endswith(macro) for macro in ignored_macros):
            return False
            
    # Check if it follows a period, colon, exclamation/question mark, item, start of line, or starts a sentence
    # We clean up preceding whitespace
    prec_clean = preceding.strip()
    if not prec_clean:
        return False # first word of the block, don't touch
        
    if prec_clean[-1] in {'.', ':', '?', '!', '\n'} or prec_clean.endswith('\\item') or prec_clean.endswith('\\textbf') or prec_clean.endswith('~') or prec_clean.endswith('\\noindent'):
        return False
        
    # Check if it is capitalized for a legitimate reason (like the first word in a list item, etc.)
    # In LaTeX, list items like \item \textbf{Word} or \item Word
    if re.search(r'\\item\s*(\\textbf\s*{)?\s*$', prec_clean):
        return False
        
    return True

for file_name in sorted(tex_files):
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
        
    modified = content
    changes = []
    
    for pattern, replacement in lowercase_replacements.items():
        for match in list(re.finditer(pattern, modified)):
            # We must recheck start position as content might shift, or we can just use match on current content
            # To be safe, we perform the replacement only if should_replace evaluates to True
            if should_replace(match, modified):
                # Save the context to print
                start = match.start()
                context = modified[max(0, start - 40):min(len(modified), start + 40)].replace('\n', ' ')
                changes.append((match.group(0), replacement, context))
                
    if changes:
        print(f"\nProposed changes in {file_name}:")
        for orig, rep, ctx in changes[:10]:
            print(f"  '{orig}' -> '{rep}' in context: ...{ctx}...")
        if len(changes) > 10:
            print(f"  ... and {len(changes) - 10} more changes.")
