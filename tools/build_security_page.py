import re

with open('tools/redesign_base.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<!DOCTYPE')
end = text.rfind('</html>') + len('</html>') if text.rfind('</html>') != -1 else len(text)
html = text[start:end]

# Extract styles from <style> in template
m_style = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
custom_css = m_style.group(1) if m_style else ""

# Extract Desktop Header
m_header = re.search(r'<header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs">.*?</header>', html, re.DOTALL)
desktop_header = m_header.group(0) if m_header else ""

# Extract Main content inside <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 space-y-6">...</main>
m_main = re.search(r'<main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 space-y-6">(.*?)</main>', html, re.DOTALL)
main_content = m_main.group(1) if m_main else ""

# Extract everything between </main> and the last <script>
m_main_end = html.find('</main>') + len('</main>')
m_last_script = html.rfind('<script')
modals_and_overlays = html[m_main_end:m_last_script].strip()

# Clean font-bold and font-semibold across all extracted blocks
def remove_bolds(s):
    s = re.sub(r'\bfont-bold\b', 'font-medium', s)
    s = re.sub(r'\bfont-semibold\b', 'font-medium', s)
    s = re.sub(r'\bfont-extrabold\b', 'font-medium', s)
    s = re.sub(r'\bfont-black\b', 'font-medium', s)
    s = re.sub(r'font-weight=["\'](?:bold|semibold|700|800|600)["\']', 'font-weight="500"', s)
    return s

desktop_header = remove_bolds(desktop_header)
main_content = remove_bolds(main_content)
modals_and_overlays = remove_bolds(modals_and_overlays)

# Make tab-overview active by default and tab-audit-history hidden by default
# Find tab-audit-history and add hidden if not present
main_content = re.sub(r'id=["\']tab-audit-history["\'] class=["\']tab-pane space-y-6["\']', 'id="tab-audit-history" class="tab-pane space-y-6 hidden"', main_content)
main_content = re.sub(r'class=["\']tab-pane space-y-6["\'] id=["\']tab-audit-history["\']', 'class="tab-pane space-y-6 hidden" id="tab-audit-history"', main_content)

# Find tab-overview and remove hidden
main_content = re.sub(r'class=["\']tab-pane space-y-6 hidden["\'] id=["\']tab-overview["\']', 'class="tab-pane space-y-6" id="tab-overview"', main_content)
main_content = re.sub(r'id=["\']tab-overview["\'] class=["\']tab-pane space-y-6 hidden["\']', 'id="tab-overview" class="tab-pane space-y-6"', main_content)

# Update tab buttons: overview button should have active class, others inactive
# Overview button:
desktop_header = re.sub(
    r'(<button class="tab-btn px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 flex items-center space-x-1.5 transition" data-tab="overview")',
    r'<button class="tab-btn px-3 py-1.5 rounded-lg font-medium flex items-center space-x-2 bg-emerald-900 text-white shadow-xs" data-tab="overview"',
    desktop_header
)
# Audit button:
desktop_header = re.sub(
    r'(<button class="tab-btn px-3 py-1.5 rounded-lg font-medium flex items-center space-x-2 bg-emerald-900 text-white shadow-xs" data-tab="audit-history")',
    r'<button class="tab-btn px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 flex items-center space-x-1.5 transition font-medium" data-tab="audit-history"',
    desktop_header
)

# Add hamburger button to the desktop_header on md:hidden
hamburger_html = '''        <!-- Mandatory Mobile Hamburger Menu Button (AGENTS.md Compliance) -->
        <button type="button" 
                class="hamburger-btn mobile-hamburger-btn md:hidden p-2 -ml-1 rounded-xl text-slate-700 hover:bg-slate-100 active:scale-95 transition-all flex items-center justify-center min-w-[40px] min-h-[40px]" 
                data-action="toggle-sidebar" 
                aria-label="Open menu" 
                aria-expanded="false" 
                title="Open navigation">
          <i class="ph ph-list text-xl text-slate-700"></i>
        </button>
'''
desktop_header = desktop_header.replace(
    '<div class="flex items-center space-x-3">\n      <div class="w-9 h-9',
    '<div class="flex items-center space-x-3">\n' + hamburger_html + '      <div class="w-9 h-9'
)

# Build full final HTML
full_html = f'''<!doctype html>
<html lang="en" data-theme="light" class="h-full">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
<title>NGIS · Cyber Defense Command &amp; SOC</title>

<!-- Fonts: Strictly light & medium weights (NO BOLD FONTS per AGENTS.md) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Symbols+Outlined" rel="stylesheet">

<!-- Bootstrap Icons v1.13.2 (NGIS Official Standard) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

<!-- Phosphor Icons for Mobile Hamburger Menu & Controls -->
<script src="https://unpkg.com/@phosphor-icons/web"></script>

<!-- Tailwind CSS CDN with forms and container queries plugins -->
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script>
  tailwind.config = {{
    theme: {{
      extend: {{
        fontFamily: {{
          sans: ['Inter', 'system-ui', 'sans-serif'],
          mono: ['"JetBrains Mono"', 'monospace'],
        }},
        colors: {{
          primary: '#0f5132',
          'primary-dark': '#0a3822',
          emerald: {{
            900: '#0f5132',
            950: '#0a3822'
          }}
        }},
        fontWeight: {{
          normal: '400',
          medium: '500',
          semibold: '500',
          bold: '500',
          extrabold: '500',
          black: '500' // Rule: NO BOLD FONTS per AGENTS.md
        }}
      }}
    }}
  }};
</script>

<!-- NGIS Design System & Global Styles -->
<link rel="stylesheet" href="../../assets/css/app.css">
<link rel="stylesheet" href="../../assets/css/hero.css">
<link rel="stylesheet" href="../../assets/css/interactions.css">
<link rel="stylesheet" href="../../assets/css/design-system.css">
<link rel="stylesheet" href="../../assets/css/action-icons.css?v=1.13.2">
<link rel="stylesheet" href="../../assets/css/ui-cleanup.css">
<script src="../../assets/js/action-icons.js?v=1.13.2" defer></script>
<script src="../../assets/js/auth.js"></script>
<script src="../../assets/js/protect.js"></script>
<script src="_auth-bootstrap.js"></script>

<style>
  /* Rule: NO BOLD FONTS. Maximum weight 500 across all UI (AGENTS.md) */
  *, h1, h2, h3, h4, h5, h6, b, strong, th, td, button, span, div, select, input, label {{
    font-weight: 400;
  }}
  .font-medium, th, h1, h2, h3, h4, [class*="font-semibold"], [class*="font-bold"] {{
    font-weight: 500 !important;
  }}

  /* Custom scrollbars */
  ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
  ::-webkit-scrollbar-track {{ background: #f1f5f9; }}
  ::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 9999px; }}

  /* Radar & Cyber Map Animations */
  .radar-grid {{
    background-image: radial-gradient(rgba(16, 185, 129, 0.12) 1px, transparent 1px),
                      radial-gradient(circle, rgba(16, 185, 129, 0.05) 0%, transparent 70%);
    background-size: 26px 26px, 100% 100%;
  }}
  .threat-tracer {{ stroke-dasharray: 6 8; animation: dash 1.6s linear infinite; }}
  .threat-tracer-amber {{ stroke-dasharray: 6 8; animation: dash 2.2s linear infinite; }}
  .shield-stream {{ stroke-dasharray: 5 6; animation: dashRev 2.8s linear infinite; }}
  @keyframes dash {{ to {{ stroke-dashoffset: -28; }} }}
  @keyframes dashRev {{ to {{ stroke-dashoffset: 28; }} }}

  /* Smooth scrollable nav tabs on mobile */
  .no-scrollbar::-webkit-scrollbar {{ display: none; }}
  .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
</style>
</head>

<body data-role="admin" data-portal="admin" data-page="security" class="bg-slate-100 text-slate-800 font-sans antialiased min-h-screen flex flex-col">

<!-- Main Layout Structure for layout.js -->
<main class="main flex-1 min-w-0 flex flex-col">

  <!-- Mandatory Mobile Appbar with Accessible Hamburger Menu (AGENTS.md Compliance) -->
  <header class="mobile-appbar md:hidden flex items-center justify-between px-4 py-3 bg-white border-b border-slate-200 sticky top-0 z-40 min-h-[44px]">
    <div class="flex items-center gap-3">
      <button type="button" 
              class="hamburger-btn mobile-hamburger-btn p-2 -ml-1 rounded-xl text-slate-700 hover:bg-slate-100 active:scale-95 transition-all flex items-center justify-center min-w-[40px] min-h-[40px]" 
              data-action="toggle-sidebar" 
              aria-label="Open menu" 
              aria-expanded="false" 
              title="Open navigation">
        <i class="ph ph-list text-xl text-slate-700"></i>
      </button>
      <div class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-lg bg-emerald-900 text-white flex items-center justify-center font-mono text-xs shadow-xs">SOC</div>
        <span class="text-xs font-medium text-emerald-900 tracking-wide uppercase">Cyber Defense Command</span>
      </div>
    </div>
    <div class="flex items-center gap-2">
      <button onclick="openMitigateModal('127.0.0.1')" class="px-2.5 py-1.5 bg-emerald-900 hover:bg-emerald-950 text-white rounded-lg text-xs font-medium shadow-xs flex items-center gap-1.5 transition active:scale-95">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
        <span>Enforce</span>
      </button>
    </div>
  </header>

  <!-- Hero Banner Anchor for layout.js -->
  <header id="heroBanner" role="banner"></header>

  <!-- Desktop & Tablet Executive Header & Tabs -->
  {desktop_header}

  <!-- Main Cyber Defense Content Container -->
  <div class="page flex-1 max-w-7xl w-full mx-auto p-3 sm:p-5 lg:p-6 space-y-6">
    {main_content}
  </div>

</main>

<!-- Modals, Overlays & Drawers -->
{modals_and_overlays}

<script>window.PAGE={{"role":"admin","active":"security"}};</script>
<script>window.HERO_CONFIG = {{
  name: 'Mr. Heng Samnang',
  id: 'Admin ID: ADM-2026-001',
  grade: 'School Administrator',
  avatar: 'https://images.pexels.com/photos/3184339/pexels-photo-3184339.jpeg?auto=compress&cs=tinysrgb&w=160',
  avatarSm: 'https://images.pexels.com/photos/3184339/pexels-photo-3184339.jpeg?auto=compress&cs=tinysrgb&w=80',
  title: 'Cyber Defense Command & SOC',
  greeting: 'Monitor threats, manage restrictions and inspect perimeter attack telemetry.',
  breadcrumbs: [{{ label: 'Security & Access Control' }}],
  homeLink: '../../index.html',
  signOutLink: '../../index.html',
  profileLink: 'admin-settings.html',
  notifLink: 'admin-security.html',
  notifCount: 0,
  ddRows: [
    {{ icon: 'security', text: 'Perimeter Telemetry Radar' }},
    {{ icon: 'shield', text: 'Server-side enforcement' }},
    {{ icon: 'history', text: 'Append-only audit trail' }},
    {{ icon: 'verified', text: 'Documented event taxonomy' }}
  ]
}};</script>
<script src="../../assets/js/hero.js"></script>
<script src="../../assets/js/layout.js"></script>

<!-- Cyber Defense Command & SOC JavaScript Controller -->
<script>
  // Forensics Mock Dataset mapping each attack vector and node
  const forensicData = {{
    'node-unauthorized': {{
      title: 'UNAUTHORIZED CREDENTIAL ATTACK',
      badge: 'SEV-1 (CRITICAL)',
      subtitle: 'INTERCEPTED AT NGIS GATEWAY PERIMETER',
      attackType: 'Credential Stuffing & Unauthorized Auth Probe',
      action: 'Firewall Drop (HTTP 401 Unauthorized)',
      time: '2024-11-17 18:35:12.482 UTC',
      waf: 'NGIS-WAF-01:3000',
      srcIp: '127.0.0.1:49210',
      asn: 'AS13335 (Cloudflare Ingress Dev Proxy)',
      geo: 'Phnom Penh, Cambodia 🇰🇭',
      ua: 'python-requests/2.31.0 [Automated Bot Runner]',
      targetAccount: 'Aiko Dubois',
      targetRole: 'USR-DMO-240 · FACULTY_STAFF (Teacher)',
      endpoint: 'GET /api/teacher/classes',
      campus: 'Tuol Kork Main Campus Gateway',
      headers: `Host: api.ngis.edu.kh\\nAuthorization: Bearer invalid.probe.signature_token\\nX-Forwarded-For: 127.0.0.1\\nUser-Agent: python-requests/2.31.0\\nSec-Fetch-Mode: cors`
    }},
    'node-ratelimit': {{
      title: 'TOKEN BUCKET RATE VIOLATION',
      badge: 'SEV-2 (WARNING)',
      subtitle: 'EXCEEDED 30 REQ / 60S THRESHOLD',
      attackType: 'Rapid API Endpoint Flooding (HTTP 429)',
      action: 'Progressive 60s Rate Throttle',
      time: '2024-11-17 18:34:02.110 UTC',
      waf: 'NGIS-TOKEN-BUCKET-CORE',
      srcIp: '203.0.113.66',
      asn: 'AS45435 (EZECOM ISP Backbone)',
      geo: 'Sen Sok Sector, Phnom Penh 🇰🇭',
      ua: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0',
      targetAccount: 'Anna Jenkins',
      targetRole: 'USR-DMO-107 · STUDENT (Grade 11)',
      endpoint: 'GET /api/auth/me',
      campus: 'Tuol Kork Secondary Perimeter',
      headers: `Host: api.ngis.edu.kh\\nX-RateLimit-Observed: 32 req / 60s\\nX-RateLimit-Budget: 30\\nConnection: keep-alive`
    }},
    'feed-auth-login': {{
      title: 'AUTHORIZED ADMINISTRATIVE ACCESS',
      badge: 'INFO (NOMINAL)',
      subtitle: 'VERIFIED CRYPTOGRAPHIC MFA HANDSHAKE',
      attackType: 'Privileged Sign-In Completed',
      action: '200 OK (Session Established)',
      time: '2024-11-17 18:32:45.012 UTC',
      waf: 'NGIS-AUTH-PROXY',
      srcIp: '127.0.0.1:51200',
      asn: 'AS13335 (Internal Bastion Proxy)',
      geo: 'Phnom Penh Admin Operations LAN',
      ua: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/122.0',
      targetAccount: 'demo-admin (Super Administrator)',
      targetRole: 'USR-SYS-001 · SUPER_ADMIN',
      endpoint: 'POST /api/auth/login',
      campus: 'Central Institutional Office',
      headers: `Host: api.ngis.edu.kh\\nX-Auth-Mechanism: FIDO2-WebAuthn\\nX-Session-Id: ses_982aef11\\nStatus: 200 SUCCESS`
    }},
    'anna-jenkins': {{
      title: 'ACCOUNT QUARANTINE RECORD',
      badge: 'RESTRICTED',
      subtitle: 'ACTIVE 24H SECURITY ISOLATION',
      attackType: 'Policy Violation & Multiple Failed Pins',
      action: 'Account Suspended (Banned 24h)',
      time: '2024-11-16 20:59:01 UTC',
      waf: 'NGIS-IAM-GATEKEEPER',
      srcIp: '203.0.113.66',
      asn: 'AS45435 (EZECOM Backbone)',
      geo: 'Phnom Penh, Cambodia',
      ua: 'Mobile Safari / iOS 17.4',
      targetAccount: 'Anna Jenkins',
      targetRole: 'USR-DMO-107 · STUDENT',
      endpoint: 'POST /api/auth/login',
      campus: 'Tuol Kork Main Campus',
      headers: `Ban Reason: UI E2E Validation / Burst Sign-In Failure\\nEnforced By: demo-admin\\nRevocation ID: REV-88219`
    }},
    'tuol-kork': {{
      title: 'CAMPUS GATEWAY NODE STATUS',
      badge: 'HEALTHY',
      subtitle: 'CORE PHYSICAL CAMPUS PERIMETER',
      attackType: 'Normal Campus Academic Traffic',
      action: 'Deep Packet Inspection: Pass',
      time: 'Live Continuous Monitor',
      waf: 'GW-TK-01',
      srcIp: '10.10.0.0/16 Subnet',
      asn: 'NGIS Private Campus WAN',
      geo: 'Tuol Kork Campus, Phnom Penh',
      ua: '1,420 Active Student & Faculty Devices',
      targetAccount: 'Institutional Student/Staff Pool',
      targetRole: 'ALL_CAMPUS_USERS',
      endpoint: 'All Academic APIs',
      campus: 'Tuol Kork Main Campus',
      headers: `Active Connections: 342\\nAverage Latency: 0.38 ms\\nWAF State: STRICT ACTIVE`
    }},
    'sensok': {{
      title: 'BRANCH GATEWAY NODE STATUS',
      badge: 'STAGING',
      subtitle: 'BRANCH SENSOR & RELAY NODE',
      attackType: 'Branch Connectivity Check',
      action: 'Proxy Pass Operational',
      time: 'Live Continuous Monitor',
      waf: 'GW-SS-02',
      srcIp: '10.20.0.0/16 Subnet',
      asn: 'NGIS Private Campus WAN',
      geo: 'Sen Sok Campus, Phnom Penh',
      ua: 'NGIS-Branch-Relay v1.2',
      targetAccount: 'Sensok Branch Infrastructure',
      targetRole: 'INFRASTRUCTURE',
      endpoint: 'All Branch Sync Endpoints',
      campus: 'Sensok Branch Campus',
      headers: `Active Connections: 14\\nAverage Latency: 1.12 ms\\nSync Status: Synchronized`
    }},
    'gateway': {{
      title: 'NGIS CENTRAL SHIELD GATEWAY',
      badge: 'CORE FIREWALL',
      subtitle: 'REVERSE PROXY & WAF FILTER CORE',
      attackType: 'Automated Token Bucket Filtering',
      action: 'Realtime Rate & Auth Interception',
      time: 'Continuous Operational Heartbeat',
      waf: 'NGIS-WAF v2.4.9',
      srcIp: '0.0.0.0:3000 / Ingress',
      asn: 'NGIS Infrastructure Core',
      geo: 'Kingdom of Cambodia',
      ua: 'NGIS-Shield-Engine/2.4.9',
      targetAccount: 'All School Portals',
      targetRole: 'CENTRAL_GATEWAY',
      endpoint: '/api/*',
      campus: 'Consolidated Gateway Core',
      headers: `Engine: NGIS-WAF v2.4.9\\nAlgorithms: Token Bucket + Leaky Bucket\\nActive Rules: 4\\nBlocked Today: 18`
    }}
  }};

  let activeForensicKey = 'node-unauthorized';

  // 1. Tab Switching Function
  function switchTab(tabId) {{
    document.querySelectorAll('.tab-pane').forEach(el => el.classList.add('hidden'));
    const target = document.getElementById(`tab-${{tabId}}`);
    if (target) target.classList.remove('hidden');

    document.querySelectorAll('.tab-btn').forEach(btn => {{
      if (btn.getAttribute('data-tab') === tabId) {{
        btn.className = 'tab-btn px-3 py-1.5 rounded-lg font-medium flex items-center space-x-2 bg-emerald-900 text-white shadow-xs';
      }} else {{
        btn.className = 'tab-btn px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 flex items-center space-x-1.5 transition font-medium';
      }}
    }});
  }}

  // 2. Open Forensic Inspector Side Drawer
  function openForensics(key) {{
    const data = forensicData[key] || forensicData['node-unauthorized'];
    activeForensicKey = key;

    const setTxt = (id, val) => {{
      const el = document.getElementById(id);
      if (el) el.textContent = val || '—';
    }};

    setTxt('inspTitle', data.title);
    setTxt('inspBadge', data.badge);
    setTxt('inspSubtitle', data.subtitle);
    setTxt('inspAttackType', data.attackType);
    setTxt('inspAction', data.action);
    setTxt('inspTime', data.time);
    setTxt('inspWaf', data.waf);
    setTxt('inspSrcIp', data.srcIp);
    setTxt('inspAsn', data.asn);
    setTxt('inspGeo', data.geo);
    setTxt('inspUa', data.ua);
    setTxt('inspTargetAccount', data.targetAccount);
    setTxt('inspTargetRole', data.targetRole);
    setTxt('inspEndpoint', data.endpoint);
    setTxt('inspCampus', data.campus);
    setTxt('inspHeaders', data.headers);

    const backdrop = document.getElementById('forensicBackdrop');
    if (backdrop) backdrop.classList.remove('hidden');
  }}

  function closeForensics() {{
    const backdrop = document.getElementById('forensicBackdrop');
    if (backdrop) backdrop.classList.add('hidden');
  }}

  // 3. One-Click Mitigation Trigger from Drawer
  function executeMitigation(type) {{
    const current = forensicData[activeForensicKey] || forensicData['node-unauthorized'];
    if (type === 'block') {{
      showNotice(`Firewall rule applied: Source IP ${{current.srcIp}} dropped for 48 hours. Logged to Audit History.`, 'warn');
    }} else if (type === 'suspend') {{
      showNotice(`Account Quarantine: ${{current.targetAccount}} suspended server-side. Immediate session invalidation triggered.`, 'error');
    }}
    closeForensics();
  }}

  function showNotice(msg, kind) {{
    try {{
      if (window.NGISUI && NGISUI.toast) {{
        NGISUI.toast(msg, kind || 'info');
        return;
      }}
    }} catch (e) {{}}
    alert(msg);
  }}

  // 4. Modal Helpers
  function openMitigateModal(target) {{
    const targetInput = document.getElementById('modalTarget');
    if (targetInput) targetInput.value = target || '127.0.0.1';
    const modal = document.getElementById('mitigateModal');
    if (modal) modal.classList.remove('hidden');
  }}

  function closeMitigateModal() {{
    const modal = document.getElementById('mitigateModal');
    if (modal) modal.classList.add('hidden');
  }}

  // 5. Fullscreen Radar Map Overlay Toggle
  function toggleFullscreenMap() {{
    const overlay = document.getElementById('fullscreenMapOverlay');
    if (overlay) {{
      overlay.classList.toggle('hidden');
    }}
  }}

  // 6. Live Clock Ticker
  function updateClock() {{
    const clock = document.getElementById('liveClock');
    if (clock) {{
      const now = new Date();
      clock.textContent = 'LIVE ' + now.toISOString().replace('T', ' ').slice(0, 19) + ' UTC';
    }}
  }}
  setInterval(updateClock, 1000);
  updateClock();

  // Close drawer on backdrop click
  const backdrop = document.getElementById('forensicBackdrop');
  if (backdrop) {{
    backdrop.addEventListener('click', function(e) {{
      if (e.target === this) closeForensics();
    }});
  }}

  // Close modal on backdrop click
  const modalEl = document.getElementById('mitigateModal');
  if (modalEl) {{
    modalEl.addEventListener('click', function(e) {{
      if (e.target === this) closeMitigateModal();
    }});
  }}

  // Escape key closes open overlays
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') {{
      closeForensics();
      closeMitigateModal();
      const overlay = document.getElementById('fullscreenMapOverlay');
      if (overlay && !overlay.classList.contains('hidden')) {{
        overlay.classList.add('hidden');
      }}
    }}
  }});

  // Set default view to Overview on boot
  document.addEventListener('DOMContentLoaded', function() {{
    switchTab('overview');
  }});
</script>
</body>
</html>
'''

with open(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\pages\admin\admin-security.html', 'w', encoding='utf-8') as out:
    out.write(full_html)

print("Successfully written pages/admin/admin-security.html, total size:", len(full_html))
