from PIL import Image, ImageDraw
import os
import shutil

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\Img"

img_bak_name = "conexion_nodo_ambiente_1779985459934.png"
img_bak = os.path.join(backup_dir, img_bak_name)
img_dest = os.path.join(img_dir, "conexion_nodo_ambiente.png")

if os.path.exists(img_bak):
    # Restore the backup image first to get a clean canvas
    shutil.copy(img_bak, img_dest)
    print(f"Restored {img_bak_name} to {img_dest}")
    
    with Image.open(img_dest) as img:
        draw = ImageDraw.Draw(img)
        
        # Get background color of the canvas (near the wire area, x=930, y=640)
        bg_color = img.getpixel((930, 640))
        print("Detected canvas background color:", bg_color)
        
        # 1. Erase the top header text
        draw.rectangle([0, 0, 1024, 140], fill="white")
        
        # 2. Erase the old wires in the open space y=614 to y=672, x=780 to x=915
        draw.rectangle([780, 614, 915, 672], fill=bg_color)
        
        # 3. Crop, rotate 180 degrees, and paste the relay module back
        # Crop coordinates: x=785 to 920, y=672 to 975
        relay_crop = img.crop((785, 672, 920, 975))
        rotated_relay = relay_crop.rotate(180)
        img.paste(rotated_relay, (785, 672))
        print("Rotated relay module pasted successfully.")
        
        # Define wire colors (Fritzing style)
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

        # The new rotated pin coordinates at y=684 are:
        # - Left pin (x=819) -> connected to GND (Black wire from x=885)
        # - Middle pin (x=852) -> connected to IN (Green wire from x=850)
        # - Right pin (x=886) -> connected to VCC (Red wire from x=815)
        
        # Wires crossing:
        # Black wire (GND): breadboard (885, 614) to relay (819, 684)
        draw_fritzing_wire((885, 614), (819, 684), black_core, black_border)
        
        # Red wire (VCC): breadboard (815, 614) to relay (886, 684)
        draw_fritzing_wire((815, 614), (886, 684), red_core, red_border)
        
        # Green wire (IN): breadboard (850, 614) to relay (852, 684)
        draw_fritzing_wire((850, 614), (852, 684), green_core, green_border)
        
        img.save(img_dest)
        print("Successfully corrected Figure 44 (relay rotated 180 degrees with crossed wires).")
else:
    print("Backup image not found.")
