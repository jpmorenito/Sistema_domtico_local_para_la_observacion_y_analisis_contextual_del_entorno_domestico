import os
from PIL import Image

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
bg_path = os.path.join(backup_dir, "artifacts", "clean_background.png")

if os.path.exists(bg_path):
    with Image.open(bg_path) as img:
        print(f"Format: {img.format}, Size: {img.size}, Mode: {img.mode}")
        # Let's save a copy to the workspace to make sure we can use it or inspect it
        img.save("clean_background_workspace.png")
        print("Saved clean_background_workspace.png to workspace.")
else:
    print("clean_background.png not found!")
