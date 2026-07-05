import os
import glob
import datetime

user_home = "C:/Users/jacob"
screenshots_folder = f"{user_home}/Pictures/Screenshots"

print(f"Searching for all image files in {screenshots_folder}...")
image_extensions = ('*.png', '*.jpg', '*.jpeg')

found = []
if os.path.exists(screenshots_folder):
    for ext in image_extensions:
        pattern = os.path.join(screenshots_folder, "**", ext)
        for path in glob.glob(pattern, recursive=True):
            if os.path.isfile(path):
                mtime = os.path.getmtime(path)
                dt = datetime.datetime.fromtimestamp(mtime)
                found.append((path, dt, os.path.getsize(path)))

# Sort by date, newest first
found.sort(key=lambda x: x[1], reverse=True)
print(f"Total screenshots found: {len(found)}")

# Print all screenshots that might be related, or at least the top 50 newest ones
for path, dt, size in found[:50]:
    name = os.path.basename(path)
    # Check if name contains any keywords or if it's just a general name
    print(f"- {name}: modified on {dt} ({size} bytes)")
