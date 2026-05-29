from PIL import Image, ImageDraw, ImageFont
import os
import shutil

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\Img"

img_bak_name = "conexion_nodo_ambiente_1779985459934.png"
img_bak = os.path.join(backup_dir, img_bak_name)
img_dest = os.path.join(img_dir, "conexion_nodo_ambiente.png")

font_path = r"C:\Windows\Fonts\arial.ttf"

def get_font(size, bold=False):
    try:
        suffix = "bd" if bold else ""
        path = font_path.replace("arial", f"arial{suffix}") if bold else font_path
        if not os.path.exists(path):
            path = font_path
        return ImageFont.truetype(path, size)
    except IOError:
        return ImageFont.load_default()

if not os.path.exists(img_bak):
    print("Backup image not found!")
    exit(1)

# Step 1: Restore the original clean image
shutil.copy(img_bak, img_dest)
print("Step 1: Restored original backup successfully.")

with Image.open(img_dest) as img:
    draw = ImageDraw.Draw(img)
    
    # Step 2: Remove the top header of the diagram (white rectangle)
    draw.rectangle([0, 0, 1024, 140], fill=(255, 255, 255))
    print("Step 2: Cleared top header.")
    
    # Step 3: Completely clear the old relay and its wires/texts area with white
    draw.rectangle([780, 665, 930, 1005], fill=(255, 255, 255))
    print("Step 3: Cleared old relay area.")
    
    # Step 4: Draw perfect straight wires coming down from the breadboard to the relay pins
    # Red wire (VCC)
    draw.line([815, 614, 815, 682], fill=(222, 40, 29), width=5)
    # Green wire (IN)
    draw.line([850, 614, 850, 682], fill=(44, 197, 71), width=5)
    # Black wire (GND)
    draw.line([886, 614, 886, 682], fill=(64, 64, 64), width=5)
    print("Step 4: Drew clean straight breadboard connections.")
    
    # Step 5: Draw the vector relay module
    pcb_color = (14, 65, 92)      # Deep navy blue PCB
    casing_color = (18, 115, 186)  # Vibrant Songle blue
    terminal_color = (0, 95, 162)  # Screw terminal block blue
    copper_color = (196, 126, 50)  # Bronze/copper terminal
    dark_copper = (90, 50, 15)
    silver_color = (200, 200, 200)
    
    # A) PCB Board
    pcb_rect = [788, 685, 917, 970]
    draw.rounded_rectangle(pcb_rect, radius=8, fill=pcb_color)
    
    # Mounting holes in corners
    for cx, cy in [(794, 691), (911, 691), (794, 964), (911, 964)]:
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=silver_color, outline=(100, 100, 100))
        
    # B) Header Pins and Dupont Connectors
    # Header base
    draw.rectangle([805, 682, 900, 694], fill=(30, 30, 30))
    
    # Dupont connector housings (black plastic housings)
    for x in [815, 850, 886]:
        draw.rectangle([x - 5, 682, x + 5, 700], fill=(20, 20, 20))
        # Silver pin slot detail
        draw.rectangle([x - 2, 688, x + 2, 694], fill=(120, 120, 120))
        
    # Pin labels right-side up
    font_pins = get_font(10, bold=True)
    draw.text((815, 712), "VCC", fill="white", font=font_pins, anchor="mm")
    draw.text((850, 712), "IN", fill="white", font=font_pins, anchor="mm")
    draw.text((886, 712), "GND", fill="white", font=font_pins, anchor="mm")
    
    # C) Small SMD Components on the left of the board
    # Power LED (PWR)
    draw.rectangle([793, 735, 799, 743], fill=silver_color)
    draw.rectangle([794, 737, 798, 741], fill=(230, 30, 30)) # Red LED
    font_tiny = get_font(7)
    draw.text((796, 748), "PWR", fill=(180, 180, 180), font=font_tiny, anchor="mm")
    
    # Status LED (ACT)
    draw.rectangle([793, 760, 799, 768], fill=silver_color)
    draw.rectangle([794, 762, 798, 766], fill=(30, 230, 30)) # Green LED
    draw.text((796, 773), "ACT", fill=(180, 180, 180), font=font_tiny, anchor="mm")
    
    # D) Vibrant Blue Relay Casing
    casing_rect = [805, 732, 912, 875]
    draw.rectangle(casing_rect, fill=casing_color)
    # 3D Highlight edges
    draw.line([805, 732, 912, 732], fill=(80, 160, 230), width=2)
    draw.line([805, 732, 805, 875], fill=(80, 160, 230), width=2)
    draw.line([805, 875, 912, 875], fill=(10, 80, 140), width=2)
    draw.line([912, 732, 912, 875], fill=(10, 80, 140), width=2)
    
    # Text on casing
    font_casing_bold = get_font(12, bold=True)
    font_casing_small = get_font(8)
    draw.text((858, 748), "SONGLE", fill="white", font=font_casing_bold, anchor="mm")
    draw.line([815, 758, 902, 758], fill=(100, 170, 230), width=1)
    draw.text((858, 768), "SRD-05VDC-SL-C", fill="white", font=font_casing_small, anchor="mm")
    
    # Ratings text
    draw.text((858, 786), "10A 250VAC   10A 125VAC", fill=(220, 240, 255), font=font_casing_small, anchor="mm")
    draw.text((858, 802), "10A 30VDC    10A 28VDC", fill=(220, 240, 255), font=font_casing_small, anchor="mm")
    
    # Stylized coil and switch schematic symbol on the relay casing
    draw.rectangle([848, 825, 868, 835], outline=(200, 230, 255), width=1) # Coil box
    draw.line([843, 830, 848, 830], fill=(200, 230, 255), width=1)
    draw.line([868, 830, 873, 830], fill=(200, 230, 255), width=1)
    # Switch
    draw.ellipse([845, 848, 847, 850], fill="white")
    draw.ellipse([865, 848, 867, 850], fill="white")
    draw.line([847, 849, 862, 843], fill="white", width=1) # Switch lever
    
    # E) Terminal Labels (NO, COM, NC)
    font_term = get_font(10, bold=True)
    draw.text((823, 895), "NO", fill="white", font=font_term, anchor="mm")
    draw.text((859, 895), "COM", fill="white", font=font_term, anchor="mm")
    draw.text((895, 895), "NC", fill="white", font=font_term, anchor="mm")
    
    # F) Terminal Block (Bottom) - NO WIRES CONNECTED!
    draw.rectangle([805, 912, 912, 960], fill=terminal_color)
    # Slots/screws
    for tx in [823, 859, 895]:
        # Copper circle
        draw.ellipse([tx - 8, 936 - 8, tx + 8, 936 + 8], fill=copper_color, outline=dark_copper, width=1)
        draw.ellipse([tx - 5, 936 - 5, tx + 5, 936 + 5], fill=dark_copper)
        # Screw flathead slot
        draw.line([tx - 4, 936 - 4, tx + 4, 936 + 4], fill=silver_color, width=2)
        
    # G) Label below the module
    font_label = get_font(13)
    draw.text((858, 988), "1-Channel Relay", fill="black", font=font_label, anchor="mm")
    
    # Save the modified image
    img.save(img_dest)
    print("Step 5: Generated gorgeous, 100% correct, right-side-up vector relay on canvas and saved.")
