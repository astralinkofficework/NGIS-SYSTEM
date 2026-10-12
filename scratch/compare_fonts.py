html_content = '''<!DOCTYPE html>
<html>
<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&family=Outfit:wght@300;400;500&family=Plus+Jakarta+Sans:wght@300;400;500&family=Poppins:wght@300;400;500&family=Urbanist:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  body { background: #f0f2f5; padding: 20px; color: #1e293b; margin: 0; }
  .grid { display: flex; flex-direction: column; gap: 20px; }
  .sample { background: white; padding: 16px 20px; border-radius: 12px; }
  .name { font-size: 14px; color: #64748b; margin-bottom: 8px; font-family: monospace; }
  .t1 { font-size: 20px; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase; }
  .t2 { font-size: 26px; font-weight: 400; margin: 6px 0; }
  .t3 { font-size: 16px; font-weight: 500; }
  .t4 { font-size: 13px; font-weight: 400; }
</style>
</head>
<body>
<div class="grid">
  <div class="sample" style="font-family: 'Plus Jakarta Sans', sans-serif;">
    <div class="name">Plus Jakarta Sans (weight 400 & 500)</div>
    <div class="t1">Finance App</div>
    <div class="t2">$ 12,540.000</div>
    <div class="t3">Statistics &middot; Quick Action &middot; Upgrade Account</div>
    <div class="t4">NYC cab service &middot; Classes Attended &middot; 44 of 48 sessions on time</div>
  </div>
  <div class="sample" style="font-family: 'Outfit', sans-serif;">
    <div class="name">Outfit (weight 400 & 500)</div>
    <div class="t1">Finance App</div>
    <div class="t2">$ 12,540.000</div>
    <div class="t3">Statistics &middot; Quick Action &middot; Upgrade Account</div>
    <div class="t4">NYC cab service &middot; Classes Attended &middot; 44 of 48 sessions on time</div>
  </div>
  <div class="sample" style="font-family: 'Poppins', sans-serif;">
    <div class="name">Poppins (weight 400 & 500)</div>
    <div class="t1">Finance App</div>
    <div class="t2">$ 12,540.000</div>
    <div class="t3">Statistics &middot; Quick Action &middot; Upgrade Account</div>
    <div class="t4">NYC cab service &middot; Classes Attended &middot; 44 of 48 sessions on time</div>
  </div>
  <div class="sample" style="font-family: 'Urbanist', sans-serif;">
    <div class="name">Urbanist (weight 400 & 500)</div>
    <div class="t1">Finance App</div>
    <div class="t2">$ 12,540.000</div>
    <div class="t3">Statistics &middot; Quick Action &middot; Upgrade Account</div>
    <div class="t4">NYC cab service &middot; Classes Attended &middot; 44 of 48 sessions on time</div>
  </div>
  <div class="sample" style="font-family: 'Inter', sans-serif;">
    <div class="name">Inter (weight 400 & 500)</div>
    <div class="t1">Finance App</div>
    <div class="t2">$ 12,540.000</div>
    <div class="t3">Statistics &middot; Quick Action &middot; Upgrade Account</div>
    <div class="t4">NYC cab service &middot; Classes Attended &middot; 44 of 48 sessions on time</div>
  </div>
</div>
</body>
</html>'''

with open('scratch/font_compare.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 800, 'height': 900})
    page.goto('file:///' + 'c:/Users/oudom/OneDrive/Desktop/NGIS-SYSTEM/scratch/font_compare.html'.replace('\\', '/'))
    page.wait_for_timeout(2000)
    page.screenshot(path='scratch/font_compare.png', full_page=True)
    browser.close()
print('Comparison saved to scratch/font_compare.png')
