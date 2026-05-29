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

if not os.path.exists(img_bak):
    print("Backup image not found!")
    exit(1)

# Step 1: Restore backup
shutil.copy(img_bak, img_dest)
print("Restored original backup image.")

with Image.open(img_dest) as img:
    img = img.convert("RGBA")
    draw = ImageDraw.Draw(img)
    
    # 1. Clean the top header (y = 0 to 140)
    draw.rectangle([0, 0, 1024, 140], fill=(255, 255, 255, 255))
    
    # 2. Extract a clean breadboard slice from x=200 to 274, y=140 to 620
    # Let's clean the breadboard regions left and right of ESP32
    # Grid period is 37 pixels. We can paste a 74-pixel wide clean slice.
    # The clean slice is from x=200 to 274
    clean_slice = img.crop((200, 140, 274, 620))
    
    # Clean left side of breadboard (x=70 to 342)
    # We step by 37 pixels and align paste coordinates
    for px in range(52, 342, 37):
        if px >= 70:
            img.paste(clean_slice, (px, 140))
            
    # Clean right side of breadboard (x=682 to 950)
    for px in range(681, 950, 37):
        img.paste(clean_slice, (px, 140))
        
    print("Cleaned all wire areas on the breadboard.")
    
    # 3. Clean the grid background in the relay quadrant (x=720 to 1024, y=590 to 1024)
    tile = img.crop((900, 150, 974, 224))
    for px in range(715, 1024, 37):
        for py in range(583, 1024, 37):
            if px >= 720 and py >= 590:
                img.paste(tile, (px, py))
    print("Cleaned background in relay quadrant.")
    
    # 4. Mirror the ESP32 horizontally at (342, 190, 682, 590)
    esp_crop = img.crop((342, 190, 682, 590))
    mirrored_esp = esp_crop.transpose(Image.FLIP_LEFT_RIGHT)
    img.paste(mirrored_esp, (342, 190))
    print("Mirrored ESP32 horizontally to match user's physical board layout.")
    
    # 5. Paste the rotated transparent relay at (795, 712)
    relay = Image.open("relay_rotated_transparent.png")
    relay_resized = relay.resize((110, 208), Image.Resampling.LANCZOS)
    img.paste(relay_resized, (795, 712), mask=relay_resized)
    print("Pasted relay module.")
    
    # 6. Draw Fritzing-style wires
    # Colors:
    red_core = (215, 30, 30, 255)
    red_border = (120, 0, 0, 255)
    
    blue_core = (30, 115, 185, 255)
    blue_border = (15, 55, 110, 255)
    
    green_core = (40, 195, 70, 255)
    green_border = (25, 135, 45, 255)
    
    yellow_core = (235, 205, 30, 255)
    yellow_border = (130, 115, 10, 255)
    
    orange_core = (235, 120, 30, 255)
    orange_border = (130, 60, 10, 255)
    
    black_core = (65, 65, 65, 255)
    black_border = (0, 0, 0, 255)
    
    def draw_wire(points, core_col, border_col):
        # points is a list of coordinates representing segments
        # Draw borders first
        for i in range(len(points)-1):
            draw.line([points[i], points[i+1]], fill=border_col, width=8, joint="round")
        # Draw cores
        for i in range(len(points)-1):
            draw.line([points[i], points[i+1]], fill=core_col, width=6, joint="round")
        # Draw dots at ends and turns
        for p in points:
            draw.ellipse([p[0]-3, p[1]-3, p[0]+3, p[1]+3], fill=border_col)

    # --- Power & Ground wires for ESP32 ---
    # Left side:
    # GND (row 14, y=455) -> bottom black rail (GND, y=614, x=326)
    draw_wire([(326, 455), (326, 614)], black_core, black_border)
    # VIN (row 15, y=474) -> bottom red rail (5V, y=603, x=310)
    draw_wire([(342, 474), (310, 474), (310, 603)], red_core, red_border)
    
    # Right side:
    # GND (row 14, y=455) -> top black rail (GND, y=153, x=696)
    draw_wire([(696, 455), (696, 153)], black_core, black_border)
    # 3V3 (row 15, y=474) -> top red rail (3V3, y=142, x=715)
    draw_wire([(682, 474), (715, 474), (715, 142)], red_core, red_border)
    
    # --- DHT11 connections (Left side) ---
    # VCC (x=115) -> top red rail (y=142)
    draw_wire([(115, 715), (115, 142)], red_core, red_border)
    # GND (x=169) -> top black rail (y=153)
    draw_wire([(169, 715), (169, 153)], black_core, black_border)
    # DATA (x=133) -> ESP32 D4 (right side, row 11, x=696, y=400)
    # Let's route it cleanly: up to y=350, right across the board to x=730, down to y=400, left to pin.
    draw_wire([(133, 715), (133, 335), (730, 335), (730, 400), (696, 400)], blue_core, blue_border)
    # NC (x=151) -> ESP32 D2 (right side, row 12, x=696, y=418)
    # Route it similarly: up to y=355, right to x=740, down to y=418, left to pin.
    draw_wire([(151, 715), (151, 355), (740, 355), (740, 418), (696, 418)], blue_core, blue_border)
    
    # --- LDR connections (Middle-left) ---
    # VCC (x=285) -> top red rail (y=142)
    draw_wire([(285, 735), (285, 142)], red_core, red_border)
    # GND (x=321) -> top black rail (y=153)
    draw_wire([(321, 735), (321, 153)], black_core, black_border)
    # SIG (x=303) -> ESP32 D32 (left side, row 6, x=326, y=308)
    # Direct short wire up to row 6
    draw_wire([(303, 735), (303, 308), (326, 308)], yellow_core, yellow_border)
    
    # --- Sound Sensor connections (Middle-right) ---
    # VCC (x=490) -> bottom red rail (y=603)
    draw_wire([(490, 715), (490, 603)], red_core, red_border)
    # GND (x=526) -> bottom black rail (y=614)
    draw_wire([(526, 715), (526, 614)], black_core, black_border)
    # OUT (x=508) -> ESP32 D27 (left side, row 10, x=326, y=381)
    # Route: up to y=381, left to x=326
    draw_wire([(508, 715), (508, 381), (326, 381)], orange_core, orange_border)
    
    # --- Relay connections (Right side) ---
    # VCC (x=834) -> bottom red rail (y=603)
    draw_wire([(834, 712), (834, 603)], red_core, red_border)
    # GND (x=855) -> bottom black rail (y=614)
    draw_wire([(855, 712), (855, 614)], black_core, black_border)
    # IN (x=845) -> ESP32 D26 (left side, row 9, x=326, y=363)
    # Route: up to y=363, left all the way to x=326
    draw_wire([(845, 712), (845, 363), (326, 363)], green_core, green_border)
    
    # 7. Add centered text label "Relay Module" below the module
    font_label = get_font(16)
    draw.text((850, 945), "Relay Module", fill=(0, 0, 0, 255), font=font_label, anchor="mm")
    
    final_img = img.convert("RGB")
    final_img.save(img_dest)
    print("All wires and ESP32 pinout updated successfully to match user's board layout!")
