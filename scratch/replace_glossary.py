import re

filepath = r"c:\Users\jacob\Downloads\TFG\Documento final\__memoria.tex"

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

# We need to find the lines for the glossary.
# From the file contents:
# Line 168: \section*{Glosario de abreviaturas}
# Line 169: \addcontentsline{toc}{section}{Glosario de abreviaturas}
# We want to replace everything from the line after that (around line 170) up to the line before %---------------------% (around line 234)

start_idx = None
end_idx = None
for idx, line in enumerate(lines):
    if "Glosario de abreviaturas" in line and "\\addcontentsline" in line:
        start_idx = idx + 1
    if "%---------------------%" in line and idx > 200:
        end_idx = idx
        break

print(f"Glossary start line index: {start_idx}, end line index: {end_idx}")

# Let's extract the list of items from the tabularx environments in that range.
glossary_content = "\n".join(lines[start_idx:end_idx])

# Find all lines like: \textbf{KEY} & VALUE \\
pattern = r"\\textbf\{([^}]+)\}\s*&\s*([^\\]+)\s*\\\\"
items = re.findall(pattern, glossary_content)

print(f"Found {len(items)} items:")
for k, v in items[:5]:
    print(f"  {k} -> {v}")

# Now build the description list
new_glossary = []
new_glossary.append(r"\begin{description}[leftmargin=2.2cm, labelwidth=1.9cm, align=left, labelsep=0.3cm, itemsep=4pt, parsep=0pt, topsep=0pt]")
for k, v in items:
    # Clean up value (strip trailing spaces)
    v_clean = v.strip()
    new_glossary.append(f"    \\item[\\textbf{{{k}}}] {v_clean}")
new_glossary.append(r"\end{description}")
new_glossary.append("") # empty line

# Replace in lines
lines[start_idx:end_idx] = new_glossary

with open(filepath, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("Replacement done successfully!")
