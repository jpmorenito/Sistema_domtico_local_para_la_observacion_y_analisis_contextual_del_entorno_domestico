from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Scan across the Red wire at y=640, x from 805 to 825
        print("Red wire cross section (x=805 to 825, y=640):")
        for x in range(805, 826):
            print(f"  x={x}: {im.getpixel((x, 640))}")
        
        # Scan across the Green wire at y=640, x from 840 to 860
        print("\nGreen wire cross section (x=840 to 860, y=640):")
        for x in range(840, 861):
            print(f"  x={x}: {im.getpixel((x, 640))}")

        # Scan across the Black wire at y=640, x from 875 to 895
        print("\nBlack wire cross section (x=875 to 895, y=640):")
        for x in range(875, 896):
            print(f"  x={x}: {im.getpixel((x, 640))}")
else:
    print("Backup image not found.")
