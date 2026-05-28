from PIL import Image, ImageEnhance
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Let's crop the area of the relay containing the pin labels (usually near the top edge, y=675 to y=780, x=750 to x=880)
        relay_labels = im.crop((740, 665, 890, 780))
        # Save a high-contrast and magnified version
        relay_labels_large = relay_labels.resize((450, 345), Image.Resampling.LANCZOS)
        enhancer = ImageEnhance.Contrast(relay_labels_large)
        relay_enhanced = enhancer.enhance(2.0)
        relay_enhanced.save(os.path.join(backup_dir, "relay_labels.png"))
        print("Relay labels crop saved as relay_labels.png")
else:
    print("Backup image not found.")
