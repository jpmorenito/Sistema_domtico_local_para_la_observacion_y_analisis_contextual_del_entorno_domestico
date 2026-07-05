import fitz
import os

pdf_path = r"c:\Users\jacob\Downloads\TFG\Documento final\__memoria.pdf"
output_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"

doc = fitz.open(pdf_path)

# Render page 20 (0-indexed 19)
page = doc[19]
pix = page.get_pixmap(dpi=150)
img_path = os.path.join(output_dir, "table_page_20_index.png")
pix.save(img_path)
print("Saved page 20 to", img_path)
