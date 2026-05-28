from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
crop_path = os.path.join(backup_dir, "relay_crop.png")

if os.path.exists(crop_path):
    with Image.open(crop_path) as im:
        width, height = im.size
        # The cropped region is (740, 600, 920, 950) in original
        # Let's check some rows to find wire colors.
        # Wires typically go down from the relay. The bottom of the relay module is around y=850.
        # Let's scan y-levels from 200 to 340 (corresponding to y=800 to 940 in original)
        # to find columns that have colored pixels (not white/gray background).
        print("Scanning rows in relay_crop (height=350, width=180) to find wires:")
        for y in range(0, height, 10):
            row_colors = []
            for x in range(width):
                r, g, b, *a = im.getpixel((x, y))
                # If color is not white (near 255) and not gray (r ~ g ~ b)
                is_gray = abs(r - g) < 15 and abs(r - b) < 15 and abs(g - b) < 15
                if not (r > 240 and g > 240 and b > 240) and not (is_gray and r > 100):
                    row_colors.append((x, (r, g, b)))
            if row_colors:
                # Group contiguous x coordinates
                groups = []
                current_group = []
                for x, col in row_colors:
                    if not current_group or x == current_group[-1][0] + 1:
                        current_group.append((x, col))
                    else:
                        groups.append(current_group)
                        current_group = [(x, col)]
                if current_group:
                    groups.append(current_group)
                
                group_info = []
                for g in groups:
                    avg_x = sum(x for x, col in g) / len(g)
                    # Average color
                    avg_r = int(sum(col[0] for x, col in g) / len(g))
                    avg_g = int(sum(col[1] for x, col in g) / len(g))
                    avg_b = int(sum(col[2] for x, col in g) / len(g))
                    group_info.append(f"x={int(avg_x)} color=({avg_r},{avg_g},{avg_b})")
                print(f"y_crop={y} (y_orig={600+y}):", ", ".join(group_info))
else:
    print("Cropped relay image not found.")
