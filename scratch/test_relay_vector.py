from PIL import Image, ImageDraw, ImageFont
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
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

# Create a blank image representing the relay region (width=135, height=303) plus some padding
test_img = Image.new("RGB", (200, 350), (255, 255, 255))
draw = ImageDraw.Draw(test_img)

# We will draw the relay with relative coordinates inside this test image to verify its design
# The relay PCB coordinates in the original image were x: 785 to 920, y: 672 to 975.
# Let's map x to x - 785 + 30, and y to y - 672 + 30 in our test image.

dx = 30 - 785
dy = 30 - 672

pcb_color = (14, 65, 92)     # Deep navy blue
casing_color = (18, 115, 186) # Vibrant relay blue
terminal_color = (0, 95, 162) # Screw terminal block blue
copper_color = (196, 126, 50)  # Bronze/copper terminal
dark_copper = (90, 50, 15)
silver_color = (200, 200, 200)

# 1. PCB Board
pcb_rect = [788 + dx, 685 + dy, 917 + dx, 970 + dy]
draw.rounded_rectangle(pcb_rect, radius=8, fill=pcb_color)

# Mounting holes
for cx, cy in [(794, 691), (911, 691), (794, 964), (911, 964)]:
    draw.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3], fill=silver_color, outline=(100, 100, 100))

# 2. Header Pins and Dupont Connectors (Top)
# Header base
draw.rectangle([805 + dx, 682 + dy, 900 + dx, 694 + dy], fill=(30, 30, 30))

# Red, Green, Black Dupont wires coming from top to pins
# In our test we just draw a short wire
draw.line([815 + dx, 0, 815 + dx, 688 + dy], fill=(214, 39, 40), width=4) # Red
draw.line([850 + dx, 0, 850 + dx, 688 + dy], fill=(44, 160, 44), width=4) # Green
draw.line([886 + dx, 0, 886 + dx, 688 + dy], fill=(30, 30, 30), width=4) # Black

# Dupont connector housings (black plastic housings)
for x in [815, 850, 886]:
    draw.rectangle([x + dx - 5, 682 + dy, x + dx + 5, 700 + dy], fill=(20, 20, 20))
    # Silver pin slot detail
    draw.rectangle([x + dx - 2, 688 + dy, x + dx + 2, 694 + dy], fill=(120, 120, 120))

# Pin labels
font_pins = get_font(10, bold=True)
draw.text((815 + dx, 712 + dy), "VCC", fill="white", font=font_pins, anchor="mm")
draw.text((850 + dx, 712 + dy), "IN", fill="white", font=font_pins, anchor="mm")
draw.text((886 + dx, 712 + dy), "GND", fill="white", font=font_pins, anchor="mm")

# 3. Small components on the left
# Power LED (PWR)
draw.rectangle([793 + dx, 735 + dy, 799 + dx, 743 + dy], fill=silver_color)
draw.rectangle([794 + dx, 737 + dy, 798 + dx, 741 + dy], fill=(230, 30, 30)) # Red LED
font_tiny = get_font(7)
draw.text((796 + dx, 748 + dy), "PWR", fill=(180, 180, 180), font=font_tiny, anchor="mm")

# Status LED (ACT)
draw.rectangle([793 + dx, 760 + dy, 799 + dx, 768 + dy], fill=silver_color)
draw.rectangle([794 + dx, 762 + dy, 798 + dx, 766 + dy], fill=(30, 230, 30)) # Green LED
draw.text((796 + dx, 773 + dy), "ACT", fill=(180, 180, 180), font=font_tiny, anchor="mm")

# 4. Blue Relay Casing
casing_rect = [805 + dx, 732 + dy, 912 + dx, 875 + dy]
draw.rectangle(casing_rect, fill=casing_color)
# 3D Highlight edges
draw.line([805 + dx, 732 + dy, 912 + dx, 732 + dy], fill=(80, 160, 230), width=2)
draw.line([805 + dx, 732 + dy, 805 + dx, 875 + dy], fill=(80, 160, 230), width=2)
draw.line([805 + dx, 875 + dy, 912 + dx, 875 + dy], fill=(10, 80, 140), width=2)
draw.line([912 + dx, 732 + dy, 912 + dx, 875 + dy], fill=(10, 80, 140), width=2)

# Text on casing
font_casing_bold = get_font(12, bold=True)
font_casing_small = get_font(8)
draw.text((858 + dx, 748 + dy), "SONGLE", fill="white", font=font_casing_bold, anchor="mm")
draw.line([815 + dx, 758 + dy, 902 + dx, 758 + dy], fill=(100, 170, 230), width=1)
draw.text((858 + dx, 768 + dy), "SRD-05VDC-SL-C", fill="white", font=font_casing_small, anchor="mm")

# Ratings text
draw.text((858 + dx, 786 + dy), "10A 250VAC   10A 125VAC", fill=(220, 240, 255), font=font_casing_small, anchor="mm")
draw.text((858 + dx, 802 + dy), "10A 30VDC    10A 28VDC", fill=(220, 240, 255), font=font_casing_small, anchor="mm")

# Stylized coil and switch schematic symbol on the relay casing
draw.rectangle([848 + dx, 825 + dy, 868 + dx, 835 + dy], outline=(200, 230, 255), width=1) # Coil box
draw.line([843 + dx, 830 + dy, 848 + dx, 830 + dy], fill=(200, 230, 255), width=1)
draw.line([868 + dx, 830 + dy, 873 + dx, 830 + dy], fill=(200, 230, 255), width=1)
# Switch
draw.ellipse([845 + dx, 848 + dy, 847 + dx, 850 + dy], fill="white")
draw.ellipse([865 + dx, 848 + dy, 867 + dx, 850 + dy], fill="white")
draw.line([847 + dx, 849 + dy, 862 + dx, 843 + dy], fill="white", width=1) # Switch lever

# 5. Terminal Labels (NO, COM, NC)
font_term = get_font(10, bold=True)
draw.text((823 + dx, 895 + dy), "NO", fill="white", font=font_term, anchor="mm")
draw.text((859 + dx, 895 + dy), "COM", fill="white", font=font_term, anchor="mm")
draw.text((895 + dx, 895 + dy), "NC", fill="white", font=font_term, anchor="mm")

# 6. Terminal Block (Bottom)
draw.rectangle([805 + dx, 912 + dy, 912 + dx, 960 + dy], fill=terminal_color)
# Slots/screws
for tx in [823, 859, 895]:
    # Copper circle
    draw.ellipse([tx + dx - 8, 936 + dy - 8, tx + dx + 8, 936 + dy + 8], fill=copper_color, outline=dark_copper, width=1)
    draw.ellipse([tx + dx - 5, 936 + dy - 5, tx + dx + 5, 936 + dy + 5], fill=dark_copper)
    # Screw flathead slot
    draw.line([tx + dx - 4, 936 + dy - 4, tx + dx + 4, 936 + dy + 4], fill=silver_color, width=2)

test_img.save(os.path.join(backup_dir, "relay_vector_test.png"))
print("Saved test image!")
