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

# Step 1: Restore the original clean image
shutil.copy(img_bak, img_dest)
print("Restored backup image.")

with Image.open(img_dest) as img:
    img = img.convert("RGBA")
    draw = ImageDraw.Draw(img)
    
    # Step 2: Remove the top header of the diagram (white rectangle)
    # The header area is y=0 to y=140
    # Let's paint it white
    draw.rectangle([0, 0, 1024, 140], fill=(255, 255, 255, 255))
    
    # Step 3: Clear the entire right bottom quadrant (where the old relay and annotations were)
    # and replace it with a tiled clean grid.
    # Take a 74x74 tile from empty grid at (900, 150)
    tile = img.crop((900, 150, 974, 224))
    
    # We will tile the area x = 720 to 1024, y = 590 to 1024
    for px in range(715, 1024, 37):
        for py in range(583, 1024, 37):
            if px >= 720 and py >= 590:
                img.paste(tile, (px, py))
                
    print("Cleaned the background grid in the relay quadrant.")
    
    # Step 4: Load the preprocessed rotated transparent relay module
    # Size of 'relay_rotated_transparent.png' is 417x787
    relay = Image.open("relay_rotated_transparent.png")
    
    # Resize it to width = 110, height = 208 (preserving aspect ratio)
    relay_resized = relay.resize((110, 208), Image.Resampling.LANCZOS)
    
    # Position: center at x=850, bottom at y=920
    # x_min = 850 - 110//2 = 795
    # y_min = 920 - 208 = 712
    img.paste(relay_resized, (795, 712), mask=relay_resized)
    print("Pasted the resized relay module.")
    
    # Step 5: Draw beautiful bordered Fritzing-style wires from breadboard to relay pins
    # Breadboard coordinates at y = 614:
    # - Red: x = 815
    # - Green: x = 850
    # - Black: x = 885
    # Relay pin coordinates (pasted at 795, 712):
    # - VCC (Left): x = 795 + 39 = 834
    # - IN (Middle): x = 795 + 50 = 845
    # - GND (Right): x = 795 + 60 = 855
    # Tips of the pins are at y = 712
    
    # Fritzing wires colors:
    red_core = (215, 30, 30, 255)
    red_border = (120, 0, 0, 255)
    
    green_core = (40, 195, 70, 255)
    green_border = (25, 135, 45, 255)
    
    black_core = (65, 65, 65, 255)
    black_border = (0, 0, 0, 255)
    
    def draw_wire(start, end, core_col, border_col):
        # Draw border
        draw.line([start, end], fill=border_col, width=8, joint="round")
        # Draw core
        draw.line([start, end], fill=core_col, width=6, joint="round")
        # Draw endpoints dots
        draw.ellipse([start[0]-3, start[1]-3, start[0]+3, start[1]+3], fill=border_col)
        draw.ellipse([end[0]-3, end[1]-3, end[0]+3, end[1]+3], fill=border_col)

    # Draw Red wire (VCC)
    draw_wire((815, 614), (834, 712), red_core, red_border)
    
    # Draw Green wire (IN)
    draw_wire((850, 614), (845, 712), green_core, green_border)
    
    # Draw Black wire (GND)
    draw_wire((885, 614), (855, 712), black_core, black_border)
    print("Drew Fritzing-style wires.")
    
    # Step 6: Add centered text label "Relay Module" below the module
    font_label = get_font(16)
    # Clear a small rectangle for label text to ensure clean rendering (though tiled grid is clean)
    text_x = 850
    text_y = 945
    # Let's draw centered text
    draw.text((text_x, text_y), "Relay Module", fill=(0, 0, 0, 255), font=font_label, anchor="mm")
    print("Added centered label below the relay.")
    
    # Convert back to RGB and save
    final_img = img.convert("RGB")
    final_img.save(img_dest)
    print("Successfully corrected Figure 44!")
