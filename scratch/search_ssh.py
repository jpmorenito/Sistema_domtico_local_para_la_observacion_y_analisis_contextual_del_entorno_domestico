import os

scratch_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\scratch"
for name in os.listdir(scratch_dir):
    if name.endswith(".py") or name.endswith(".txt"):
        path = os.path.join(scratch_dir, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                if "ssh" in content.lower() or "jpmorenito" in content.lower() or "192.168" in content.lower():
                    print(f"Found in {name}")
        except Exception:
            pass
