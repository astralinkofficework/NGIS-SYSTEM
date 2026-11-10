import glob

search_terms = ['ks-workflow-bar', 'Build weekly class and teacher schedules', 'Remaining Periods', 'bg-surface-container-lowest p-3 sm:p-space-md rounded-2xl border']

for fn in glob.glob('assets/js/*.js') + glob.glob('pages/**/*.html', recursive=True):
    try:
        with open(fn, 'r', encoding='utf-8') as f:
            c = f.read()
        for term in search_terms:
            if term in c:
                print(f'{fn}: found "{term}"')
    except Exception as e:
        pass

