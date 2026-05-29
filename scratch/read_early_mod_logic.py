import os
import json

log_path = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\.system_generated\logs\transcript.jsonl"

if os.path.exists(log_path):
    print("Reading transcript lines from step 4580 to 4750:")
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                step_idx = obj.get("step_index")
                if 4580 <= step_idx <= 4750:
                    t = obj.get("type")
                    content = str(obj.get("content", ""))[:150].replace("\n", " ")
                    print(f"Step {step_idx} | {t} | {content}")
                    tool_calls = obj.get("tool_calls", [])
                    for tc in tool_calls:
                        print(f"  Tool: {tc.get('name')}")
                        args = tc.get("args", {})
                        # Show file content if it is a python script
                        if "CodeContent" in args:
                            print(f"  CodeContent:\n{args['CodeContent'][:600]}\n...")
            except Exception as e:
                pass
else:
    print("transcript.jsonl not found!")
