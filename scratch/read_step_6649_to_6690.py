import os
import json

log_path = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\.system_generated\logs\transcript.jsonl"

if os.path.exists(log_path):
    print("Reading steps 6649 to 6690:")
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                step_idx = obj.get("step_index")
                if 6649 <= step_idx <= 6690:
                    t = obj.get("type")
                    print(f"Step {step_idx} | {t}")
                    tool_calls = obj.get("tool_calls", [])
                    for tc in tool_calls:
                        args = tc.get("args", {})
                        if "CodeContent" in args:
                            print(f"  Tool: {tc.get('name')} | CodeContent:\n{args['CodeContent'][:1200]}\n...")
            except Exception as e:
                pass
else:
    print("transcript.jsonl not found!")
