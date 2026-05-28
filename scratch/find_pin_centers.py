from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
crop_path = os.path.join(backup_dir, "relay_bottom_crop.png")

if os.path.exists(crop_path):
    with Image.open(crop_path) as im:
        width, height = im.size
        # The crop is 130x100, x_orig = x_crop + 790, y_orig = y_crop + 890
        # Let's print out the pixel colors for y_crop = 50 to 90 (y_orig = 940 to 980)
        # to find the pins.
        # Let's scan y_crop and look for metal pins: they are usually silver/gray (e.g. 150-180)
        # with dark housing.
        # Let's print rows that have distinctive pin patterns.
        print("Scanning rows in relay_bottom_crop:")
        for y in range(40, 95, 5):
            row_data = []
            for x in range(width):
                r, g, b, *a = im.getpixel((x, y))
                # Let's format as hex color
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                row_data.append((x, hex_color, (r,g,b)))
            # Let's filter out rows that are just solid green board or white background
            # The PCB board is green (e.g. R=0-50, G=80-150, B=50-100) or dark.
            # White background is R>240, G>240, B>240.
            # Let's find coordinates that are not white and not green.
            non_green_white = []
            for x, hex_col, rgb in row_data:
                r, g, b = rgb
                is_white = r > 240 and g > 240 and b > 240
                is_green = g > r + 30 and g > b + 20 and g > 60
                is_gray_board = abs(r-g) < 15 and abs(r-b) < 15 and g > 100
                if not is_white and not is_green and not is_gray_board:
                    non_green_white.append((x, hex_col))
            if non_green_white:
                # Group consecutive x
                groups = []
                current = []
                for x, col in non_green_white:
                    if not current or x == current[-1][0] + 1:
                        current.append((x, col))
                    else:
                        groups.append(current)
                        current = [(x, col)]
                if current:
                    groups.append(current)
                
                group_strs = []
                for g in groups:
                    avg_x = sum(x for x, c in g) / len(g)
                    avg_x_orig = avg_x + 790
                    group_strs.append(f"x_crop={int(avg_x)} (x_orig={int(avg_x_orig)}) [{g[0][1]}]")
                print(f"y_crop={y} (y_orig={890+y}):", ", ".join(group_strs))
else:
    print("Crop not found.")
