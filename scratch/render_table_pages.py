import fitz
import os

pdf_path = r"c:\Users\jacob\Downloads\TFG\Documento final\__memoria.pdf"
output_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"

doc = fitz.open(pdf_path)

pages_to_render = [43, 107, 111, 112, 113]

for p in pages_to_render:
    page_num = p - 1 # 0-indexed
    if page_num < len(doc):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=150)
        img_path = os.path.join(output_dir, f"table_page_{p}.png")
        pix.save(img_path)
        print(f"Saved page {p} to {img_path}")
