import io, re
s = io.open(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\server.py', encoding='utf-8').read().split('\n')
for i, l in enumerate(s, 1):
    if '@app.route' in l and ('transcripts' in l or 'service-requests' in l or '/grades' in l or 'attendance-by-day' in l):
        print(i, l.strip())
