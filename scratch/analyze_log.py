with open(r"c:\Users\jacob\Downloads\TFG\Documento final\__memoria.log", "r", encoding="utf-8", errors="ignore") as f:
    log_content = f.read()

# Let's search for "Glosario" or "abreviaturas" or the pages around Roman numerals.
# Let's find "Glosario de abreviaturas" and print 50 lines before and after.
lines = log_content.splitlines()
for idx, line in enumerate(lines):
    if "[18]" in line or "[19]" in line:
        print(f"--- line {idx}: {line}")
        start = max(0, idx - 20)
        end = min(len(lines), idx + 20)
        for i in range(start, end):
            print(f"{i:5d}: {lines[i]}")
        print("="*40)
