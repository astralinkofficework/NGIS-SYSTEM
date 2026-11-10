import sys, os
sys.path.insert(0, os.path.abspath('.'))
from server import DB
import json
print("Classes in DB:")
print(json.dumps(DB.get('classes', []), indent=2))

