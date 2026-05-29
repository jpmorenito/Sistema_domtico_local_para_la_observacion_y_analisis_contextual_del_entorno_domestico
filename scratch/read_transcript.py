import os
from PIL import Image
import numpy as np

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_escritorio_1779985482306.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as img:
        arr = np.array(img.convert("RGB"))
        # We search for red pixels (R > 180, G < 100, B < 100) starting from y = 803 near x = 619
        # and going upwards
        curr_x = 619
        print("Tracing red wire of laser:")
        for y in range(803, 580, -2):
            found_x = []
            for dx in range(-15, 16):
                x = curr_x + dx
                if 0 <= x < img.width:
                    r, g, b = arr[y, x]
                    if r > 150 and g < 100 and b < 100:
                        found_x.append(x)
            if found_x:
                curr_x = int(sum(found_x) / len(found_x))
                print(f"  y={y}: x={curr_x}, color={arr[y, curr_x]}")
            else:
                print(f"  y={y}: wire ended or turned")
                break
else:
    print("Backup not found")
