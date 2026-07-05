with open(r"c:\Users\jacob\Downloads\TFG\Documento final\__memoria.log", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

errors = [line for line in lines if "Error" in line or "error" in line or "!" in line]
print("Found", len(errors), "lines with error indicator:")
for e in errors[:30]:
    print(e.strip())
