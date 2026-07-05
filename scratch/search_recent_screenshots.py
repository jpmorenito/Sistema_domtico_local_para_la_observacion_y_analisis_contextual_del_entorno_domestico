import os
import glob
import datetime

user_home = "C:/Users/jacob"
folders = [
    f"{user_home}/Pictures/Screenshots",
    f"{user_home}/Pictures",
    f"{user_home}/Desktop",
    f"{user_home}/Downloads"
]

print("Searching for recent image files in user folders...")
image_extensions = ('*.png', '*.jpg', '*.jpeg')

for folder in folders:
    if os.path.exists(folder):
        print(f"\nChecking folder: {folder}")
        found = []
        for ext in image_extensions:
            # We search recursively with depth 2
            pattern = os.path.join(folder, "**", ext)
            for path in glob.glob(pattern, recursive=True):
                # Only check files, skip TFG folder since we already scanned it
                if os.path.isfile(path) and "Downloads/TFG" not in path.replace("\\", "/"):
                    mtime = os.path.getmtime(path)
                    dt = datetime.datetime.fromtimestamp(mtime)
                    # We only care about files modified in the last 7 days
                    if (datetime.datetime.now() - dt).days <= 7:
                        found.append((path, dt, os.path.getsize(path)))
        
        # Sort by date, newest first
        found.sort(key=lambda x: x[1], reverse=True)
        if found:
            for path, dt, size in found[:15]:
                print(f"- {os.path.basename(path)}: modified on {dt} ({size} bytes) in {os.path.dirname(path)}")
        else:
            print("No recent images found.")
