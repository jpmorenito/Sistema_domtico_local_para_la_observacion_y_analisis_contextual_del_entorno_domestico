import os

tfg_path = "c:/Users/jacob/Downloads/TFG"
image_extensions = ('.png', '.jpg', '.jpeg', '.mp4')

print(f"Recursively searching for images in {tfg_path}...")
found_files = []

for root, dirs, files in os.walk(tfg_path):
    # Skip git and cache folders
    if '.git' in dirs:
        dirs.remove('.git')
    if '.gemini' in dirs:
        dirs.remove('.gemini')
    if 'Miktex' in root or 'AppData' in root:
        continue
        
    for file in files:
        if file.lower().endswith(image_extensions):
            full_path = os.path.join(root, file)
            # Make it relative for readability
            rel_path = os.path.relpath(full_path, tfg_path)
            found_files.append((rel_path, os.path.getsize(full_path)))

print(f"Total images/videos found: {len(found_files)}")
for path, size in sorted(found_files):
    print(f"- {path} ({size} bytes)")
