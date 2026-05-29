import os

root_dir = r"c:\Users\jacob\Downloads\TFG\Documento final"
yaml_files = []

for root, dirs, files in os.walk(root_dir):
    for f in files:
        if f.endswith(".yaml") or f.endswith(".yml"):
            yaml_files.append(os.path.join(root, f))

print("YAML files found:")
for yf in yaml_files:
    print(yf)
