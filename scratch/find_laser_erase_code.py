import os
import json

log_path = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\.system_generated\logs\transcript.jsonl"

if os.path.exists(log_path):
    print("Searching transcript.jsonl for laser wire erasing code...")
    matches = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if "laser" in line.lower() and "wire" in line.lower() and "erase" in line.lower() or "vcc" in line.lower() and "laser" in line.lower():
                try:
                    obj = json.loads(line)
                    step_idx = obj.get("step_index")
                    tc = obj.get("tool_calls", [])
                    for t in tc:
                        if t.get("name") == "write_to_file":
                            matches.append((step_idx, t.get("args", {}).get("CodeContent", "")))
                except Exception:
                    pass
    print(f"Found {len(matches)} matches:")
    for step_idx, code in matches:
        print(f"--- Step {step_idx} ---")
        print(code[:800])
        print("----------------------")
else:
    print("transcript.jsonl not found!")
