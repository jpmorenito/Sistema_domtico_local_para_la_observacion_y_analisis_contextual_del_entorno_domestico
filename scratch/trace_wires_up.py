from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # We trace the wires from y=610 upwards. Wires on a breadboard might go vertically, then turn.
        # Let's print out a grid of pixel colors in the region x=780 to 910, y=550 to 615 to see where the wires land.
        for x_start, name in [(814, "Left Wire (Red)"), (850, "Middle Wire (Green)"), (885, "Right Wire (Black)")]:
            print(f"\nTrace {name} above y=610:")
            # We look for the wire's color in rows y=610 down to y=500 (going up, smaller y)
            # Red color: high R, low G/B
            # Green color: high G, low R/B
            # Black/Dark: low R, G, B
            curr_x = x_start
            for y in range(610, 500, -10):
                # Search locally for the wire color
                found = []
                for dx in range(-15, 16):
                    x = curr_x + dx
                    if 0 <= x < im.width:
                        r, g, b, *a = im.getpixel((x, y))
                        is_gray = abs(r - g) < 15 and abs(r - b) < 15 and abs(g - b) < 15
                        # We want to match the wire color
                        if name == "Left Wire (Red)":
                            match = (r > 150 and g < 100 and b < 100)
                        elif name == "Middle Wire (Green)":
                            match = (g > 150 and r < 120 and b < 120)
                        else: # Black
                            match = (r < 80 and g < 80 and b < 80)
                        if match:
                            found.append(x)
                if found:
                    curr_x = sum(found) // len(found)
                    print(f"  y={y}: x={curr_x}")
                else:
                    print(f"  y={y}: lost wire")
                    break
else:
    print("Backup image not found.")
