import os
import json

log_path = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\.system_generated\logs\transcript.jsonl"

if os.path.exists(log_path):
    print("Scanning historical steps in transcript.jsonl for SSH/network tools...")
    matches = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                step_idx = obj.get("step_index")
                tool_calls = obj.get("tool_calls", [])
                
                # Check if this step is a command execution that matches network words
                is_match = False
                call_info = ""
                for tc in tool_calls:
                    if tc.get("name") == "run_command":
                        cmd = tc.get("args", {}).get("CommandLine", "")
                        if any(w in cmd.lower() for w in ["ssh", "scp", "ping", "192.168", "jacob-pi", "jpmorenito"]):
                            is_match = True
                            call_info = cmd
                
                if is_match:
                    matches.append((step_idx, call_info))
            except Exception:
                pass
                
    print(f"Found {len(matches)} historical network command steps:")
    for step_idx, cmd in matches:
        print(f"Step {step_idx}: {cmd}")
else:
    print("transcript.jsonl not found!")
