import re
for f in ['principal-classes','principal-departments','principal-attendance',
          'principal-approvals','principal-reports','principal-services',
          'principal-lost-found','principal-timetables']:
    s = open('pages/principal/%s.html' % f, encoding='utf-8').read()
    ids = re.findall(r'<input[^>]*?id="([^"]+)"[^>]*?type="(?:search|text)"', s)
    ids += re.findall(r'<input[^>]*?type="(?:search|text)"[^>]*?id="([^"]+)"', s)
    # also placeholder-bearing search inputs
    ph = re.findall(r'<input[^>]*?placeholder="([^"]*[Ss]earch[^"]*)"[^>]*?>', s)
    print('%-26s ids=%s' % (f, list(dict.fromkeys(ids))[:5]))
    print('%-26s ph =%s' % ('', ph[:3]))
