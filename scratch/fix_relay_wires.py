from PIL import Image, ImageDraw
import os
import shutil

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\Img"

img_bak_name = "conexion_nodo_ambiente_1779985459934.png"
img_bak = os.path.join(backup_dir, img_bak_name)
img_dest = os.path.join(img_dir, "conexion_nodo_ambiente.png")

if os.path.exists(img_bak):
    # Restore the backup first
    shutil.copy(img_bak, img_dest)
    print(f"Restored {img_bak_name} to {img_dest}")
    
    with Image.open(img_dest) as img:
        draw = ImageDraw.Draw(img)
        
        # Get background color of the canvas (near the wire area but clear of wires, e.g. x=930, y=640)
        bg_color = img.getpixel((930, 640))
        print("Detected canvas background color:", bg_color)
        
        # 1. Erase the top header text
        # The text is at y=0 to y=140. We fill it with white as done previously.
        draw.rectangle([0, 0, 1024, 140], fill="white")
        
        # 2. Erase the three old vertical wires in the open space y=614 to y=672, x=790 to x=910
        # We fill this area with the canvas background color to cleanly remove the wire segments.
        draw.rectangle([790, 614, 910, 672], fill=bg_color)
        
        # Define the wire colors
        red_core = (215, 30, 30)
        red_border = (120, 0, 0)
        
        green_core = (40, 195, 70)
        green_border = (25, 135, 45)
        
        black_core = (65, 65, 65)
        black_border = (0, 0, 0)
        
        # Helper to draw a bordered line (Fritzing style)
        def draw_fritzing_wire(start, end, core_color, border_color):
            # Draw border (width=8)
            draw.line([start, end], fill=border_color, width=8, joint="round")
            # Draw core (width=6)
            draw.line([start, end], fill=core_color, width=6, joint="round")
        
        # Redraw wires:
        # Left wire (Red): straight from breadboard x=815 to relay x=815
        draw_fritzing_wire((815, 614), (815, 672), red_core, red_border)
        
        # Middle wire (Black): from breadboard GND (x=885) to relay GND (x=850)
        draw_fritzing_wire((885, 614), (850, 672), black_core, black_border)
        
        # Right wire (Green): from breadboard GPIO 26 (x=850) to relay IN (x=885)
        draw_fritzing_wire((850, 614), (885, 672), green_core, green_border)
        
        img.save(img_dest)
        print("Successfully corrected Figure 44 (relay wires).")
else:
    print("Backup image not found.")
