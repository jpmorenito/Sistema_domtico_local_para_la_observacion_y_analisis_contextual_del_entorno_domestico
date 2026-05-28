from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Let's check where the Left (Red), Middle (Green), and Right (Black) wires terminate
        # The breadboard bottom row where they connect:
        # Left (Red) wire is at x=815
        # Middle (Green) wire is at x=850
        # Right (Black) wire is at x=885
        # Let's inspect the area from y=500 to y=610 for connections.
        # Wires go straight up to the breadboard.
        # Let's print out what other wires or pins are in the same columns (x=815, x=850, x=885)
        # on the breadboard (y=530 to 600) or ESP32.
        print("Left wire (Red) column (x=815) pixels from y=500 to y=600:")
        for y in range(500, 610, 10):
            print(f"  y={y}: {im.getpixel((815, y))}")

        print("\nMiddle wire (Green) column (x=850) pixels from y=500 to y=600:")
        for y in range(500, 610, 10):
            print(f"  y={y}: {im.getpixel((850, y))}")

        print("\nRight wire (Black) column (x=885) pixels from y=500 to y=600:")
        for y in range(500, 610, 10):
            print(f"  y={y}: {im.getpixel((885, y))}")
else:
    print("Backup image not found.")
