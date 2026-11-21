# -*- coding: utf-8 -*-
import os
import urllib.request
import json

output_dir = r"assets/images/icons-3d"
os.makedirs(output_dir, exist_ok=True)

icons_to_download = {
    # Functional Mapping
    "calendar": "calendar",
    "timetable": "timetable",
    "classroom": "classroom",
    "notepad": "notepad",
    "open-book": "open-book",
    "graduation-cap": "graduation-cap",
    "trophy": "trophy",
    "fingerprint": "fingerprint",
    "megaphone": "megaphone",
    "student-male": "student-male",
    "business-report": "business-report",
    "documents": "documents",
    "briefcase": "briefcase",
    "books": "books",
    "alarm-clock": "alarm-clock",
    "confetti": "confetti",
    "training": "training",
    "compass": "compass",
    "ok": "ok",
    "empty-box": "empty-box",
    "calculator": "calculator",
    "microscope": "microscope"
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

results = []

for name, slug in icons_to_download.items():
    url = f"https://img.icons8.com/3d-fluency/94/{slug}.png"
    dest_path = os.path.join(output_dir, f"{name}.png")
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            with open(dest_path, "wb") as f:
                f.write(data)
            size_kb = round(len(data) / 1024, 1)
            results.append({
                "concept": name,
                "slug": slug,
                "file": f"{name}.png",
                "bytes": len(data),
                "url": url,
                "status": "SUCCESS"
            })
            print(f"[OK] Downloaded {name}.png ({size_kb} KB)")
    except Exception as e:
        print(f"[ERROR] Failed {name}: {e}")
        results.append({
            "concept": name,
            "slug": slug,
            "status": f"FAILED: {e}"
        })

print(f"\nDownloaded {len([r for r in results if r['status'] == 'SUCCESS'])} of {len(icons_to_download)} icons.")
with open(os.path.join(output_dir, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
