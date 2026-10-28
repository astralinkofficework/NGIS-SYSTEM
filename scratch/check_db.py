import sys
sys.path.insert(0, '.')
import server
print("DB keys:", list(server.DB.keys()))
for k in ['students', 'classes', 'teachers', 'parents', 'subjects', 'campuses', 'departments']:
    if k in server.DB:
        print(f"server.DB['{k}']: {len(server.DB[k])} items")
        print(f"Sample {k}:", server.DB[k][0] if server.DB[k] else "Empty")
