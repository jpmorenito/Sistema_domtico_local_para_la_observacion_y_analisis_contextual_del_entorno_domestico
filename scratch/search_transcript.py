import json
import re

transcript_path = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\.system_generated\logs\transcript.jsonl"

print("Searching transcript for image edits...")

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            content = data.get("content", "")
            # Look for code block writing a python file
            if "TargetFile" in line and (".py" in line) and ("Image" in line or "PIL" in line or "conexion_nodo" in line):
                # Print the tool calls of the model
                tool_calls = data.get("tool_calls", [])
                for tc in tool_calls:
                    if tc.get("name") == "write_to_file":
                        args = tc.get("args", {})
                        target = args.get("TargetFile", "")
                        if "edit" in target or "image" in target or "draw" in target or "process" in target or "conexion" in target:
                            print(f"TargetFile: {target}")
                            print("Code Content:")
                            print(args.get("CodeContent"))
                            print("=" * 60)
            # Or look for command running python files
            if "run_command" in line and ".py" in line:
                pass
        except Exception as e:
            pass
