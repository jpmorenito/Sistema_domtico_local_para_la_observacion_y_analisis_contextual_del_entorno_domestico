from PIL import Image, ImageDraw, ImageFont
import os
import shutil

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\Img"

img_bak_name = "conexion_nodo_ambiente_1779985459934.png"
img_bak = os.path.join(backup_dir, img_bak_name)
img_dest = os.path.join(img_dir, "conexion_nodo_ambiente.png")

font_path = r"C:\Windows\Fonts\arial.ttf"

def get_font(size):
    try:
        return ImageFont.truetype(font_path, size)
    except IOError:
        return ImageFont.load_default()

if os.path.exists(img_bak):
    # Restore backup
    shutil.copy(img_bak, img_dest)
    print(f"Restored original backup to {img_dest}")
    
    with Image.open(img_dest) as img:
        draw = ImageDraw.Draw(img)
        
        # Get background color of the canvas (near the wire area, x=930, y=640)
        bg_color = img.getpixel((930, 640))
        print("Detected canvas background color:", bg_color)
        
        # 1. Erase the top header text
        draw.rectangle([0, 0, 1024, 140], fill="white")
        
        # 2. Erase the old wires in the open space y=614 to y=672, x=780 to x=915
        draw.rectangle([780, 614, 915, 672], fill=bg_color)
        
        # 3. Crop, rotate 180 degrees the relay module
        # Crop coordinates: x=785 to 920, y=672 to 975
        relay_crop = img.crop((785, 672, 920, 975))
        rotated_relay = relay_crop.rotate(180)
        
        # In the rotated crop, let's clean the upside-down PCB text using the royal blue background color
        pcb_blue = (42, 134, 201)
        r_draw = ImageDraw.Draw(rotated_relay)
        
        # - Paint over the top text area (y_crop = 15 to 45, covering old labels)
        r_draw.rectangle([10, 18, 125, 45], fill=pcb_blue)
        
        # - Paint over the left-side text area (y_crop = 80 to 220, covering old rotated "Relay Module" label)
        r_draw.rectangle([10, 80, 45, 220], fill=pcb_blue)
        
        # - Redraw "VCC", "IN", "GND" right-side up near the top pins (y_crop = 12 is the pin tip, let's put text around y_crop = 32)
        font_small = get_font(12)
        
        # VCC label under the left pin (x_crop = 33)
        r_draw.text((20, 30), "VCC", fill="white", font=font_small)
        # IN label under the middle pin (x_crop = 67)
        r_draw.text((58, 30), "IN", fill="white", font=font_small)
        # GND label under the right pin (x_crop = 100)
        r_draw.text((90, 30), "GND", fill="white", font=font_small)
        
        # Write "Relay Module" right-side up in the middle of the PCB (e.g. horizontally at y_crop = 160)
        font_msg = get_font(14)
        r_draw.text((25, 160), "Relay Module", fill="white", font=font_msg)
        
        # Paste the modified rotated relay back
        img.paste(rotated_relay, (785, 672))
        print("Rotated and relabeled relay pasted successfully.")
        
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

        # Draw wires straight down:
        # 1. Red wire (VCC): breadboard x=815 to relay VCC pin (x=818, y=684)
        draw_fritzing_wire((815, 614), (818, 684), red_core, red_border)
        
        # 2. Green wire (IN): breadboard x=850 to relay IN pin (x=852, y=684)
        draw_fritzing_wire((850, 614), (852, 684), green_core, green_border)
        
        # 3. Black wire (GND): breadboard x=885 to relay GND pin (x=885, y=684)
        draw_fritzing_wire((885, 614), (885, 684), black_core, black_border)
        
        img.save(img_dest)
        print("Successfully corrected Figure 44 (relay rotated and relabeled, with straight wires).")
else:
    print("Backup image not found.")
