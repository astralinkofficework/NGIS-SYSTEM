import sys
sys.path.insert(0, '.')
from server import DB
import json

print("Keys in server.DB:")
for k in DB.keys():
    v = DB[k]
    if isinstance(v, list):
        print(f"  {k}: list of {len(v)} items")
    elif isinstance(v, dict):
        print(f"  {k}: dict with {len(v)} keys")
    else:
        print(f"  {k}: {type(v)}")
