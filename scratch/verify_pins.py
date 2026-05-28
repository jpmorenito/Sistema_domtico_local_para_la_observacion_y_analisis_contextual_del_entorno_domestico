from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Check colors at y=965 to 975 for x=818, 852, 886
        for x in [818, 852, 886]:
            print(f"\nChecking coordinates around pin x={x}:")
            for y in range(960, 980, 2):
                print(f"  y={y}: {im.getpixel((x, y))}")
else:
    print("Backup image not found.")
