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
                    code = args.get("CodeContent", "")
                    if "conexion_nodo_puerta.png" in code or "path3" in code:
                        # Print the block that modifies path3 or door node
                        # We print lines of the code content containing path3 or door node
                        lines = code.replace("\\n", "\n").replace("\\t", "\t").split("\n")
                        for idx, l in enumerate(lines):
                            if "conexion_nodo_puerta.png" in l or "path3" in l:
                                start = max(0, idx - 2)
                                end = min(len(lines), idx + 25)
                                print(f"--- Step {data.get('step_index')} code lines {start} to {end} ---")
                                for i in range(start, end):
                                    print(f"{i+1}: {lines[i]}")
        except Exception as e:
            pass
