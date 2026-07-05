import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open(r"c:\Users\jacob\Downloads\TFG\Documento final\__memoria.pdf")
print("Total pages in PDF:", len(doc))

toc = doc.get_toc()
print("Complete TOC:")
for entry in toc:
    print(entry)


# Let's find pages matching "Índice de tablas"
found_page = None
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    if "Índice de tablas" in text or "INDICE DE TABLAS" in text:
        print(f"Found on page {page_num + 1}")
        found_page = page_num + 1
