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

# Restore original
shutil.copy(img_bak, img_dest)

with Image.open(img_dest) as img:
    draw = ImageDraw.Draw(img)
    bg_color = img.getpixel((930, 640))
    
    # Remove header
    draw.rectangle([0, 0, 1024, 140], fill="white")
    
    # Crop relay (x=785-920, y=672-975)
    relay_crop = img.crop((785, 672, 920, 975))
    rotated = relay_crop.rotate(180)
    r_draw = ImageDraw.Draw(rotated)
    cw, ch = rotated.size  # 135 x 303
    
    # Sample multiple points on the ORIGINAL (non-rotated) crop to get accurate colors
    # In original: top is screw terminals, middle is casing, bottom is PCB+pins
    # After rotation: top is PCB+pins, middle is casing, bottom is screw terminals
    
    # Sample from the original crop (before rotation) for accuracy
    orig_draw = ImageDraw.Draw(relay_crop)
    
    # PCB color from original (near pin labels at the bottom of original, y~280)
    pcb_samples = [relay_crop.getpixel((x, 280)) for x in [30, 50, 70, 90, 110]]
    print("PCB samples (original bottom):", pcb_samples)
    
    # Casing color from original center
    casing_samples = [relay_crop.getpixel((x, 150)) for x in [20, 40, 67, 90, 110]]
    print("Casing samples (original center):", casing_samples)
    
    # Edge color of casing
    edge_samples = [relay_crop.getpixel((x, 120)) for x in [10, 12, 14]]
    print("Edge samples:", edge_samples)
    
    # Now work on the rotated version
    # After 180 rotation, what was at bottom is now at top
    
    # A) y=0-18: old "1-Channel Relay" label → canvas bg
    r_draw.rectangle([0, 0, cw, 18], fill=bg_color)
    
    # B) y=18-55: PCB area with pin labels
    # Use the actual PCB color sampled
    pcb_blue = (42, 134, 201)  # This was the PCB color I found earlier
    # Actually let me sample directly from the rotated image at a safe spot
    pcb_at_top = rotated.getpixel((67, 35))
    print("PCB color in rotated at (67,35):", pcb_at_top)
    
    # Cover pin label area
    r_draw.rectangle([5, 18, cw-5, 55], fill=pcb_at_top)
    font_pins = get_font(11)
    r_draw.text((22, 30), "VCC", fill="white", font=font_pins)
    r_draw.text((60, 30), "IN", fill="white", font=font_pins)
    r_draw.text((90, 30), "GND", fill="white", font=font_pins)
    
    # C) y=55-245: ENTIRE casing - be aggressive, cover EVERYTHING
    # Sample the background casing color at various points
    casing_bg = rotated.getpixel((67, 80))
    print("Casing bg at (67,80):", casing_bg)
    
    # Cover from the very left edge to right edge of the casing
    # But we need to preserve the outer dark border of the PCB
    # The outer PCB edge is about 5px on each side
    r_draw.rectangle([6, 55, cw-6, 245], fill=casing_bg)
    
    # Draw inner relay box
    inner_box_color = (100, 160, 220)
    r_draw.rectangle([35, 95, 110, 200], fill=inner_box_color)
    
    # Draw labels on the casing
    font_casing = get_font(14)
    font_sub = get_font(11)
    r_draw.text((48, 120), "Relay", fill="white", font=font_casing)
    r_draw.text((42, 140), "Module", fill="white", font=font_casing)
    r_draw.text((50, 175), "5V DC", fill="white", font=font_sub)
    
    # D) y=245-290: terminal area - labels NO/COM/NC upside down
    # Cover just the label text, not the actual terminals
    terminal_bg = rotated.getpixel((67, 280))
    print("Terminal label bg at (67,280):", terminal_bg)
    r_draw.rectangle([5, 272, cw-5, 290], fill=bg_color)
    font_term = get_font(9)
    r_draw.text((18, 275), "NO", fill="black", font=font_term)
    r_draw.text((53, 275), "COM", fill="black", font=font_term)
    r_draw.text((98, 275), "NC", fill="black", font=font_term)
    
    # E) Bottom wire stubs
    r_draw.rectangle([0, 290, cw, ch], fill=(255,255,255))
    
    # Paste back
    img.paste(rotated, (785, 672))
    
    # Label below
    draw.rectangle([785, 975, 920, 1000], fill=(255,255,255))
    font_label = get_font(13)
    draw.text((798, 978), "1-Channel Relay", fill="black", font=font_label)
    
    img.save(img_dest)
    print("DONE")
