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
    # Restore original backup
    shutil.copy(img_bak, img_dest)
    print(f"Restored original backup to {img_dest}")
    
    with Image.open(img_dest) as img:
        draw = ImageDraw.Draw(img)
        
        # Get canvas background color (x=930, y=640)
        bg_color = img.getpixel((930, 640))
        print("Detected canvas background color:", bg_color)
        
        # 1. Erase the top header text of the schematic
        draw.rectangle([0, 0, 1024, 140], fill="white")
        
        # 2. Erase the old wires in the open space y=614 to y=672, x=780 to x=915
        draw.rectangle([780, 614, 915, 672], fill=bg_color)
        
        # 3. Crop, rotate 180 degrees, and clean the relay module
        # Crop coordinates: x=785 to 920, y=672 to 975
        relay_crop = img.crop((785, 672, 920, 975))
        rotated_relay = relay_crop.rotate(180)
        
        # We draw on the rotated crop to clean up the upside-down text and wire stubs
        r_draw = ImageDraw.Draw(rotated_relay)
        
        # Colors:
        pcb_blue = (42, 134, 201)
        casing_blue = (130, 196, 244)
        terminals_gray = (69, 93, 103)
        
        # A. Erase the top upside-down "1-Channel Relay" text (y_crop = 0 to 18)
        # Fill with canvas bg_color to blend with the background above the relay
        r_draw.rectangle([0, 0, 135, 18], fill=bg_color)
        
        # B. Erase the upside-down "VCC", "IN", "GND" labels on the PCB (y_crop = 18 to 45)
        # Fill with PCB blue color
        r_draw.rectangle([10, 18, 125, 45], fill=pcb_blue)
        
        # C. Erase the upside-down vertical "Relay Module" text and other rotated markings on the light-blue casing (y_crop = 65 to 235)
        # Fill with casing light-blue color
        r_draw.rectangle([38, 65, 110, 235], fill=casing_blue)
        
        # D. Erase the wire stubs sticking out below the terminals (y_crop = 286 to 303)
        # Fill with white background
        r_draw.rectangle([0, 286, 135, 303], fill=(255, 255, 255))
        
        # E. Clean the wire entry ports inside the terminals (y_crop = 275 to 286)
        # Fill with terminals gray color
        r_draw.rectangle([15, 275, 120, 286], fill=terminals_gray)
        
        # F. Draw new clean labels right-side up on the PCB (y_crop = 32)
        font_small = get_font(12)
        # VCC (left pin is at x_crop = 33)
        r_draw.text((22, 30), "VCC", fill="white", font=font_small)
        # IN (middle pin is at x_crop = 67)
        r_draw.text((60, 30), "IN", fill="white", font=font_small)
        # GND (right pin is at x_crop = 100)
        r_draw.text((90, 30), "GND", fill="white", font=font_small)
        
        # G. Draw casing text right-side up on the light-blue casing
        font_casing_title = get_font(15)
        font_casing_sub = get_font(12)
        r_draw.text((48, 105), "Relay", fill="white", font=font_casing_title)
        r_draw.text((45, 130), "Module", fill="white", font=font_casing_title)
        r_draw.text((53, 165), "5V DC", fill="white", font=font_casing_sub)
        
        # Paste the modified rotated relay back onto the canvas at (785, 672)
        img.paste(rotated_relay, (785, 672))
        print("Rotated and cleaned relay pasted successfully.")
        
        # 4. Draw wires straight down:
        red_core = (215, 30, 30)
        red_border = (120, 0, 0)
        
        green_core = (40, 195, 70)
        green_border = (25, 135, 45)
        
        black_core = (65, 65, 65)
        black_border = (0, 0, 0)
        
        def draw_fritzing_wire(start, end, core_color, border_color):
            # Draw border (width=8)
            draw.line([start, end], fill=border_color, width=8, joint="round")
            # Draw core (width=6)
            draw.line([start, end], fill=core_color, width=6, joint="round")
            # Draw pin terminal dots
            draw.ellipse([start[0]-3, start[1]-3, start[0]+3, start[1]+3], fill=border_color)
            draw.ellipse([end[0]-3, end[1]-3, end[0]+3, end[1]+3], fill=border_color)

        # Red wire (VCC): breadboard (815, 614) to relay VCC pin (818, 684)
        draw_fritzing_wire((815, 614), (818, 684), red_core, red_border)
        
        # Green wire (IN): breadboard (850, 614) to relay IN pin (852, 684)
        draw_fritzing_wire((850, 614), (852, 684), green_core, green_border)
        
        # Black wire (GND): breadboard (885, 614) to relay GND pin (885, 684)
        draw_fritzing_wire((885, 614), (885, 684), black_core, black_border)
        
        # 5. Draw "1-Channel Relay" right-side up below the relay module (centered around x=852, y=982)
        font_bottom = get_font(13)
        draw.text((800, 982), "1-Channel Relay", fill="black", font=font_bottom)
        
        img.save(img_dest)
        print("Successfully corrected Figure 44 (perfect clean rotation, labels right-side up, wire stubs removed).")
else:
    print("Backup image not found.")
