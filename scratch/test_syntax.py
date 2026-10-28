import sys
import os
import json
import sqlite3
from datetime import datetime, timezone

print("Testing python syntax and datetime...")
now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
print("Now:", now)
