import io
s = io.open(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\server.py', encoding='utf-8').read()
print('lines', s.count('\n') + 1)
for tok in ('PRINCIPAL_DEMO_STATE', '_demo_filter_queue', '_demo_audit', '_demo_now',
            'PRINCIPAL APPROVAL QUEUE ROUTES', "build_principal_queue()",
            "@app.route('/api/principal/approvals'"):
    print(tok, s.count(tok))
