import asyncio
from playwright.async_api import async_playwright

VIEWPORTS = [
    (1440, 900, "desktop_1440"),
    (1024, 768, "laptop_1024"),
    (820, 1180, "tablet_820"),
    (768, 1024, "tablet_768"),
    (390, 844, "mobile_390"),
    (360, 800, "mobile_360")
]

PAGES = [
    ('http://127.0.0.1:3000/pages/student/student.html', 'Student Dashboard'),
    ('http://127.0.0.1:3000/pages/teacher/teacher.html', 'Teacher Dashboard'),
    ('http://127.0.0.1:3000/pages/teacher/teacher-departments.html', 'Teacher Departments'),
    ('http://127.0.0.1:3000/pages/shared/department.html', 'Shared Department Hub')
]

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        all_passed = True
        
        for url, name in PAGES:
            print(f"\n==========================================")
            print(f"Testing {name}: {url}")
            print(f"==========================================")
            
            for width, height, vp_name in VIEWPORTS:
                await page.set_viewport_size({'width': width, 'height': height})
                await page.goto(url, wait_until='networkidle')
                
                # Check horizontal overflow
                overflow_info = await page.evaluate('''() => {
                    return {
                        scrollWidth: document.documentElement.scrollWidth,
                        innerWidth: window.innerWidth,
                        bodyScrollWidth: document.body.scrollWidth,
                        hasOverflow: document.documentElement.scrollWidth > window.innerWidth
                    };
                }''')
                
                status = "PASS" if not overflow_info['hasOverflow'] else "FAIL"
                if overflow_info['hasOverflow']:
                    all_passed = False
                    print(f"  [{vp_name} - {width}px] OVERFLOW: scrollWidth={overflow_info['scrollWidth']}, innerWidth={overflow_info['innerWidth']}")
                else:
                    print(f"  [{vp_name} - {width}px] Overflow Check: {status} ({overflow_info['scrollWidth']}px / {overflow_info['innerWidth']}px)")
            
            # Check font weights
            heavy_fonts = await page.evaluate('''() => {
                const heavy = [];
                const all = document.querySelectorAll('*');
                for (let el of all) {
                    const fw = window.getComputedStyle(el).fontWeight;
                    const num = parseInt(fw, 10);
                    if (num > 500) {
                        heavy.push({
                            tag: el.tagName,
                            class: el.className,
                            weight: fw,
                            text: el.innerText ? el.innerText.slice(0, 30) : ''
                        });
                        if (heavy.length >= 5) break;
                    }
                }
                return heavy;
            }''')
            
            if heavy_fonts:
                print(f"  [CRITICAL RULE] Heavy fonts found (> 500): {len(heavy_fonts)} samples: {heavy_fonts}")
            else:
                print(f"  [CRITICAL RULE] Strict Font-Weight <= 500 Check: PASS (Zero heavy fonts)")
                
        await browser.close()
        print(f"\nFinal Verification Status: {'ALL PASSED!' if all_passed else 'SOME ISSUES REMAIN'}")

if __name__ == '__main__':
    asyncio.run(verify())

