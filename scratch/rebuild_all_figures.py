import os
from PIL import Image, ImageDraw, ImageFont

# Directory paths
backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
art_dir = os.path.join(backup_dir, "artifacts")
img_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\Img"
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

# Wire Colors for Relay Wires in Ambiente
red_core = (215, 30, 30, 255)
red_border = (120, 0, 0, 255)
green_core = (40, 195, 70, 255)
green_border = (25, 135, 45, 255)
black_core = (65, 65, 65, 255)
black_border = (0, 0, 0, 255)

def draw_wire(draw, points, core_col, border_col):
    # Draw borders first
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=border_col, width=8, joint="round")
    # Draw cores
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=core_col, width=6, joint="round")
    # Draw terminal connection dots
    for p in points:
        draw.ellipse([p[0]-3, p[1]-3, p[0]+3, p[1]+3], fill=border_col)

def draw_vector_relay(draw_ctx):
    # Vector relay coordinates: Board bounds [788, 685, 917, 970]
    pcb_color = (14, 65, 92)      # Deep navy blue PCB
    casing_color = (18, 115, 186)  # Vibrant Songle blue
    terminal_color = (0, 95, 162)  # Screw terminal block blue
    copper_color = (196, 126, 50)  # Bronze/copper terminal
    dark_copper = (90, 50, 15)
    silver_color = (200, 200, 200)
    
    # A) PCB Board
    pcb_rect = [788, 685, 917, 970]
    draw_ctx.rounded_rectangle(pcb_rect, radius=8, fill=pcb_color)
    
    # Mounting holes in corners
    for cx, cy in [(794, 691), (911, 691), (794, 964), (911, 964)]:
        draw_ctx.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=silver_color, outline=(100, 100, 100))
        
    # B) Header Pins and Dupont Connectors (rotated pins at top)
    draw_ctx.rectangle([805, 682, 900, 694], fill=(30, 30, 30))
    for x in [815, 850, 886]:
        draw_ctx.rectangle([x - 5, 682, x + 5, 700], fill=(20, 20, 20))
        draw_ctx.rectangle([x - 2, 688, x + 2, 694], fill=(120, 120, 120))
        
    # Pin labels right-side up
    font_pins = get_font(10, bold=True)
    draw_ctx.text((815, 712), "VCC", fill="white", font=font_pins, anchor="mm")
    draw_ctx.text((850, 712), "IN", fill="white", font=font_pins, anchor="mm")
    draw_ctx.text((886, 712), "GND", fill="white", font=font_pins, anchor="mm")
    
    # C) Small SMD Components on the left of the board
    # Power LED (PWR)
    draw_ctx.rectangle([793, 735, 799, 743], fill=silver_color)
    draw_ctx.rectangle([794, 737, 798, 741], fill=(230, 30, 30)) # Red LED
    font_tiny = get_font(7)
    draw_ctx.text((796, 748), "PWR", fill=(180, 180, 180), font=font_tiny, anchor="mm")
    
    # Status LED (ACT)
    draw_ctx.rectangle([793, 760, 799, 768], fill=silver_color)
    draw_ctx.rectangle([794, 762, 798, 766], fill=(30, 230, 30)) # Green LED
    draw_ctx.text((796, 773), "ACT", fill=(180, 180, 180), font=font_tiny, anchor="mm")
    
    # D) Vibrant Blue Relay Casing
    casing_rect = [805, 732, 912, 875]
    draw_ctx.rectangle(casing_rect, fill=casing_color)
    draw_ctx.line([805, 732, 912, 732], fill=(80, 160, 230), width=2)
    draw_ctx.line([805, 732, 805, 875], fill=(80, 160, 230), width=2)
    draw_ctx.line([805, 875, 912, 875], fill=(10, 80, 140), width=2)
    draw_ctx.line([912, 732, 912, 875], fill=(10, 80, 140), width=2)
    
    # Text on casing
    font_casing_bold = get_font(12, bold=True)
    font_casing_small = get_font(8)
    draw_ctx.text((858, 748), "SONGLE", fill="white", font=font_casing_bold, anchor="mm")
    draw_ctx.line([815, 758, 902, 758], fill=(100, 170, 230), width=1)
    draw_ctx.text((858, 768), "SRD-05VDC-SL-C", fill="white", font=font_casing_small, anchor="mm")
    
    # Ratings text
    draw_ctx.text((858, 786), "10A 250VAC   10A 125VAC", fill=(220, 240, 255), font=font_casing_small, anchor="mm")
    draw_ctx.text((858, 802), "10A 30VDC    10A 28VDC", fill=(220, 240, 255), font=font_casing_small, anchor="mm")
    
    # Stylized coil and switch schematic symbol on the relay casing
    draw_ctx.rectangle([848, 825, 868, 835], outline=(200, 230, 255), width=1) # Coil box
    draw_ctx.line([843, 830, 848, 830], fill=(200, 230, 255), width=1)
    draw_ctx.line([868, 830, 873, 830], fill=(200, 230, 255), width=1)
    # Switch
    draw_ctx.ellipse([845, 848, 847, 850], fill="white")
    draw_ctx.ellipse([865, 848, 867, 850], fill="white")
    draw_ctx.line([847, 849, 862, 843], fill="white", width=1) # Switch lever
    
    # E) Terminal Labels (NO, COM, NC)
    font_term = get_font(10, bold=True)
    draw_ctx.text((823, 895), "NO", fill="white", font=font_term, anchor="mm")
    draw_ctx.text((859, 895), "COM", fill="white", font=font_term, anchor="mm")
    draw_ctx.text((895, 895), "NC", fill="white", font=font_term, anchor="mm")
    
    # F) Terminal Block (Bottom) - NO WIRES CONNECTED!
    draw_ctx.rectangle([805, 912, 912, 960], fill=terminal_color)
    # Slots/screws
    for tx in [823, 859, 895]:
        draw_ctx.ellipse([tx - 8, 936 - 8, tx + 8, 936 + 8], fill=copper_color, outline=dark_copper, width=1)
        draw_ctx.ellipse([tx - 5, 936 - 5, tx + 5, 936 + 5], fill=dark_copper)
        draw_ctx.line([tx - 4, 936 - 4, tx + 4, 936 + 4], fill=silver_color, width=2)
        
    # G) Label below the module
    font_label = get_font(13)
    draw_ctx.text((858, 988), "1-Channel Relay", fill="black", font=font_label, anchor="mm")

def rebuild_ambiente():
    print("Rebuilding Figura 44 (Nodo Ambiente) on top of original Fritzing image...")
    # Load the original Fritzing image backup
    img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")
    with Image.open(img_bak) as im:
        im = im.convert("RGBA")
        
        # 1. Paste unmirrored ESP32 at (342, 190)
        esp = Image.open(os.path.join(art_dir, "esp32_unmirrored.png"))
        im.paste(esp, (342, 190), mask=esp)
        
        # 2. Clear ONLY the relay area [780, 665, 930, 1005] with white
        draw = ImageDraw.Draw(im)
        draw.rectangle([780, 665, 930, 1005], fill=(255, 255, 255, 255))
        
        # 3. Draw vector relay at [788, 685, 917, 970]
        draw_vector_relay(draw)
        
        # 4. Draw straight wires from breadboard down to top relay pins (y=682)
        # VCC (x=815) -> bottom red rail (y=603)
        draw_wire(draw, [(815, 682), (815, 603)], red_core, red_border)
        # GND (x=886) -> bottom black rail (y=614)
        draw_wire(draw, [(886, 682), (886, 614)], black_core, black_border)
        # IN (x=850) -> ESP32 D26 (left side, row 9, x=326, y=363)
        draw_wire(draw, [(850, 682), (850, 363), (326, 363)], green_core, green_border)
        
        # Save to output
        dest_path = os.path.join(img_dir, "conexion_nodo_ambiente.png")
        im.convert("RGB").save(dest_path)
        print("Saved conexion_nodo_ambiente.png successfully.")

def rebuild_escritorio():
    print("Rebuilding Figura 45 (Nodo Escritorio) on top of original Fritzing image...")
    # Load the original Fritzing image backup
    img_bak = os.path.join(backup_dir, "conexion_nodo_escritorio_1779985482306.png")
    with Image.open(img_bak) as im:
        im = im.convert("RGBA")
        
        # 1. Paste unmirrored ESP32 at (342, 190)
        esp = Image.open(os.path.join(art_dir, "esp32_unmirrored.png"))
        im.paste(esp, (342, 190), mask=esp)
        
        # Save to output
        dest_path = os.path.join(img_dir, "conexion_nodo_escritorio.png")
        im.convert("RGB").save(dest_path)
        print("Saved conexion_nodo_escritorio.png successfully.")

def rebuild_puerta():
    print("Rebuilding Figura 46 (Nodo Puerta) on top of original Fritzing image...")
    # Load the original Fritzing image backup
    img_bak = os.path.join(backup_dir, "conexion_nodo_puerta_1779985504271.png")
    with Image.open(img_bak) as im:
        im = im.convert("RGBA")
        
        # 1. Paste unmirrored ESP32 at (342, 190)
        esp = Image.open(os.path.join(art_dir, "esp32_unmirrored.png"))
        im.paste(esp, (342, 190), mask=esp)
        
        # Save to output
        dest_path = os.path.join(img_dir, "conexion_nodo_puerta.png")
        im.convert("RGB").save(dest_path)
        print("Saved conexion_nodo_puerta.png successfully.")

if __name__ == "__main__":
    rebuild_ambiente()
    rebuild_escritorio()
    rebuild_puerta()
    print("Done generating all figures!")
