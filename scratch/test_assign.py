import sys, os
sys.path.insert(0, os.path.abspath('.'))
import json
from timetable_models import auto_assign, build_seed_state

state = build_seed_state()
res = auto_assign(state)
grid = state.get("grid", {})
print("Auto-assign result:", res.get("placed"), "lessons placed. Grid len:", len(grid))
if grid:
    print("Sample key:", list(grid.keys())[0], "value:", list(grid.values())[0])
