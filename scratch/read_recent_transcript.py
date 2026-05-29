import os
import json

log_path = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\.system_generated\logs\transcript.jsonl"

if os.path.exists(log_path):
    print("Reading recent transcript lines:")
    lines = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            lines.append(line)
    
    # Let's inspect the last 100 lines
    last_lines = lines[-100:]
    for i, line in enumerate(last_lines):
        try:
            obj = json.loads(line)
            step = obj.get("step_index")
            t = obj.get("type")
            content = str(obj.get("content", ""))[:120].replace("\n", " ")
            tcalls = obj.get("tool_calls", "")
            print(f"Step {step} | {t} | {content}")
            if tcalls:
                print(f"  Tools: {tcalls}")
        except Exception as e:
            print(f"Error parsing line {i}: {e}")
else:
    print("transcript.jsonl not found!")
