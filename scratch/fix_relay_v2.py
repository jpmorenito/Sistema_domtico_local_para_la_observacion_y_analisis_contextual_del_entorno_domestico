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

# Step 1: Restore original completely
shutil.copy(img_bak, img_dest)

with Image.open(img_dest) as img:
    draw = ImageDraw.Draw(img)
    bg_color = img.getpixel((930, 640))
    
    # Remove header text
    draw.rectangle([0, 0, 1024, 140], fill="white")
    
    # Crop the relay (x=785-920, y=672-975)
    relay_crop = img.crop((785, 672, 920, 975))
    rotated = relay_crop.rotate(180)
    r_draw = ImageDraw.Draw(rotated)
    cw, ch = rotated.size  # 135 x 303
    
    # Sample real colors from the rotated crop to match backgrounds
    # PCB board color (dark blue-green near the pin headers)
    pcb_color = rotated.getpixel((67, 45))
    # Light blue casing color (center of relay box)
    casing_color = rotated.getpixel((67, 150))
    # Dark blue edge of casing
    edge_color = rotated.getpixel((15, 150))
    
    print(f"PCB color: {pcb_color}, Casing color: {casing_color}, Edge color: {edge_color}")
    
    # A) Top area - old "1-Channel Relay" label now upside down → canvas bg
    r_draw.rectangle([0, 0, cw, 18], fill=bg_color)
    
    # B) Pin label area - old VCC/IN/GND now upside down → PCB color + redraw
    r_draw.rectangle([5, 18, cw-5, 52], fill=pcb_color)
    font_pins = get_font(11)
    r_draw.text((22, 28), "VCC", fill="white", font=font_pins)
    r_draw.text((60, 28), "IN", fill="white", font=font_pins)
    r_draw.text((90, 28), "GND", fill="white", font=font_pins)
    
    # C) ENTIRE casing face - cover EVERYTHING from left edge to right edge
    # This covers the upside-down "SONGLE", "RELAY MODULE" vertical text, logo, everything
    # The casing spans roughly y=62 to y=238 in the rotated crop
    # Cover the full width of the casing (x=8 to x=127)
    r_draw.rectangle([8, 62, 127, 238], fill=casing_color)
    
    # Draw clean right-side-up labels on casing
    font_casing = get_font(15)
    font_sub = get_font(11)
    
    # Draw the blue inner box outline (the actual relay component)
    inner_blue = (60, 120, 180)
    r_draw.rectangle([42, 100, 105, 195], outline=inner_blue, width=2)
    r_draw.rectangle([44, 102, 103, 193], fill=(100, 160, 220))
    
    # Text on the inner box
    r_draw.text((52, 120), "Relay", fill="white", font=font_casing)
    r_draw.text((45, 140), "Module", fill="white", font=font_casing)
    r_draw.text((55, 175), "5V DC", fill="white", font=font_sub)
    
    # D) Bottom terminal labels - NO/COM/NC are now upside down
    # Cover the label area and redraw
    r_draw.rectangle([5, 270, cw-5, 290], fill=bg_color)
    font_term = get_font(9)
    r_draw.text((18, 273), "NO", fill="black", font=font_term)
    r_draw.text((53, 273), "COM", fill="black", font=font_term)
    r_draw.text((98, 273), "NC", fill="black", font=font_term)
    
    # E) Bottom wire stubs - clean white below terminals
    r_draw.rectangle([0, 290, cw, ch], fill=(255, 255, 255))
    
    # Paste back
    img.paste(rotated, (785, 672))
    
    # Clean text area below relay and write label
    draw.rectangle([785, 975, 920, 1000], fill=(255,255,255))
    font_label = get_font(13)
    draw.text((798, 978), "1-Channel Relay", fill="black", font=font_label)
    
    img.save(img_dest)
    print("DONE - relay fully cleaned and relabeled")
