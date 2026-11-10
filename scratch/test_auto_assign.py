import sys
sys.path.insert(0, '.')
import timetable_models as M
state = M.STORE.state()
print("Auto-assign function:", M.auto_assign)
try:
    res = M.auto_assign(state, class_id="class_7B")
    print("Placed for 7B:", res.get("placed", len(res.get("grid", {}))))
except Exception as e:
    print("Error:", e)
