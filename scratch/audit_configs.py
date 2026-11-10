import json, os

if os.path.exists("data/system_configuration.json"):
    with open("data/system_configuration.json", "r", encoding="utf-8") as f:
        sys_conf = json.load(f)
    print("system_configuration.json keys:", list(sys_conf.keys()))
    print("Preview of system_configuration.json:")
    print(json.dumps(sys_conf, indent=2)[:1000])

if os.path.exists("data/timetable_state.json"):
    with open("data/timetable_state.json", "r", encoding="utf-8") as f:
        tt_state = json.load(f)
    print("\ntimetable_state.json keys:", list(tt_state.keys()))
    if "settings" in tt_state:
        print("timetable_state settings:", json.dumps(tt_state["settings"], indent=2)[:600])

