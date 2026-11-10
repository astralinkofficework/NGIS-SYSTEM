import json

transcript_path = r"C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7\.system_generated\logs\transcript_full.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        if data.get("type") == "USER_INPUT":
            content = data.get("content", "")
            if "Master Timetable" in content:
                print("Found USER_INPUT with length:", len(content))
                with open(r"scratch\user_prompt_10.html", "w", encoding="utf-8") as out:
                    out.write(content)
                print("Saved to scratch/user_prompt_10.html")

