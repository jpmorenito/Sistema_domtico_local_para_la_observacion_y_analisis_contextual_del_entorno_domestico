with open("c:/Users/jacob/Downloads/TFG/Documento final/__memoria.toc", "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    if "\\contentsline {section}" in line or "\\contentsline {subsection}" in line:
        print(line.strip())
