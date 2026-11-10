with open('assets/js/auth.js', 'r', encoding='utf-8') as f:
    auth_js = f.read()
print("auth.js length:", len(auth_js))
print("auth.js first 60 lines:")
print('\n'.join(auth_js.splitlines()[:60]))

with open('assets/js/protect.js', 'r', encoding='utf-8') as f:
    protect_js = f.read()
print("\nprotect.js length:", len(protect_js))
print("protect.js first 60 lines:")
print('\n'.join(protect_js.splitlines()[:60]))

