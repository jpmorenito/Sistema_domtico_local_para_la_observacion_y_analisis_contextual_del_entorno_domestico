import json

transcript_path = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\.system_generated\logs\transcript.jsonl"
out_path = r"c:\Users\jacob\Downloads\TFG\Documento final\scratch\step_detail.txt"

with open(transcript_path, "r", encoding="utf-8") as f, open(out_path, "w", encoding="utf-8") as out:
    for line in f:
        try:
            data = json.loads(line)
            step_idx = data.get("step_index")
            # We want to find the step where the edit_images.py script was written
            # in the previous turn (likely around step 4643 to 4647)
            if step_idx in [4643, 4644, 4645, 4646, 4647]:
                out.write(f"=== STEP {step_idx} ===\n")
                out.write(json.dumps(data, indent=2))
                out.write("\n\n")
        except Exception as e:
            pass

print(f"Done. Details written to {out_path}")
