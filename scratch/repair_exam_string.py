"""Repair newline accidentally left inside the exam print-template JS string.

fix_inject_position stripped the misplaced block but replaced it with a literal
newline, splitting the single-quoted template:  '</style>\n</head><body>'  -> JS
syntax error. The real document head never has '</style>' immediately followed by
'</head>' on one adjacency, so this pattern is unique to the JS template.
"""
import glob, re

targets = []
for p in sorted(glob.glob('pages/**/*.html', recursive=True)) + ['index.html']:
    s = open(p, encoding='utf-8').read()
    # only inside JS strings: the tight '</head><body>' adjacency (no whitespace)
    # never occurs in a real head (which has </head>\n<body), so this is unique.
    fixed = re.sub(r"</style>\s*\n\s*</head><body>", "</style></head><body>", s)
    if fixed != s:
        open(p, 'w', encoding='utf-8').write(fixed)
        targets.append(p)
print('Repaired pages:', targets)
