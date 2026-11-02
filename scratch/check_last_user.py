import json

transcript_path = r"C:\Users\oudom\.gemini\antigravity\brain\92720a74-07b3-40fa-91e3-a384311b91aa\.system_generated\logs\transcript.jsonl"
with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        if data.get("source") in ["USER_EXPLICIT", "USER"]:
            print("STEP:", data.get("step_index"))
            print("CONTENT:", data.get("content"))
            print("---")

