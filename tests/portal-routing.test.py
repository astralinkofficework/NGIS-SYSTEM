#!/usr/bin/env python3
"""Static regression checks for NGIS portal routing and retired messaging cleanup."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

for layout_path in (ROOT / "layout.js", ROOT / "assets/js/layout.js"):
    layout = layout_path.read_text()
    assert "function resolvePortalRole" in layout, layout_path
    assert "ngis_user" in layout, layout_path
    assert "pathRole" in layout, layout_path
    assert "window.location.replace" in layout, layout_path
    assert not re.search(r'id:"messaging", label:"Messaging", icon:"forum", collapsible:true', layout), layout_path
    for retired in ("messaging-dashboard", "saved", "attachments", "notification-preferences", "message-search"):
        assert f'id:"{retired}"' not in layout, (layout_path, retired)
    for retired_route in (
        "pages/messaging/messaging-dashboard.html",
        "pages/messaging/search.html",
    ):
        assert retired_route not in layout, (layout_path, retired_route)

for retired_file in (
    "pages/messaging/messaging-dashboard.html",
    "pages/messaging/saved.html",
    "pages/messaging/attachments.html",
    "pages/messaging/notification-preferences.html",
    "pages/messaging/search.html",
):
    assert not (ROOT / retired_file).exists(), retired_file

messaging_data = (ROOT / "assets/js/messaging-data.js").read_text()
for retired_symbol in (
    "SAVED", "ATTACHMENTS", "NOTIF_CATEGORIES", "SEARCH_INDEX",
    "saved:", "attachments:", "notifCategories:", "searchIndex:",
):
    assert retired_symbol not in messaging_data, retired_symbol

print("portal-routing.test.py: PASS")
