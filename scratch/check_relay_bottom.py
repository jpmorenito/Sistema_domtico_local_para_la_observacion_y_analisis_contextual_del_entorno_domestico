from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Let's crop the bottom area of the relay (x=790 to 920, y=850 to 990)
        # and search for non-white/non-gray elements representing pins or labels
        # Let's print out what colors we find at different y coordinates
        print("Relay bottom scan (x=790 to 920, y=850 to 990):")
        for y in range(850, 990, 10):
            found_cols = []
            for x in range(790, 920):
                r, g, b, *a = im.getpixel((x, y))
                # Check for colors that are not white/light gray
                is_gray = abs(r - g) < 15 and abs(r - b) < 15 and abs(g - b) < 15
                if not (r > 240 and g > 240 and b > 240) and not (is_gray and r > 100):
                    found_cols.append(x)
            if found_cols:
                # Print summary
                print(f"y={y}: colored pixels at x={found_cols[0]} to {found_cols[-1]} (count={len(found_cols)})")
else:
    print("Backup image not found.")
