import sys, os
sys.path.insert(0, os.path.abspath('.'))
from server import DB
import json
print("Assignments in DB:")
print(json.dumps(DB.get('assignments', []), indent=2))
print("Teachers in DB:")
print(json.dumps(DB.get('teachers', []), indent=2))

