import glob, re

pages = [
    "pages/principal/principal.html",
    "pages/principal/principal-activity.html",
    "pages/principal/principal-attendance.html",
    "pages/principal/principal-lost-found.html",
    "pages/principal/principal-profile.html",
    "pages/principal/principal-services.html",
    "pages/principal/principal-timetables.html",
    "pages/principal/principal-reports.html"
]

for p in pages:
    with open(p, "r", encoding="utf-8") as fh:
        c = fh.read()
    print(f"***** {p} *****")
    # find all telemetry cards
    for m in re.finditer(r'<div class="[^"]*telemetry-card[^"]*">', c):
        idx = m.start()
        # Find closing div of card
        end_idx = c.find('</div>\n      </div>', idx)
        if end_idx != -1:
            card_str = c[idx:end_idx+18]
        else:
            card_str = c[idx:idx+600]
        # check if it has a second div after flex items-start justify-between
        first_div_close = card_str.find('</div>\n        </div>')
        if first_div_close == -1:
            first_div_close = card_str.find('</div>\n          </div>')
        print(f"Card: {card_str[:120]} ...")
        # print what is after first_div_close
        if first_div_close != -1:
            print("  AFTER TOP PART:", card_str[first_div_close+18:].strip().replace('\n', ' '))

