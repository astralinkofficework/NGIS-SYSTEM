import sys, os
sys.path.insert(0, os.path.abspath('.'))
from timetable_models import build_seed_state, auto_assign

s = build_seed_state()
print("Initial grid len:", len(s["grid"]))

# Modify an assignment in step 2: assign t_M2 to class_7A for Math
for a in s["assignments"]:
    if a["class_id"] == "class_7A" and a["subject_id"] == "sub_M":
        a["teacher_id"] = "t_M2"
        print("Updated assignment to t_M2")

# Run auto_assign
res = auto_assign(s)
new_grid = res["state"]["grid"]
print("Placed slots:", res["placed"], "Grid len:", len(new_grid))

# Check slots for class_7A
for k, cell in new_grid.items():
    if "class_7A" in k and cell["subject_id"] == "sub_M":
        print(f"Slot {k}: teacher={cell['teacher_id']}")
        assert cell["teacher_id"] == "t_M2", "Teacher assignment must match updated assignment!"
        break

print("SUCCESS: Dynamic auto_assign accurately uses live state.assignments!")

