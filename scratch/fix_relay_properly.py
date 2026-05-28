from PIL import Image, ImageDraw
import os
import shutil

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\Img"

img_bak_name = "conexion_nodo_ambiente_1779985459934.png"
img_bak = os.path.join(backup_dir, img_bak_name)
img_dest = os.path.join(img_dir, "conexion_nodo_ambiente.png")

if os.path.exists(img_bak):
    # Restore the original backup first to get a clean image
    shutil.copy(img_bak, img_dest)
    print(f"Restored {img_bak_name} to {img_dest}")
    
    with Image.open(img_dest) as img:
        draw = ImageDraw.Draw(img)
        
        # Get the canvas background color to erase the old wires
        bg_color = img.getpixel((930, 640))
        print("Detected canvas background color:", bg_color)
        
        # 1. Erase the top header text
        draw.rectangle([0, 0, 1024, 140], fill="white")
        
        # 2. Erase the old wires in the open space y=614 to y=672, x=790 to x=910
        # This removes the incorrect wire segments connecting to the top terminals
        draw.rectangle([790, 614, 910, 672], fill=bg_color)
        
        # Define the wire colors (Fritzing style)
        red_core = (215, 30, 30)
        red_border = (120, 0, 0)
        
        green_core = (40, 195, 70)
        green_border = (25, 135, 45)
        
        black_core = (65, 65, 65)
        black_border = (0, 0, 0)
        
        # Helper to draw a bordered line
        def draw_fritzing_wire(start, end, core_color, border_color):
            # Draw border (width=8)
            draw.line([start, end], fill=border_color, width=8, joint="round")
            # Draw core (width=6)
            draw.line([start, end], fill=core_color, width=6, joint="round")
            # Draw pin terminal dots at endpoints
            draw.ellipse([start[0]-3, start[1]-3, start[0]+3, start[1]+3], fill=border_color)
            draw.ellipse([end[0]-3, end[1]-3, end[0]+3, end[1]+3], fill=border_color)
        
        # Draw new wires going all the way down to the bottom pins (y=962):
        # 1. Red wire (VCC): from breadboard (815, 614) to relay bottom VCC pin (818, 962)
        draw_fritzing_wire((815, 614), (818, 962), red_core, red_border)
        
        # 2. Green wire (IN): from breadboard (850, 614) to relay bottom IN pin (852, 962)
        draw_fritzing_wire((850, 614), (852, 962), green_core, green_border)
        
        # 3. Black wire (GND): from breadboard (885, 614) to relay bottom GND pin (885, 962)
        draw_fritzing_wire((885, 614), (885, 962), black_core, black_border)
        
        img.save(img_dest)
        print("Successfully corrected Figure 44 (relay connected to bottom pins).")
else:
    print("Backup image not found.")
