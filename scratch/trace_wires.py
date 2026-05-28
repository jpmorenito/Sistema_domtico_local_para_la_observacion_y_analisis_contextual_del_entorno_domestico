from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Trace coordinates around y=610 to y=670 for the three columns
        for name, x_start in [("Left Wire", 815), ("Middle Wire", 850), ("Right Wire", 886)]:
            print(f"\nTracing {name} starting near x={x_start}:")
            for y in range(610, 675, 5):
                # Search locally for the wire color
                # Left is Red, Middle is Green, Right is Black
                found = []
                for dx in range(-15, 16):
                    x = x_start + dx
                    r, g, b, *a = im.getpixel((x, y))
                    is_gray = abs(r - g) < 15 and abs(r - b) < 15 and abs(g - b) < 15
                    if not (r > 240 and g > 240 and b > 240) and not (is_gray and r > 100):
                        found.append((x, (r, g, b)))
                if found:
                    avg_x = sum(x for x, c in found) / len(found)
                    avg_c = (int(sum(c[0] for x, c in found)/len(found)),
                             int(sum(c[1] for x, c in found)/len(found)),
                             int(sum(c[2] for x, c in found)/len(found)))
                    print(f"  y={y}: x={avg_x:.1f}, color={avg_c}")
else:
    print("Backup image not found.")
