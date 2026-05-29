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
                    if "conexion_nodo_puerta.png" in code and "edit_images.py" in args.get("TargetFile", ""):
                        print("FOUND CODE in edit_images.py:")
                        print(code)
                        print("=" * 80)
        except Exception as e:
            pass
