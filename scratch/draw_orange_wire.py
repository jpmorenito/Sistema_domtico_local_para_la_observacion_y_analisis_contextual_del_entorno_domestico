import os
from PIL import Image, ImageDraw, ImageFont

img_path = r"c:\Users\jacob\Downloads\TFG\Documento final\scratch\erased_wire.png"
dest_path = r"c:\Users\jacob\Downloads\TFG\Documento final\Img\conexion_nodo_ambiente.png"
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

def draw_wire(draw, points, core_col, border_col):
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=border_col, width=8, joint="round")
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=core_col, width=6, joint="round")
    for p in [points[0], points[-1]]:
        draw.ellipse([p[0]-3, p[1]-3, p[0]+3, p[1]+3], fill=border_col)

if os.path.exists(img_path):
    img = Image.open(img_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    
    orange_core = (235, 120, 30, 255)
    orange_border = (130, 60, 10, 255)
    
    # We erased from (215, 400) down to (299, 948).
    # Bottom point: (250, 940)
    # We want to route it to the top left of ESP32, e.g. (330, 220)
    # Let's route it up the left side and bend right.
    points = [
        (250, 940),
        (250, 220),
        (330, 220)
    ]
    draw_wire(draw, points, orange_core, orange_border)
    
    width, height = img.size
    
    # Redraw labels
    font_esp = get_font(32, bold=True)
    draw.text((width // 2, 40), "ESP32", fill="black", font=font_esp, anchor="mm")
    
    font_sensors = get_font(22, bold=True)
    draw.text((120, height - 250), "Sensor DHT11", fill="black", font=font_sensors, anchor="mm")
    draw.text((320, height - 20), "LDR", fill="black", font=font_sensors, anchor="mm")
    draw.text((width - 150, height - 20), "Relé", fill="black", font=font_sensors, anchor="mm")
    draw.text((width - 120, height - 430), "Big Sound", fill="black", font=font_sensors, anchor="mm")
    
    img.convert("RGB").save(dest_path)
    print("New wire drawn and labels applied.")
