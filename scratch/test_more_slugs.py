# -*- coding: utf-8 -*-
import urllib.request
import urllib.error

extra_candidates = [
    "notepad", "memo", "note", "edit", "pencil", "pen", "fountain-pen-close-up",
    "identification-documents", "pass", "checked-checkbox",
    "teacher", "school-director", "podium-with-speaker",
    "microscope", "calculator", "dna", "test-tube",
    "certificate", "contract", "certificate-degree", "checked-laptop"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for slug in extra_candidates:
    url = f"https://img.icons8.com/3d-fluency/94/{slug}.png"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                length = len(resp.read())
                if length > 500:
                    print(f"[FOUND] {slug} ({length} bytes)")
    except Exception:
        pass
