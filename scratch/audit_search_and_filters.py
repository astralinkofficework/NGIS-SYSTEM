import glob
import re

print("Auditing search inputs and filter select elements in all pages/principal/*.html...")

files = sorted(glob.glob("pages/principal/*.html"))

for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find search inputs
    inputs = re.findall(r'<input[^>]*placeholder=[\'"][^\'"]*?[Ss]earch[^\'"]*?[\'"][^>]*>', content)
    # Find filter selects
    selects = re.findall(r'<select[^>]*>', content)
    
    print(f"\n[{filepath}]")
    if not inputs:
        print("  No search input found.")
    for inp in inputs:
        has_inline_pad = "padding-left" in inp
        has_pl_imp = "!pl-" in inp
        print(f"  SEARCH: inline_pad={has_inline_pad}, !pl={has_pl_imp}")
        if not has_inline_pad:
            print(f"    Raw input: {inp[:120]}...")

    if selects:
        print(f"  Total selects: {len(selects)}")
        for sel in selects:
            has_w = "w-" in sel or "width" in sel
            if not has_w:
                print(f"    Select missing explicit width: {sel[:100]}")

