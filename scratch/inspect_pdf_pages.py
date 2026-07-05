import fitz  # PyMuPDF

doc = fitz.open(r"c:\Users\jacob\Downloads\TFG\Memoria_JSS_2025_TFG_unsigned.pdf")
print("Total pages:", len(doc))

# Let's inspect pages 4, 5, 6, 7 (0-indexed: 3, 4, 5, 6)
for i in [4, 5, 6]:
    print(f"\n--- PAGE {i+1} ---")
    page = doc[i]
    text_instances = page.get_text("blocks")
    for b in text_instances:
        print(f"Block: x0={b[0]:.1f}, y0={b[1]:.1f}, x1={b[2]:.1f}, y1={b[3]:.1f}")
        print(b[4].strip())
