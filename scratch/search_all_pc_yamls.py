import os

paths_to_search = [
    "c:/Users/jacob/Downloads",
    "c:/Users/jacob/Documents",
    "c:/Users/jacob/Desktop",
    "c:/Users/jacob"
]

target_names = [
    "esp32-nodo-ambiente",
    "esp32-zona-escritorio",
    "esp32-zona-puerta",
    "automations.yaml"
]

print("Scanning for yaml configurations on PC...")
found_files = []

for base_path in paths_to_search:
    if os.path.exists(base_path):
        print(f"Searching in: {base_path}")
        # Use a depth limit of 3 to avoid scanning millions of files in the home dir
        for root, dirs, files in os.walk(base_path):
            # Calculate depth relative to base_path
            rel_path = os.path.relpath(root, base_path)
            depth = len(rel_path.split(os.sep)) if rel_path != "." else 0
            if depth > 3:
                # Clear dirs to prevent going deeper
                dirs.clear()
                continue
                
            for file in files:
                if file.endswith(".yaml") or file.endswith(".yml"):
                    file_lower = file.lower()
                    for target in target_names:
                        if target in file_lower:
                            full_path = os.path.join(root, file)
                            found_files.append(full_path)
                            print(f"FOUND: {full_path} ({os.path.getsize(full_path)} bytes)")

print(f"Scan complete. Total files found: {len(found_files)}")
