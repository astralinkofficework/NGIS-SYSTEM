import subprocess

out = subprocess.check_output(['git', 'log', '-p', '-n', '2', 'pages/student/css/hero.css'], encoding='utf-8', errors='ignore')
for line in out.splitlines():
    if 'hero-body' in line or 'padding' in line and 'hero' in line or 'dash-overlap' in line:
        print(line)
