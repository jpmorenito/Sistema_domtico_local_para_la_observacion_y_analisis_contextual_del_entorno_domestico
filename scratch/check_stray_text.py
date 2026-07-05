import fitz

pdf_path = "c:/Users/jacob/Downloads/TFG/Documento final/__memoria.pdf"
doc = fitz.open(pdf_path)

with open("c:/Users/jacob/Downloads/TFG/Documento final/scratch/page_text.txt", "w", encoding="utf-8") as out:
    for idx in [76, 77, 78]: # absolute pages (0-indexed: 76, 77, 78 are pages 77, 78, 79)
        if idx < len(doc):
            out.write(f"\n--- Absolute Page {idx+1} (printed {doc[idx].get_label()}) ---\n")
            out.write(doc[idx].get_text())
print("Done writing to page_text.txt")
