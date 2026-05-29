from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"

img_esc = os.path.join(backup_dir, "conexion_nodo_escritorio_1779985482306.png")
img_pue = os.path.join(backup_dir, "conexion_nodo_puerta_1779985504271.png")

if os.path.exists(img_esc):
    with Image.open(img_esc) as img:
        img.crop((342, 190, 682, 590)).save("escritorio_esp32_crop.png")
        print("Cropped escritorio ESP32.")

if os.path.exists(img_pue):
    with Image.open(img_pue) as img:
        img.crop((342, 190, 682, 590)).save("puerta_esp32_crop.png")
        print("Cropped puerta ESP32.")
