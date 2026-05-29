import os
import json

log_path = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\.system_generated\logs\transcript.jsonl"

if os.path.exists(log_path):
    print("Searching transcript.jsonl for early modifications prior to step 4581...")
    matches = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                step_idx = obj.get("step_index")
                if step_idx < 4581:
                    tc = obj.get("tool_calls", [])
                    for t in tc:
                        cmd = str(t.get("args", {}))
                        if "conexion_nodo_" in cmd or "Img" in cmd:
                            matches.append((step_idx, obj.get("type"), t.get("name"), cmd[:150]))
            except Exception:
                pass
    print(f"Found {len(matches)} early matches:")
    for step_idx, ttype, name, args in matches[:50]:
        print(f"Step {step_idx} | {ttype} | Tool: {name} | Args: {args}")
else:
    print("transcript.jsonl not found!")
