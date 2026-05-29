import os
import json

log_path = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\.system_generated\logs\transcript.jsonl"

if os.path.exists(log_path):
    print("Found transcript.jsonl. Searching for ssh or raspberry or yaml...")
    count = 0
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if "ssh" in line.lower() or "jpmorenito" in line.lower() or "yaml" in line.lower() or "ip" in line.lower():
                try:
                    obj = json.loads(line)
                    # Print only relevant parts to avoid flooding
                    print(f"Step {obj.get('step_index')}: {obj.get('type')} | Content snippet: {str(obj.get('content'))[:150]}")
                    if 'tool_calls' in obj:
                        print(f"  Tool calls: {obj['tool_calls']}")
                    count += 1
                    if count > 40:
                        print("Too many matches, truncating...")
                        break
                except Exception as e:
                    print(f"Error parsing line: {e}")
else:
    print(f"transcript.jsonl not found at {log_path}")
