for role in ['student', 'teacher', 'admin', 'principal', 'staff']:
    p = f'pages/{role}/_auth-bootstrap.js'
    print(f'=== {p} ===')
    try:
        with open(p, 'r', encoding='utf-8') as f:
            print(f.read().strip())
    except Exception as e:
        print('Error:', e)

