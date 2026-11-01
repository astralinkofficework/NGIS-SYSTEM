import json

transcript_path = r"C:\Users\oudom\.gemini\antigravity\brain\42e7f2c5-dd76-4874-84f0-090ddb400de9\.system_generated\logs\transcript_full.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i == 51:
            data = json.loads(line)
            content = data.get("content", "")
            print("Line 51 length:", len(content))
            with open("scratch/raw_data.csv", "w", encoding="utf-8") as out:
                out.write(content)
            print("Successfully written to scratch/raw_data.csv")
            break
