from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak_name = "conexion_nodo_ambiente_1779985459934.png"
img_bak = os.path.join(backup_dir, img_bak_name)

if os.path.exists(img_bak):
    with Image.open(img_bak) as img:
        # The ESP32 is at x=342 to 682, y=190 to 590
        # Let's crop the left pins area (x=342 to 400, y=190 to 590)
        img.crop((342, 190, 420, 590)).save("bak_esp32_left_pins.png")
        # Let's crop the right pins area (x=620 to 682, y=190 to 590)
        img.crop((600, 190, 682, 590)).save("bak_esp32_right_pins.png")
        print("Successfully saved original backup pin crops.")
else:
    print("Backup not found.")
