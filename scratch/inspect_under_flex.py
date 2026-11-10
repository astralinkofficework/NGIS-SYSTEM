import glob, re

for f in sorted(glob.glob("pages/principal/*.html")):
    with open(f, "r", encoding="utf-8") as fh:
        c = fh.read()
    if "telemetry-card" in c:
        print(f"\n==================== {f} ====================")
        # Find every telemetry-card block
        pattern = re.compile(r'(<div class="[^"]*telemetry-card[^"]*">)(.*?)(</div>\s*</div>)', re.DOTALL)
        matches = list(re.finditer(r'<div class="[^"]*telemetry-card[^"]*">', c))
        for i, m in enumerate(matches):
            start = m.start()
            # find matching end of card
            # A card has <div class="telemetry-card..."> then <div class="flex items-start justify-between">...</div> and optionally a second div... then closing </div>
            card_sub = c[start:start+1200]
            # let's look for the flex items-start justify-between
            f_start = card_sub.find('flex items-start justify-between')
            if f_start != -1:
                # find the end of this flex div
                # We can trace div tags
                div_count = 0
                div_open_idx = card_sub.rfind('<div', 0, f_start)
                f_end = -1
                for tag_match in re.finditer(r'</?div[^>]*>', card_sub[div_open_idx:]):
                    tag = tag_match.group(0)
                    if tag.startswith('</div'):
                        div_count -= 1
                    else:
                        div_count += 1
                    if div_count == 0:
                        f_end = div_open_idx + tag_match.end()
                        break
                if f_end != -1:
                    under_flex = card_sub[f_end:].strip()
                    # take up to the next </div> that closes the card
                    print(f"Card {i+1} under flex: {under_flex[:150]}...")

