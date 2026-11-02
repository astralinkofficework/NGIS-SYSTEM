import io, re

KEEP = re.compile(r'staffNotes|handedToStaff|is_staff|Staff will|staff verification|'
                  r'updaterRole|staff_name|staff_role|reviewerRole|reviewer_name|'
                  r'Authorized Staff|Staff Member|Lost & Found Staff|updater_name')
hits = []
for i, ln in enumerate(io.open('server.py', encoding='utf-8'), 1):
    if re.search(r"operationalTasks|DB\['staff'\]|staff", ln, re.I) and not KEEP.search(ln):
        hits.append(f'{i}: {ln.rstrip()[:140]}')
print('\n'.join(hits))
