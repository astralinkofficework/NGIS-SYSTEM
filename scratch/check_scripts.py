import urllib.request, re

html = urllib.request.urlopen('http://127.0.0.1:3000/pages/teacher/teacher.html').read().decode('utf-8')
scripts = re.findall(r'<script\s+src="([^"]+)"', html)
print('scripts:', scripts)
for s in scripts:
    url = 'http://127.0.0.1:3000/pages/teacher/' + s
    try:
        content = urllib.request.urlopen(url).read().decode('utf-8', errors='ignore')
        if 'Course Materials' in content:
            print('FOUND Course Materials in:', s)
        if 'Teaching' in content:
            print('FOUND Teaching in:', s)
    except Exception as e:
        print('Error loading', url, e)
