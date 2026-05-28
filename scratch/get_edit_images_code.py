import json

transcript_path = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\.system_generated\logs\transcript.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            tool_calls = data.get("tool_calls", [])
            for tc in tool_calls:
                if tc.get("name") == "write_to_file":
                    args = tc.get("args", {})
                    target = args.get("TargetFile", "")
                    if "edit_images.py" in target:
                        code = args.get("CodeContent", "")
                        # Replace literal \n with newlines if needed, or if it was serialized
                        # Usually, python's json.loads already decodes \n, but let's check
                        code = code.replace("\\n", "\n").replace("\\t", "\t")
                        if "conexion_nodo_puerta.png" in code:
                            lines = code.split("\n")
                            for idx, l in enumerate(lines):
                                if "conexion_nodo_puerta.png" in l or "path3" in l:
                                    start = max(0, idx - 5)
                                    end = min(len(lines), idx + 40)
                                    print(f"--- Code lines {start} to {end} ---")
                                    for i in range(start, end):
                                        print(f"{i+1}: {lines[i]}")
                                    break
        except Exception as e:
            pass
