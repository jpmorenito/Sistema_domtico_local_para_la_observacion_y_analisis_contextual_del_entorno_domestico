import os
import shutil

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\Img"

files = {
    "conexion_nodo_ambiente.png": "conexion_nodo_ambiente_1779985459934.png",
    "conexion_nodo_escritorio.png": "conexion_nodo_escritorio_1779985482306.png",
    "conexion_nodo_puerta.png": "conexion_nodo_puerta_1779985504271.png"
}

print("Reverting all edited figures in Img/ back to your original backups...")
for dest_name, src_name in files.items():
    src_path = os.path.join(backup_dir, src_name)
    dest_path = os.path.join(img_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, dest_path)
        print(f"  Restored {dest_name} from backup {src_name}")
    else:
        print(f"  Backup {src_name} not found!")

print("All diagrams reverted to original state.")
