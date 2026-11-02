import io

src = io.open('server.py', encoding='utf-8').read()
new_layer = io.open('scratch/new_principal_layer.py', encoding='utf-8').read()

marker = '# ── PRINCIPAL & STAFF OVERSIGHT APIS ──'
end_marker = '# ── ADMIN MANAGEMENT API ENDPOINTS ──'

start = src.index(marker)
end = src.index(end_marker)
assert start < end, (start, end)

old_block = src[start:end]
print('Replacing %d chars, %d lines' % (len(old_block), old_block.count('\n')))

repl = new_layer.rstrip('\n') + '\n\n'
src = src[:start] + repl + src[end:]
io.open('server.py', 'w', encoding='utf-8', newline='\n').write(src)
print('Spliced OK!')
