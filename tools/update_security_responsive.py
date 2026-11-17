import re

with open(r'pages/admin/admin-security.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove duplicate mobile appbar header and replace the desktop header with the unified responsive header
# Currently:
#   <!-- Mandatory Mobile Appbar with Accessible Hamburger Menu (AGENTS.md Compliance) -->
#   <header class="mobile-appbar md:hidden flex items-center justify-between px-4 py-3 bg-white border-b border-slate-200 sticky top-0 z-40 min-h-[44px]">
#   ...
#   </header>
#
#   <!-- Hero Banner Anchor for layout.js -->
#   <header id="heroBanner" role="banner"></header>
#
#   <!-- Desktop & Tablet Executive Header & Tabs -->
#   <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs">
#   ...

old_header_pattern = re.compile(
    r'<!-- Mandatory Mobile Appbar with Accessible Hamburger Menu \(AGENTS\.md Compliance\) -->.*?'
    r'<header class="mobile-appbar md:hidden.*?</header>\s*'
    r'<!-- Hero Banner Anchor for layout\.js -->\s*'
    r'<header id="heroBanner" role="banner"></header>\s*'
    r'<!-- Desktop & Tablet Executive Header & Tabs -->\s*'
    r'<header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs">.*?'
    r'<div class="px-5 py-3\.5 flex flex-col md:flex-row md:items-center md:justify-between gap-3">.*?'
    r'</div>\s*<!-- Interactive Tab Bar Switcher -->',
    re.DOTALL
)

new_header_replacement = '''<!-- Hero Banner Anchor for layout.js -->
  <header id="heroBanner" role="banner"></header>

  <!-- Unified Responsive Executive Header & Mobile Appbar -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-xs">
    <div class="px-3.5 sm:px-5 py-2 sm:py-3 flex flex-col md:flex-row md:items-center md:justify-between gap-2 sm:gap-3">
      <!-- Brand & Mobile Appbar Row -->
      <div class="flex items-center justify-between w-full md:w-auto">
        <div class="flex items-center space-x-2 sm:space-x-3">
          <!-- Mandatory Accessible Mobile Hamburger Button (AGENTS.md Compliance) -->
          <button type="button" 
                  class="hamburger-btn mobile-hamburger-btn md:hidden p-2 -ml-1 rounded-xl text-slate-700 hover:bg-slate-100 active:scale-95 transition-all flex items-center justify-center min-w-[40px] min-h-[40px]" 
                  data-action="toggle-sidebar" 
                  aria-label="Open menu" 
                  aria-expanded="false" 
                  title="Open navigation">
            <i class="ph ph-list text-xl text-slate-700"></i>
          </button>
          <div class="w-8 h-8 sm:w-9 sm:h-9 rounded-xl bg-emerald-900 text-white flex items-center justify-center font-medium font-mono text-xs sm:text-sm shadow-xs flex-shrink-0">
            SOC
          </div>
          <div>
            <div class="flex items-center space-x-1.5 sm:space-x-2 text-[10px] sm:text-[11px] font-medium text-emerald-800 tracking-wider uppercase">
              <span>NGIS</span>
              <span>•</span>
              <span class="truncate">Security &amp; Perimeter Command</span>
            </div>
            <h1 class="text-sm sm:text-base md:text-xl font-medium text-slate-900 tracking-tight flex items-center gap-1.5 sm:gap-2">
              Cyber Defense Operations Center
            </h1>
          </div>
        </div>

        <!-- Quick Enforce Button on Mobile View -->
        <div class="flex items-center gap-1.5 md:hidden">
          <button onclick="openMitigateModal('127.0.0.1')" class="px-2.5 py-1.5 bg-emerald-900 hover:bg-emerald-950 text-white rounded-lg text-xs font-medium shadow-xs flex items-center gap-1 transition active:scale-95">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            <span>Enforce</span>
          </button>
        </div>
      </div>

      <!-- Quick Global Actions on Desktop & Tablet -->
      <div class="hidden md:flex items-center space-x-2.5">
        <div class="flex items-center bg-slate-100 text-slate-700 px-3 py-1.5 rounded-lg font-mono text-[11px] border border-slate-200">
          <span class="w-2 h-2 rounded-full bg-emerald-500 mr-2 animate-ping"></span>
          <span id="liveClock">LIVE TELEMETRY ACTIVE</span>
        </div>
        <div class="relative">
          <select class="text-xs bg-slate-50 border border-slate-200 rounded-lg py-1.5 pl-3 pr-7 font-medium text-slate-700 focus:ring-1 focus:ring-emerald-800">
            <option selected="">Last 24 hours</option>
            <option>Last 6 hours</option>
            <option>Last 7 days</option>
          </select>
        </div>
        <button class="px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 rounded-lg text-xs font-medium text-slate-700 shadow-2xs flex items-center space-x-1.5 transition" onclick="location.reload()" title="Refresh Feed">
          <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          <span>Refresh</span>
        </button>
        <button class="px-3.5 py-1.5 bg-emerald-900 hover:bg-emerald-950 text-white rounded-lg text-xs font-medium shadow-xs flex items-center space-x-1.5 transition" onclick="openMitigateModal('127.0.0.1')">
          <svg class="w-3.5 h-3.5 text-emerald-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          <span>+ Enforce Rule</span>
        </button>
      </div>
    </div>

    <!-- Interactive Tab Bar Switcher -->'''

if old_header_pattern.search(html):
    html = old_header_pattern.sub(new_header_replacement, html, count=1)
    print("Unified Header replaced successfully!")
else:
    print("WARNING: Header pattern did not match directly, let's debug")

# 2. Make Tab Bar horizontally scrollable with min-w-max on nav
html = html.replace(
    '<div class="px-5 border-t border-slate-100 overflow-x-auto bg-slate-50/60">\n    <nav class="flex space-x-1 sm:space-x-3 text-xs font-medium py-1.5" id="navTabs">',
    '<div class="px-3 sm:px-5 border-t border-slate-100 overflow-x-auto bg-slate-50/70 no-scrollbar">\n    <nav class="flex space-x-1 sm:space-x-2 text-xs font-medium py-1.5 min-w-max" id="navTabs">'
)

# 3. Main container responsive padding
html = html.replace(
    '<div class="page flex-1 max-w-7xl w-full mx-auto p-3 sm:p-5 lg:p-6 space-y-6">',
    '<div class="page flex-1 max-w-7xl w-full mx-auto p-3 sm:p-5 lg:p-6 space-y-4 sm:space-y-6">'
)

# 4. KPI cards in tab-overview: change to 2 columns on mobile
html = html.replace(
    '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">',
    '<div class="grid grid-cols-2 lg:grid-cols-4 gap-2.5 sm:gap-4">'
)

# 5. KPI card paddings and text sizes for mobile
html = re.sub(
    r'<div class="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs">',
    r'<div class="bg-white rounded-xl border border-slate-200 p-3 sm:p-4 shadow-2xs">',
    html
)
html = re.sub(
    r'<div class="text-2xl font-medium text-slate-900 mt-1">',
    r'<div class="text-xl sm:text-2xl font-medium text-slate-900 mt-1">',
    html
)

# 6. Radar subheader responsive wrapping
html = html.replace(
    '<div class="px-5 py-3 bg-slate-950/95 border-b border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs font-mono">',
    '<div class="px-3.5 sm:px-5 py-2.5 sm:py-3 bg-slate-950/95 border-b border-slate-800 flex flex-wrap items-center justify-between gap-2 sm:gap-3 text-xs font-mono">'
)

# 7. Radar map viewport height on mobile
html = html.replace(
    '<div class="relative w-full h-[200px] flex items-center justify-center p-2 radar-grid">',
    '<div class="relative w-full h-[170px] sm:h-[200px] flex items-center justify-center p-2 radar-grid overflow-hidden">'
)

# 8. Intercept feed border on mobile stack
html = html.replace(
    '<div class="lg:col-span-4 p-4 bg-slate-950/70 flex flex-col justify-between">',
    '<div class="lg:col-span-4 p-3.5 sm:p-4 bg-slate-950/70 flex flex-col justify-between border-t lg:border-t-0 lg:border-l border-slate-800">'
)

# 9. Drawer responsiveness
html = html.replace(
    '<div class="bg-slate-900 border-l border-slate-700 w-full max-w-xl h-full shadow-2xl flex flex-col text-slate-100 overflow-hidden transform transition-all" id="forensicDrawer">',
    '<div class="bg-slate-900 border-l border-slate-700 w-full sm:max-w-xl h-full shadow-2xl flex flex-col text-slate-100 overflow-hidden transform transition-all" id="forensicDrawer">'
)
html = html.replace(
    '<div class="p-5 bg-slate-950 border-t border-slate-800 flex gap-3">',
    '<div class="p-3.5 sm:p-5 bg-slate-950 border-t border-slate-800 flex flex-col sm:flex-row gap-2.5 sm:gap-3">'
)

# 10. Modal max height on mobile
html = html.replace(
    '<div class="bg-white rounded-2xl max-w-md w-full shadow-2xl border border-slate-200 overflow-hidden">',
    '<div class="bg-white rounded-2xl max-w-md w-full shadow-2xl border border-slate-200 overflow-hidden max-h-[92vh] flex flex-col">'
)

with open(r'pages/admin/admin-security.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated pages/admin/admin-security.html successfully!")
