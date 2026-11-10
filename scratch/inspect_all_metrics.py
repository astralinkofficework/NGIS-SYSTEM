import glob, re

for f in sorted(glob.glob("pages/principal/*.html")):
    with open(f, "r", encoding="utf-8") as fh:
        content = fh.read()
    
    # Check if there are telemetry cards
    if "telemetry-card" in content:
        print("==================================================")
        print("FILE:", f)
        print("==================================================")
        # Find the section containing metrics or telemetry-card
        m = re.search(r'(<section[^>]*data-purpose="metrics-telemetry"[^>]*>.*?</section>)', content, re.DOTALL)
        if m:
            print(m.group(1)[:2500])
        else:
            # find all telemetry-card blocks
            matches = re.findall(r'(<div class="[^"]*telemetry-card[^"]*">.*?</div>\s*</div>)', content, re.DOTALL)
            for card in matches[:2]:
                print(card[:500])
                print("---")

