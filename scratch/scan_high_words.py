import os, glob, re

files = glob.glob('pages/principal/*.html')
terms = ['dossier', 'cohort', 'adjudicat', 'cryptograph', 'pedagog', 'credentialed', 'custod', 'requisition', 'oversight', 'jurisdiction', 'sovereign', 'audit trail', 'executive governance', 'ledger']

for fpath in sorted(files):
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Strip HTML comments and CSS classes/selectors
    stripped = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    stripped = re.sub(r'<style.*?</style>', '', stripped, flags=re.DOTALL)
    stripped = re.sub(r'class="[^"]*"', '', stripped)
    stripped = re.sub(r'id="[^"]*"', '', stripped)
    
    hits = []
    for t in terms:
        matches = list(re.finditer(r'\b' + t + r'\w*', stripped, re.I))
        if matches:
            # show snippet
            snippets = [stripped[max(0, m.start()-20):min(len(stripped), m.end()+25)].replace('\n', ' ') for m in matches[:3]]
            hits.append((t, len(matches), snippets))
    if hits:
        print(f"=== {fname} ===")
        for t, count, snips in hits:
            print(f"  {t} ({count}): {snips}")

