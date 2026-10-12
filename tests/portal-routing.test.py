#!/usr/bin/env python3
"""Static regression checks for NGIS portal routing and layout separation."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
layout = (ROOT / "layout.js").read_text()

assert "function resolvePortalRole" in layout
assert "ngis_user" in layout
assert "pathRole" in layout
assert "window.location.replace" in layout

# Admin-only configuration must not be exposed to other role definitions.
role_chunks = {}
for role in ("admin", "teacher", "student", "parent"):
    match = re.search(rf"    {role}: \{{(.*?)(?=\n    (?:admin|teacher|student|parent): \{{|\n  \}};)" , layout, re.S)
    assert match, f"missing {role} navigation"
    role_chunks[role] = match.group(1)
for role in ("admin", "teacher", "student", "parent"):
    assert "telegram-config" not in role_chunks[role]

# No non-admin navigation entry may point to student-only lost-and-found.
for role in ("teacher", "student", "parent"):
    assert "pages/student/student-lost-found.html" not in role_chunks[role]

print("portal-routing.test.py: PASS")
