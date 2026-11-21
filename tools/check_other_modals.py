import re

files = [
    'pages/student/student-services.html',
    'pages/admin/admin-modal-add-subject.html',
    'pages/teacher/teacher-reports.html',
    'pages/teacher/teacher-submissions.html'
]

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
        matches = re.findall(r'<div[^>]*id=["\'][^"\']*[Mm]odal[^"\']*["\'][^>]*>', content)
        print(f, 'modals found:', len(matches))
        for m in matches:
            print('  ', m)
        # Check for dark:bg-slate or bg-slate-900
        dark_matches = re.findall(r'class="[^"]*(?:dark:bg-slate|bg-slate-900|bg-gray-900)[^"]*"', content)
        if dark_matches:
            print('   Dark classes in file:', len(dark_matches))
            for dm in dark_matches[:3]:
                print('    ', dm[:100])
    except Exception as e:
        print(f, e)
