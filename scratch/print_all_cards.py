import glob, re

for f in sorted(glob.glob("pages/principal/*.html")):
    with open(f, "r", encoding="utf-8") as fh:
        c = fh.read()
    if "telemetry-card" in c:
        print(f"\n==================== {f} ====================")
        # find all cards
        # We can find blocks with class containing telemetry-card
        # and print each card's structure
        pos = 0
        card_num = 1
        while True:
            idx = c.find('telemetry-card', pos)
            if idx == -1:
                break
            start = c.rfind('<div', 0, idx)
            # Find closing of this card by bracket counting or just take next 800 chars
            print(f"--- Card {card_num} ---")
            card_content = c[start:start+700]
            print(card_content[:card_content.find('</section>') if '</section>' in card_content else 500])
            pos = idx + len('telemetry-card')
            card_num += 1

