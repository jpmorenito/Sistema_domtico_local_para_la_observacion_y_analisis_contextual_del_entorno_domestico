import fitz  # PyMuPDF
import os

pdf_path = r"c:\Users\jacob\Downloads\TFG\Documento final\__memoria.pdf"
output_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"

doc = fitz.open(pdf_path)
print(f"Total pages: {len(doc)}")

for page_num in [1, 2, 3, 4, 5]:
    if page_num < len(doc):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=150)
        img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(img_path)
        print(f"Saved page {page_num + 1} to {img_path}")

