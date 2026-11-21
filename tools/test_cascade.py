import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000/pages/admin/admin-classes.html', wait_until='networkidle')
        
        # Add the responsive override
        await page.evaluate('''() => {
            const st = document.createElement('style');
            st.textContent = `
                @media (min-width: 640px) {
                    .sm\\\\:flex-row { flex-direction: row !important; }
                    .sm\\\\:items-center { align-items: center !important; }
                    .sm\\\\:items-end { align-items: flex-end !important; }
                    .sm\\\\:justify-between { justify-content: space-between !important; }
                }
                @media (min-width: 768px) {
                    .md\\\\:flex-row { flex-direction: row !important; }
                    .md\\\\:items-center { align-items: center !important; }
                    .md\\\\:items-end { align-items: flex-end !important; }
                    .md\\\\:justify-between { justify-content: space-between !important; }
                }
                @media (min-width: 1024px) {
                    .lg\\\\:flex-row { flex-direction: row !important; }
                    .lg\\\\:items-center { align-items: center !important; }
                    .lg\\\\:items-end { align-items: flex-end !important; }
                    .lg\\\\:justify-between { justify-content: space-between !important; }
                }
            `;
            document.head.appendChild(st);
        }''')
        
        await page.screenshot(path=r'C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536\test_admin_classes_fixed.png')
        print('Captured test_admin_classes_fixed.png')
        await browser.close()

asyncio.run(main())
