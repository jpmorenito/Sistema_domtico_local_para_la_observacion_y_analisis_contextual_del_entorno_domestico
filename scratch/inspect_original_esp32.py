from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak_name = "conexion_nodo_ambiente_1779985459934.png"
img_bak = os.path.join(backup_dir, img_bak_name)

if os.path.exists(img_bak):
    with Image.open(img_bak) as img:
        # Crop the ESP32 area
        esp_crop = img.crop((342, 190, 682, 590))
        esp_crop.save("original_esp32_crop.png")
        print("Cropped original ESP32 area successfully.")
else:
    print("Backup image not found.")
