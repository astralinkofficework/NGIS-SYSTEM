with open(r"scratch/test_timetable_scheduler.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("[TEST 5]")
print(text[idx:idx+400])
