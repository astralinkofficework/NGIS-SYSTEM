with open('pages/admin/admin-teacher-class-assignment.html', 'r', encoding='utf-8') as f:
    c = f.read()

print('Length of admin-teacher-class-assignment:', len(c))
print('PAGE config:', [l.strip() for l in c.split('\n') if 'PAGE=' in l or 'KS_MODULE=' in l or 'HERO_CONFIG' in l])

