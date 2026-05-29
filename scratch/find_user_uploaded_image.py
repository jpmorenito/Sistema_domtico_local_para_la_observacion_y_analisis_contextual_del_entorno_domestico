import os
import time

search_dirs = [
    r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8",
    os.path.join(r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8", "artifacts"),
    os.path.join(r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8", ".tempmediaStorage"),
    r"c:\Users\jacob\Downloads\TFG\Documento final"
]

now = time.time()
print("Searching for recently created images (within last 10 minutes):")

found = []
for d in search_dirs:
    if os.path.exists(d):
        for root, subdirs, files in os.walk(d):
            # Avoid traversing deep into system folders
            if ".system_generated" in root or ".git" in root or ".esphome" in root:
                continue
            for f in files:
                if f.lower().endswith((".png", ".jpg", ".jpeg")):
                    p = os.path.join(root, f)
                    try:
                        mtime = os.path.getmtime(p)
                        # Modified in the last 10 minutes (600 seconds)
                        if now - mtime < 600:
                            found.append((p, mtime))
                    except Exception:
                        pass

# Sort by modification time (newest first)
found.sort(key=lambda x: x[1], reverse=True)
for p, mtime in found:
    print(f"Path: {p} | ModTime: {time.ctime(mtime)}")
