import os
import json

log_path = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\.system_generated\logs\transcript.jsonl"

if os.path.exists(log_path):
    print("Searching transcript.jsonl for early generation steps...")
    matches = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                step_idx = obj.get("step_index")
                t = obj.get("type")
                # Look for tool_calls that modify the images or write to scratch/
                tool_calls = obj.get("tool_calls", [])
                for tc in tool_calls:
                    if tc.get("name") in ["write_to_file", "replace_file_content", "run_command"]:
                        args_str = str(tc.get("args", {}))
                        if "conexion_nodo_" in args_str or "rebuild" in args_str:
                            matches.append((step_idx, t, tc.get("name"), args_str[:200]))
            except Exception:
                pass
    print(f"Found {len(matches)} early matches:")
    for m in matches[:30]:
        print(f"Step {m[0]} | {m[1]} | Tool: {m[2]} | Args: {m[3]}")
else:
    print("transcript.jsonl not found!")
