from PIL import Image, ImageDraw, ImageFont
import os

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

def draw_rotated_text(img, text, position, angle, font, fill_color):
    txt_img = Image.new("RGBA", (100, 30), (0, 0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_img)
    txt_draw.text((50, 15), text, fill=fill_color, font=font, anchor="mm")
    rotated = txt_img.rotate(angle, expand=True)
    w, h = rotated.size
    px = int(position[0] - w/2)
    py = int(position[1] - h/2)
    img.paste(rotated, (px, py), mask=rotated)

# Load cropped ESP32
esp = Image.open("original_esp32_crop.png").convert("RGBA")
draw = ImageDraw.Draw(esp)

# Cover left labels: x from 90 to 101, y from 45 to 325
draw.rectangle([90, 45, 101, 325], fill=(24, 24, 24, 255))

# Cover right labels: x from 239 to 250, y from 45 to 325
draw.rectangle([239, 45, 250, 325], fill=(24, 24, 24, 255))

# Cover bottom-left button label
draw.rectangle([125, 350, 142, 375], fill=(24, 24, 24, 255))

# Cover bottom-right button label
draw.rectangle([198, 350, 215, 375], fill=(24, 24, 24, 255))

# Pin labels
left_labels = ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25", "D26", "D27", "D14", "D12", "D13", "GND", "VIN"]
right_labels = ["D23", "D22", "TX0", "RX0", "D21", "D19", "D18", "D5", "TX2", "RX2", "D4", "D2", "D15", "GND", "3V3"]

# Row coordinates in the crop
y_coords = [52, 71, 90, 108, 127, 145, 163, 182, 200, 219, 237, 256, 274, 293, 311]

font_label = get_font(7, bold=True)
font_btn = get_font(6, bold=True)

# Draw left labels (rotated 270 degrees to read upwards/along the board)
for label, y in zip(left_labels, y_coords):
    draw_rotated_text(esp, label, (95, y), 270, font_label, (230, 230, 230, 255))

# Draw right labels (rotated 90 degrees)
for label, y in zip(right_labels, y_coords):
    draw_rotated_text(esp, label, (245, y), 90, font_label, (230, 230, 230, 255))

# Draw EN next to left button
draw_rotated_text(esp, "EN", (133, 362), 270, font_btn, (180, 180, 180, 255))

# Draw BOOT next to right button
draw_rotated_text(esp, "BOOT", (206, 362), 270, font_btn, (180, 180, 180, 255))

esp.save("test_esp32_labeled.png")
print("Saved test_esp32_labeled.png")
