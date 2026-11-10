import glob, os, re

for f in sorted(glob.glob("pages/principal/*.html")):
    with open(f, "r", encoding="utf-8") as fh:
        c = fh.read()
    if "telemetry-card" in c:
        print(f"=== {f} ===")
        # Find blocks starting with telemetry-card
        for m in re.finditer(r'<div class="[^"]*telemetry-card[^"]*">', c):
            idx = m.start()
            print(c[idx:idx+400])
            print("---")

