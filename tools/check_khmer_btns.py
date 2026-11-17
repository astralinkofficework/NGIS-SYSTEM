with open('assets/js/khmer-suite-ui.js', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if ('border-dashed border-emerald' in line or 'hover:bg-[#14532D]' in line) and ('+' in line or 'plus' in line or 'add' in line):
            print(f"{i}: {line.strip()[:100]}")
