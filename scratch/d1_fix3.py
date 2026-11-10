# D1 fix round 3: chat-link sweep
import re, sys, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 1) remove inert chatLink config props everywhere in live pages
pat_chatlink = re.compile(r"""\s*chatLink:\s*['"][^'"]*chat[^'"]*['"],""")
n1 = 0
for f in glob.glob('pages/**/*.html', recursive=True):
    t = open(f, encoding='utf-8', errors='replace').read()
    t2, n = pat_chatlink.subn('', t)
    if n:
        open(f, 'w', encoding='utf-8').write(t2); n1 += n
        print(f'chatLink removed ({n}x): {f}')

# 2) student-services: remaining functional navigations -> notifications
f = 'pages/student/student-services.html'
t = open(f, encoding='utf-8').read()
t2, n = re.subn(r"""window\.location\.href\s*=\s*['"]\.\./shared/chat\.html['"]""", "window.location.href = 'student-notifications.html'", t)
open(f, 'w', encoding='utf-8').write(t2)
print('student-services navigations rewired:', n)

# 3) student-lost-found: remove dead Message Reporter button block
f = 'pages/student/student-lost-found.html'
t = open(f, encoding='utf-8').read()
block = """  if (!isMine) {
    const btnChat = document.createElement('button');
    btnChat.className = 'px-3.5 py-2 rounded-xl text-xs font-medium bg-surface-container-low  text-on-surface flex items-center gap-1 cursor-pointer';
    btnChat.innerHTML = '<span class="material-symbols-outlined text-base text-outline">chat</span> Message Reporter';
    btnChat.onclick = () => {
      window.location.href = `../shared/chat.html?contact=${encodeURIComponent(item.reporterName)}&ref=${encodeURIComponent(item.refId)}&item=${encodeURIComponent(item.title)}`;
    };
    row.appendChild(btnChat);
  }
"""
if block in t:
    t = t.replace(block, '')
    open(f, 'w', encoding='utf-8').write(t)
    print('lost-found Message Reporter block removed: OK')
else:
    print('lost-found Message Reporter block: NOT FOUND verbatim')

# 4) principal notifLink -> shared announcements
for f in ('pages/principal/principal-profile.html', 'pages/principal/principal-reports.html'):
    t = open(f, encoding='utf-8').read()
    t2 = t.replace("'../messaging/campus-announcements.html'", "'../shared/announcements.html?portal=principal'")
    if t2 != t:
        open(f, 'w', encoding='utf-8').write(t2); print('notifLink rewired:', f)

# final leftover scan on live surfaces
live = glob.glob('pages/**/*.html', recursive=True) + glob.glob('assets/js/*.js') + ['index.html']
bad = 0
for f in live:
    t = open(f, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'(?:chat|group-chat|class-chats|campus-announcements)\.html', t):
        s = max(0, m.start()-60)
        print('LEFTOVER', f, '::', ' '.join(t[s:m.end()+30].split())[:140]); bad += 1
print('total leftovers:', bad, '| chatLink props removed:', n1)
