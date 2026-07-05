import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open(r"c:\Users\jacob\Downloads\TFG\Documento final\__memoria.pdf")
print("Total pages in PDF:", len(doc))

# Let's print the outline (TOC) of the PDF
toc = doc.get_toc()
print("TOC:")
for entry in toc[:20]:
    print(entry)

print("\nLast 5 pages text snippet:")
for page_num in range(len(doc)-5, len(doc)):
    page = doc[page_num]
    text = page.get_text()
    print(f"--- Page {page_num + 1} ---")
    print(repr(text[:200]))

