import json

transcript_path = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\.system_generated\logs\transcript.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            step = data.get("step_index")
            if step in [5304, 5305]:
                print(f"\n================ STEP {step} ({data.get('source')}, {data.get('type')}) ================")
                print(json.dumps(data, indent=2))
        except Exception as e:
            pass
