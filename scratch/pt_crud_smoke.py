import asyncio
import json
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

URL = 'http://127.0.0.1:3000/pages/principal/principal-teachers.html'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:200]))

        await page.goto(URL, wait_until='networkidle')
        await page.wait_for_timeout(1000)
        rows0 = await page.evaluate("document.querySelectorAll('#faculty-table-body tr').length")
        print('initial rows:', rows0)

        # 1. View profile of first teacher
        await page.click('#faculty-table-body tr:first-child button[title="View teacher profile"]')
        await page.wait_for_timeout(300)
        prof = await page.evaluate("""({
          open: !document.getElementById('profileModal').classList.contains('hidden'),
          name: document.getElementById('pmName').textContent,
          email: document.getElementById('pmEmail').textContent,
        })""")
        print('profile modal:', json.dumps(prof))
        await page.screenshot(path='scratch/pt_profile.png')
        await page.click('#profileModal button[onclick="closeProfileModal()"]')

        # 2. Add teacher via form (server-backed)
        await page.click('button:has-text("Add Teacher")')
        await page.wait_for_timeout(200)
        await page.fill('#tfName', 'Chanthy Oeung')
        await page.fill('#tfSubject', 'Chemistry')
        await page.select_option('#tfDepartment', 'STEM')
        await page.fill('#tfEmail', 'chanthy.oeung@ngis.edu.kh')
        await page.fill('#tfClasses', '3')
        await page.fill('#tfYears', '5')
        await page.click('#tfmSubmitBtn')
        await page.wait_for_timeout(1200)
        rows1 = await page.evaluate("document.querySelectorAll('#faculty-table-body tr').length")
        hasNew = await page.evaluate("facultyData.some(f => f.email === 'chanthy.oeung@ngis.edu.kh')")
        serverHas = await page.evaluate("""async () => {
          const r = await NGISAuth.api('/api/principal/roster/teachers');
          return (r.data || []).some(t => t.email === 'chanthy.oeung@ngis.edu.kh');
        }""")
        print('after add: rows', rows0, '->', rows1, '| local has new:', hasNew, '| server has new:', serverHas)
        newId = await page.evaluate("(facultyData.find(f => f.email === 'chanthy.oeung@ngis.edu.kh') || {}).id")
        print('new teacher id:', newId)

        # switch filter to ALL so the new (CLEARED) row is visible
        await page.select_option('#status-filter', 'ALL')
        await page.evaluate("renderFacultyTable()")

        # 3. Edit the new teacher (subject -> Molecular Science) via edit icon on its row
        await page.click(f'#faculty-table-body tr[data-id="{newId}"] button[title="Edit teacher record"]')
        await page.wait_for_timeout(300)
        title = await page.evaluate("document.getElementById('tfmTitle').textContent")
        await page.fill('#tfSubject', 'Molecular Science')
        await page.click('#tfmSubmitBtn')
        await page.wait_for_timeout(1200)
        edited = await page.evaluate(f"facultyData.find(f => f.id === '{newId}').subject")
        serverEdited = await page.evaluate("""async () => {
          const r = await NGISAuth.api('/api/principal/roster/teachers');
          const t = (r.data || []).find(x => x.id === '%s');
          return t ? t.subject : null;
        }""" % newId)
        print('edit modal title:', title)
        print('after edit: local subject =', edited, '| server subject =', serverEdited)
        await page.screenshot(path='scratch/pt_after_crud.png')

        # 4. Status filter still works, new row shows
        await page.select_option('#status-filter', 'ALL')
        await page.evaluate("renderFacultyTable()")
        rows2 = await page.evaluate("document.querySelectorAll('#faculty-table-body tr').length")
        print('rows with ALL filter:', rows2)

        print('page errors:', errs or 'NONE')
        await browser.close()

asyncio.run(main())
