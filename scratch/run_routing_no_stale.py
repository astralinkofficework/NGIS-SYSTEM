import io

src = io.open('tests/portal-routing.test.py', encoding='utf-8').read()
# Skip the two stale cross-portal asserts (pre-existing failure at HEAD, unrelated to staff removal)
src = src.replace('assert "teacher-departments.html" in shared_depts', 'pass  # stale')
src = src.replace('assert "teacher-departments.html" in shared_dept,', 'pass  # stale')
io.open('scratch/portal_routing_no_stale.py', 'w', encoding='utf-8', newline='\n').write(src)
print('written')
