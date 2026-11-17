with open('pages/admin/admin-security.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

markers = [
    '<style>',
    '</style>',
    'LIVE PERIMETER TELEMETRY MAP',
    'id="forensicBackdrop"',
    'id="mitigateModal"',
    'id="fullscreenMapOverlay"',
    '<script>window.PAGE',
    '// Forensics Mock Dataset',
    'id="tab-overview"',
    'id="tab-security-settings"'
]

for i, l in enumerate(lines):
    for m in markers:
        if m in l:
            print(f"Line {i+1}: {m}")
