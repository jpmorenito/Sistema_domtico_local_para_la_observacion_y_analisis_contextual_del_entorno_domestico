from PIL import Image
import os

img_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\Img"
backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"

img_curr = os.path.join(img_dir, "conexion_nodo_escritorio.png")
img_bak = os.path.join(backup_dir, "conexion_nodo_escritorio_1779985482306.png")

print(f"Current: exists={os.path.exists(img_curr)}, size={os.path.getsize(img_curr) if os.path.exists(img_curr) else 0}")
print(f"Backup: exists={os.path.exists(img_bak)}, size={os.path.getsize(img_bak) if os.path.exists(img_bak) else 0}")

# Let's inspect pixel colors in current image at (748, 718) to verify if the red wire is there
if os.path.exists(img_curr):
    with Image.open(img_curr) as im:
        print("Current image size:", im.size)
        # Check pixel color around (748, 718)
        print("Current color at (748, 718):", im.getpixel((748, 718)))

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        print("Backup image size:", im.size)
        print("Backup color at (748, 718):", im.getpixel((748, 718)))
