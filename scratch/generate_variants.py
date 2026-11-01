import asyncio
from playwright.async_api import async_playwright

async def generate_variants():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # Test 1: Deck with auto height / align-items: start, profile hugs content tightly
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="domcontentloaded")
        await page.wait_for_selector(".dash-overlap")
        await page.wait_for_timeout(500)
        
        await page.add_style_tag(content="""
            @media (min-width: 992px) {
              .dash-overlap {
                display: grid !important;
                grid-template-columns: 240px minmax(0, 1fr) 280px !important;
                gap: 16px !important;
                max-width: 1280px !important;
                margin: -48px auto 0 !important;
                padding: 0 24px !important;
                align-items: start !important;
              }
              .ov-profile {
                height: auto !important;
              }
              .ov-upcoming, .ov-deadlines {
                height: 330px !important;
                max-height: 330px !important;
              }
            }
            .ov-profile-header {
              padding: 14px 12px 10px !important;
            }
            .ov-avatar {
              width: 52px !important;
              height: 52px !important;
              margin: 0 auto 6px !important;
            }
            .ov-profile-name {
              font-size: 14px !important;
              margin: 0 0 2px !important;
            }
            .ov-profile-grade {
              font-size: 11px !important;
              margin-bottom: 4px !important;
            }
            .ov-profile-badge {
              font-size: 9.5px !important;
              padding: 1.5px 8px !important;
            }
            .ov-profile-body {
              padding: 8px 14px 4px !important;
              flex: 0 0 auto !important;
              gap: 0 !important;
            }
            .ov-info-row {
              padding: 4px 0 !important;
              font-size: 11px !important;
            }
            .ov-actions {
              margin-top: 10px !important;
              padding: 10px 14px !important;
            }
            .ov-btn-main {
              padding: 7px 8px !important;
              font-size: 11px !important;
            }
            .ov-btn-ic {
              width: 32px !important;
              height: 32px !important;
              min-width: 32px !important;
            }
            .ov-upcoming {
              padding: 12px 16px !important;
              display: flex !important;
              flex-direction: column !important;
            }
            .ov-card-head {
              margin-bottom: 6px !important;
            }
            .ov-inner-grid {
              gap: 12px !important;
              flex: 1 !important;
              min-height: 0 !important;
            }
            .ov-inner-head {
              font-size: 11px !important;
              padding-bottom: 3px !important;
              margin-bottom: 3px !important;
            }
            .ov-inner-item {
              padding: 2px 0 !important;
            }
            .ov-inner-item-t {
              font-size: 10.5px !important;
              line-height: 1.2 !important;
            }
            .ov-inner-item-s {
              font-size: 9.5px !important;
              margin-top: 0 !important;
            }
            .ov-upcoming [style*="max-height"] {
              max-height: 220px !important;
              height: 220px !important;
            }
            .ov-deadlines {
              padding: 12px 16px !important;
              display: flex !important;
              flex-direction: column !important;
            }
            .ov-deadline-panel {
              margin-bottom: 6px !important;
            }
            .ov-deadline-head {
              font-size: 11px !important;
              padding-bottom: 3px !important;
              margin-bottom: 3px !important;
            }
            .ov-deadline-item {
              padding: 3px 0 !important;
            }
            .ov-deadline-item-t {
              font-size: 10.5px !important;
              line-height: 1.2 !important;
            }
            .ov-deadline-item-s {
              font-size: 9.5px !important;
              margin-top: 0 !important;
            }
            .ov-tag {
              font-size: 8.5px !important;
              padding: 1px 6px !important;
              margin-left: 6px !important;
            }
        """)
        
        await page.screenshot(path="scratch/variant_a_compact.png")
        
        # Test 2: Profile card equal height with subtle stats or balanced padding (~330px)
        await page.add_style_tag(content="""
            @media (min-width: 992px) {
              .ov-profile {
                height: 330px !important;
                display: flex !important;
                flex-direction: column !important;
              }
              .ov-actions {
                margin-top: auto !important;
                padding: 12px 14px !important;
              }
              .ov-profile-body {
                padding: 10px 14px 6px !important;
              }
              .ov-info-row {
                padding: 5px 0 !important;
              }
            }
        """)
        await page.screenshot(path="scratch/variant_b_equal330.png")
        
        await browser.close()
        print("Generated variant_a_compact.png and variant_b_equal330.png")

asyncio.run(generate_variants())

