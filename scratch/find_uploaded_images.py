import os
import glob
import time

brain_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"

# Search for all image files recursively in brain_dir
image_extensions = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.img"]
found_files = []

for ext in image_extensions:
    # Recursively find all files with extension
    pattern = os.path.join(brain_dir, "**", ext)
    for f in glob.glob(pattern, recursive=True):
        mtime = os.path.getmtime(f)
        found_files.append((f, mtime, os.path.getsize(f)))

# Sort by modification time descending
found_files.sort(key=lambda x: x[1], reverse=True)

print("Found image files (sorted by modification time, newest first):")
for f, mtime, size in found_files[:20]:
    t_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
    print(f"  {f} | Size: {size} bytes | Modified: {t_str}")
