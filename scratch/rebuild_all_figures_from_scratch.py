import os
from PIL import Image, ImageDraw, ImageFont

# Define directories
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

# Wire Colors (Fritzing Style)
red_core = (215, 30, 30, 255)
red_border = (120, 0, 0, 255)

black_core = (65, 65, 65, 255)
black_border = (0, 0, 0, 255)

blue_core = (30, 115, 185, 255)
blue_border = (15, 55, 110, 255)

yellow_core = (235, 205, 30, 255)
yellow_border = (130, 115, 10, 255)

orange_core = (235, 120, 30, 255)
orange_border = (130, 60, 10, 255)

green_core = (40, 195, 70, 255)
green_border = (25, 135, 45, 255)

def draw_wire(draw, points, core_col, border_col):
    # Draw wire outline/border
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=border_col, width=8, joint="round")
    # Draw wire inner core
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=core_col, width=6, joint="round")
    # Draw connection dots at end points
    for p in [points[0], points[-1]]:
        draw.ellipse([p[0]-3, p[1]-3, p[0]+3, p[1]+3], fill=border_col)

def draw_vector_relay(draw_ctx):
    # Vector relay coordinates: Board bounds [788, 685, 917, 970]
    pcb_color = (14, 65, 92)      # Deep navy blue PCB
    casing_color = (18, 115, 186)  # Songle blue
    terminal_color = (0, 95, 162)  # Screw terminal block blue
    copper_color = (196, 126, 50)  # Bronze/copper terminal
    dark_copper = (90, 50, 15)
    silver_color = (200, 200, 200)
    
    # A) PCB Board
    pcb_rect = [788, 685, 917, 970]
    draw_ctx.rounded_rectangle(pcb_rect, radius=8, fill=pcb_color)
    
    # Mounting holes
    for cx, cy in [(794, 691), (911, 691), (794, 964), (911, 964)]:
        draw_ctx.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=silver_color, outline=(100, 100, 100))
        
    # B) Header Pins and Dupont Connectors (rotated pins at top)
    draw_ctx.rectangle([805, 682, 900, 694], fill=(30, 30, 30))
    for x in [815, 850, 886]:
        draw_ctx.rectangle([x - 5, 682, x + 5, 700], fill=(20, 20, 20))
        draw_ctx.rectangle([x - 2, 688, x + 2, 694], fill=(120, 120, 120))
        
    # Pin labels
    font_pins = get_font(10, bold=True)
    draw_ctx.text((815, 712), "VCC", fill="white", font=font_pins, anchor="mm")
    draw_ctx.text((850, 712), "IN", fill="white", font=font_pins, anchor="mm")
    draw_ctx.text((886, 712), "GND", fill="white", font=font_pins, anchor="mm")
    
    # C) Small SMD Components
    draw_ctx.rectangle([793, 735, 799, 743], fill=silver_color)
    draw_ctx.rectangle([794, 737, 798, 741], fill=(230, 30, 30)) # Red LED
    font_tiny = get_font(7)
    draw_ctx.text((796, 748), "PWR", fill=(180, 180, 180), font=font_tiny, anchor="mm")
    
    draw_ctx.rectangle([793, 760, 799, 768], fill=silver_color)
    draw_ctx.rectangle([794, 762, 798, 766], fill=(30, 230, 30)) # Green LED
    draw_ctx.text((796, 773), "ACT", fill=(180, 180, 180), font=font_tiny, anchor="mm")
    
    # D) Songle Casing
    casing_rect = [805, 732, 912, 875]
    draw_ctx.rectangle(casing_rect, fill=casing_color)
    draw_ctx.line([805, 732, 912, 732], fill=(80, 160, 230), width=2)
    draw_ctx.line([805, 732, 805, 875], fill=(80, 160, 230), width=2)
    draw_ctx.line([805, 875, 912, 875], fill=(10, 80, 140), width=2)
    draw_ctx.line([912, 732, 912, 875], fill=(10, 80, 140), width=2)
    
    font_casing_bold = get_font(12, bold=True)
    font_casing_small = get_font(8)
    draw_ctx.text((858, 748), "SONGLE", fill="white", font=font_casing_bold, anchor="mm")
    draw_ctx.line([815, 758, 902, 758], fill=(100, 170, 230), width=1)
    draw_ctx.text((858, 768), "SRD-05VDC-SL-C", fill="white", font=font_casing_small, anchor="mm")
    draw_ctx.text((858, 786), "10A 250VAC   10A 125VAC", fill=(220, 240, 255), font=font_casing_small, anchor="mm")
    draw_ctx.text((858, 802), "10A 30VDC    10A 28VDC", fill=(220, 240, 255), font=font_casing_small, anchor="mm")
    
    # Schematic symbol
    draw_ctx.rectangle([848, 825, 868, 835], outline=(200, 230, 255), width=1)
    draw_ctx.line([843, 830, 848, 830], fill=(200, 230, 255), width=1)
    draw_ctx.line([868, 830, 873, 830], fill=(200, 230, 255), width=1)
    draw_ctx.ellipse([845, 848, 847, 850], fill="white")
    draw_ctx.ellipse([865, 848, 867, 850], fill="white")
    draw_ctx.line([847, 849, 862, 843], fill="white", width=1)
    
    # E) Terminal Labels
    font_term = get_font(10, bold=True)
    draw_ctx.text((823, 895), "NO", fill="white", font=font_term, anchor="mm")
    draw_ctx.text((859, 895), "COM", fill="white", font=font_term, anchor="mm")
    draw_ctx.text((895, 895), "NC", fill="white", font=font_term, anchor="mm")
    
    # F) Screw Terminal Block (Bottom) - unconnected
    draw_ctx.rectangle([805, 912, 912, 960], fill=terminal_color)
    for tx in [823, 859, 895]:
        draw_ctx.ellipse([tx - 8, 936 - 8, tx + 8, 936 + 8], fill=copper_color, outline=dark_copper, width=1)
        draw_ctx.ellipse([tx - 5, 936 - 5, tx + 5, 936 + 5], fill=dark_copper)
        draw_ctx.line([tx - 4, 936 - 4, tx + 4, 936 + 4], fill=silver_color, width=2)

def make_clean_canvas():
    bg_p = os.path.join(art_dir, "clean_background.png")
    canvas = Image.open(bg_p).convert("RGBA")
    # Paste the unmirrored ESP32 WROOM-32 at (342, 190)
    esp = Image.open(os.path.join(art_dir, "esp32_unmirrored.png")).convert("RGBA")
    canvas.paste(esp, (342, 190), mask=esp)
    return canvas

def rebuild_ambiente():
    print("Generating Figure 44 (Nodo Ambiente) from scratch...")
    img = make_clean_canvas()
    draw = ImageDraw.Draw(img)
    
    # 1. Load and place LDR Sensor
    # clean_LDR_cropped.png: (709, 450) -> resize to (120, 76)
    ldr = Image.open(os.path.join(art_dir, "clean_LDR_cropped.png")).convert("RGBA")
    ldr = ldr.resize((120, 76), Image.Resampling.LANCZOS)
    img.paste(ldr, (240, 720), mask=ldr)
    
    # 2. Load and place Sound Sensor
    # clean_Sound_cropped.png: (798, 333) -> resize to (160, 67)
    sound = Image.open(os.path.join(art_dir, "clean_Sound_cropped.png")).convert("RGBA")
    sound = sound.resize((160, 67), Image.Resampling.LANCZOS)
    img.paste(sound, (440, 720), mask=sound)
    
    # 3. Load and place DHT11 Sensor
    # clean_DHT11_cropped.png: (365, 723) -> resize to (80, 158)
    dht = Image.open(os.path.join(art_dir, "clean_DHT11_cropped.png")).convert("RGBA")
    dht = dht.resize((80, 158), Image.Resampling.LANCZOS)
    img.paste(dht, (80, 680), mask=dht)
    
    # 4. Draw Vector Relay
    draw_vector_relay(draw)
    
    # 5. Draw ESP32 Power & Ground Connections
    # Left side:
    # GND (row 14, y=455) -> bottom black rail (GND, y=614, x=326)
    draw_wire(draw, [(326, 455), (326, 614)], black_core, black_border)
    # VIN (row 15, y=474) -> bottom red rail (5V, y=603, x=310)
    draw_wire(draw, [(342, 474), (310, 474), (310, 603)], red_core, red_border)
    # Right side:
    # GND (row 14, y=455) -> top black rail (GND, y=153, x=696)
    draw_wire(draw, [(696, 455), (696, 153)], black_core, black_border)
    # 3V3 (row 15, y=474) -> top red rail (3V3, y=142, x=715)
    draw_wire(draw, [(682, 474), (715, 474), (715, 142)], red_core, red_border)
    
    # 6. Draw DHT11 connections (left)
    # VCC (pin x=115, y=680) -> top red rail (y=142)
    draw_wire(draw, [(115, 680), (115, 142)], red_core, red_border)
    # GND (pin x=152, y=680) -> top black rail (y=153)
    draw_wire(draw, [(152, 680), (152, 153)], black_core, black_border)
    # DATA (pin x=133, y=680) -> ESP32 D4 (right side, row 11, x=696, y=400)
    # Route: up to y=335, right to x=730, down to y=400, left to pin.
    draw_wire(draw, [(133, 680), (133, 335), (730, 335), (730, 400), (696, 400)], blue_core, blue_border)
    
    # 7. Draw LDR connections (middle-left)
    # VCC (pin x=260, y=720) -> top red rail (y=142)
    draw_wire(draw, [(260, 720), (260, 142)], red_core, red_border)
    # GND (pin x=300, y=720) -> top black rail (y=153)
    draw_wire(draw, [(300, 720), (300, 153)], black_core, black_border)
    # SIG (pin x=280, y=720) -> ESP32 D32 (left side, row 6, x=326, y=308)
    draw_wire(draw, [(280, 720), (280, 308), (326, 308)], yellow_core, yellow_border)
    
    # 8. Draw Sound Sensor connections (middle-right)
    # VCC (pin x=460, y=720) -> bottom red rail (y=603)
    draw_wire(draw, [(460, 720), (460, 603)], red_core, red_border)
    # GND (pin x=500, y=720) -> bottom black rail (y=614)
    draw_wire(draw, [(500, 720), (500, 614)], black_core, black_border)
    # OUT (pin x=480, y=720) -> ESP32 D27 (left side, row 10, x=326, y=381)
    draw_wire(draw, [(480, 720), (480, 381), (326, 381)], orange_core, orange_border)
    
    # 9. Draw Relay connections (right)
    # VCC (x=815, y=682) -> bottom red rail (y=603)
    draw_wire(draw, [(815, 682), (815, 603)], red_core, red_border)
    # GND (x=886, y=682) -> bottom black rail (y=614)
    draw_wire(draw, [(886, 682), (886, 614)], black_core, black_border)
    # IN (x=850, y=682) -> ESP32 D26 (left side, row 9, x=326, y=363)
    # Route: up to y=363, left all the way to x=326
    draw_wire(draw, [(850, 682), (850, 363), (326, 363)], green_core, green_border)
    
    # Add Text Labels
    font_labels = get_font(14)
    draw.text((120, 850), "Sensor DHT11", fill="black", font=font_labels, anchor="mm")
    draw.text((300, 810), "Fotorresistor LDR", fill="black", font=font_labels, anchor="mm")
    draw.text((520, 800), "Sensor de Sonido", fill="black", font=font_labels, anchor="mm")
    draw.text((858, 988), "Módulo Relé (1-Canal)", fill="black", font=get_font(13), anchor="mm")
    
    dest_path = os.path.join(img_dir, "conexion_nodo_ambiente.png")
    img.convert("RGB").save(dest_path)
    print("Saved conexion_nodo_ambiente.png successfully.")

def rebuild_escritorio():
    print("Generating Figure 45 (Nodo Escritorio) from scratch...")
    img = make_clean_canvas()
    draw = ImageDraw.Draw(img)
    
    # 1. Load and place Radar LD2410
    # clean_Radar_cropped.png: (307, 271) -> resize to (120, 106)
    radar = Image.open(os.path.join(art_dir, "clean_Radar_cropped.png")).convert("RGBA")
    radar = radar.resize((120, 106), Image.Resampling.LANCZOS)
    img.paste(radar, (120, 700), mask=radar)
    
    # 2. Load and place Laser Diode
    # clean_Laser_cropped.png: (481, 674) -> resize to (100, 140)
    laser = Image.open(os.path.join(art_dir, "clean_Laser_cropped.png")).convert("RGBA")
    laser = laser.resize((100, 140), Image.Resampling.LANCZOS)
    img.paste(laser, (500, 680), mask=laser)
    
    # 3. Draw ESP32 Power & Ground Connections
    # Left side:
    draw_wire(draw, [(326, 455), (326, 614)], black_core, black_border)
    draw_wire(draw, [(342, 474), (310, 474), (310, 603)], red_core, red_border)
    # Right side:
    draw_wire(draw, [(696, 455), (696, 153)], black_core, black_border)
    draw_wire(draw, [(682, 474), (715, 474), (715, 142)], red_core, red_border)
    
    # 4. Draw Radar Connections (VCC, GND, TX, RX)
    # VCC (pin x=140, y=700) -> bottom red rail (y=603)
    draw_wire(draw, [(140, 700), (140, 603)], red_core, red_border)
    # GND (pin x=200, y=700) -> bottom black rail (y=614)
    draw_wire(draw, [(200, 700), (200, 614)], black_core, black_border)
    # TX (pin x=160, y=700) -> ESP32 RX2 (right side, row 10, x=696, y=381)
    # Route: up to y=320, right to x=730, down to y=381, left to pin.
    draw_wire(draw, [(160, 700), (160, 320), (730, 320), (730, 381), (696, 381)], green_core, green_border)
    # RX (pin x=180, y=700) -> ESP32 TX2 (right side, row 9, x=696, y=363)
    # Route: up to y=340, right to x=750, down to y=363, left to pin.
    draw_wire(draw, [(180, 700), (180, 340), (750, 340), (750, 363), (696, 363)], yellow_core, yellow_border)
    
    # 5. Draw Laser Connections (ONLY SIG and GND - NO VCC!)
    # SIG (pin x=520, y=680) -> ESP32 D12 (left side, row 12, x=326, y=418)
    # Route: up to y=418, left to x=326
    draw_wire(draw, [(520, 680), (520, 418), (326, 418)], blue_core, blue_border)
    # GND (pin x=550, y=680) -> bottom black rail (y=614)
    draw_wire(draw, [(550, 680), (550, 614)], black_core, black_border)
    
    # Add Text Labels
    font_labels = get_font(14)
    draw.text((180, 820), "Radar LD2410", fill="black", font=font_labels, anchor="mm")
    draw.text((550, 840), "Diodo Láser", fill="black", font=font_labels, anchor="mm")
    
    dest_path = os.path.join(img_dir, "conexion_nodo_escritorio.png")
    img.convert("RGB").save(dest_path)
    print("Saved conexion_nodo_escritorio.png successfully.")

def rebuild_puerta():
    print("Generating Figure 46 (Nodo Puerta) from scratch...")
    img = make_clean_canvas()
    draw = ImageDraw.Draw(img)
    
    # 1. Load and place Reed Sensor (Magnetic switch)
    # clean_Reed_cropped.png: (479, 443) -> resize to (120, 111)
    reed = Image.open(os.path.join(art_dir, "clean_Reed_cropped.png")).convert("RGBA")
    reed = reed.resize((120, 111), Image.Resampling.LANCZOS)
    img.paste(reed, (450, 700), mask=reed)
    
    # 2. Draw ESP32 Power & Ground Connections
    # Left side:
    draw_wire(draw, [(326, 455), (326, 614)], black_core, black_border)
    draw_wire(draw, [(342, 474), (310, 474), (310, 603)], red_core, red_border)
    # Right side:
    draw_wire(draw, [(696, 455), (696, 153)], black_core, black_border)
    draw_wire(draw, [(682, 474), (715, 474), (715, 142)], red_core, red_border)
    
    # 3. Draw Reed Switch Connections (Two pins, no polarity, no VCC!)
    # Terminal 1 (pin x=480, y=700) -> ESP32 D4 (right side, row 11, x=696, y=400)
    # Route: up to y=350, right to x=730, down to y=400, left to pin.
    draw_wire(draw, [(480, 700), (480, 350), (730, 350), (730, 400), (696, 400)], blue_core, blue_border)
    # Terminal 2 (pin x=520, y=700) -> bottom black rail (y=614)
    draw_wire(draw, [(520, 700), (520, 614)], black_core, black_border)
    
    # Add Text Labels
    font_labels = get_font(14)
    draw.text((510, 830), "Sensor Magnético Reed", fill="black", font=font_labels, anchor="mm")
    
    dest_path = os.path.join(img_dir, "conexion_nodo_puerta.png")
    img.convert("RGB").save(dest_path)
    print("Saved conexion_nodo_puerta.png successfully.")

if __name__ == "__main__":
    rebuild_ambiente()
    rebuild_escritorio()
    rebuild_puerta()
    print("All figures successfully reconstructed from scratch!")
