import re

path = 'pages/principal/principal-reports.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update grade badge styles to strict 5-color palette
content = re.sub(
    r'\.grade-a\s*\{[^}]*\}',
    '.grade-a { background:#F3F3F5; color:#202F63; border:1px solid #E5E5E8; }',
    content
)
content = re.sub(
    r'\.grade-b\s*\{[^}]*\}',
    '.grade-b { background:#F3F3F5; color:#000000; border:1px solid #E5E5E8; }',
    content
)

# 2. Update stat icon classes
content = content.replace('<div class="stat-ico t-blue">', '<div class="stat-ico" style="background:#F3F3F5;color:#202F63">')
content = content.replace('<div class="stat-ico t-green">', '<div class="stat-ico" style="background:#F3F3F5;color:#000000">')
content = content.replace('<div class="stat-ico t-purple">', '<div class="stat-ico" style="background:#F3F3F5;color:#202F63">')
content = content.replace('<div class="stat-ico t-amber">', '<div class="stat-ico" style="background:#F3F3F5;color:#000000">')

# 3. Clean trend up & badge colors
content = content.replace('<span class="trend up">', '<span class="trend" style="background:#F3F3F5;color:#202F63;border:1px solid #E5E5E8;padding:2px 8px;border-radius:6px;font-size:11px;font-weight:500">')
content = content.replace('<span class="badge green">Term Active · AY 2025–26</span>', '<span class="badge" style="background:#F3F3F5;color:#202F63;border:1px solid #E5E5E8">Term Active &middot; AY 2025–26</span>')
content = content.replace('<span class="badge blue">Exceeding Benchmark</span>', '<span class="badge" style="background:#F3F3F5;color:#202F63;border:1px solid #E5E5E8">Exceeding Benchmark</span>')
content = content.replace('<span class="badge green">On Target</span>', '<span class="badge" style="background:#F3F3F5;color:#000000;border:1px solid #E5E5E8">On Target</span>')
content = content.replace('<span class="badge green">95.8%</span>', '<span class="badge" style="background:#F3F3F5;color:#000000;border:1px solid #E5E5E8">95.8%</span>')
content = content.replace('<span class="badge green" id="g11AttBadge">96.7%</span>', '<span class="badge" style="background:#F3F3F5;color:#202F63;border:1px solid #E5E5E8" id="g11AttBadge">96.7%</span>')
content = content.replace('<span class="badge green">97.2%</span>', '<span class="badge" style="background:#F3F3F5;color:#000000;border:1px solid #E5E5E8">97.2%</span>')

# 4. Update loadExecutiveReportMetrics to use /api/principal/stats and /api/academic/admin/oversight
new_loader = '''async function loadExecutiveReportMetrics() {
  try {
    const statRes = await fetch('/api/principal/stats');
    if (statRes.ok) {
      const stats = await statRes.json();
      if (stats.averageGpa && document.getElementById('repAvgGpa')) {
        document.getElementById('repAvgGpa').textContent = Number(stats.averageGpa).toFixed(2);
      }
      if (stats.publishedGrades && document.getElementById('repPublishedGrades')) {
        document.getElementById('repPublishedGrades').textContent = stats.publishedGrades;
      }
      if (stats.attendanceRate && document.getElementById('repAttRate')) {
        document.getElementById('repAttRate').textContent = stats.attendanceRate;
        const g11 = document.getElementById('g11AttBadge');
        if (g11) g11.textContent = stats.attendanceRate;
      }
      if (stats.honorsRate && document.getElementById('repHonorRoll')) {
        document.getElementById('repHonorRoll').textContent = stats.honorsRate;
      }
    }
  } catch (err) {
    console.warn('Fallback loading oversight metrics:', err);
  }
}'''

content = re.sub(r'async function loadExecutiveReportMetrics\(\) \{.*?\}', new_loader, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Principal reports page upgraded successfully.")

