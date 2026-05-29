import os

scratch_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\scratch"
for name in os.listdir(scratch_dir):
    if name.endswith(".py"):
        path = os.path.join(scratch_dir, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                if "clean_background" in content:
                    print(f"Found in {name}")
        except Exception:
            pass
