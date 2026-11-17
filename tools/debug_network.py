import asyncio
from playwright.async_api import async_playwright

async def check_page(url):
    print(f"\n--- Checking {url} ---")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        page.on("console", lambda msg: print(f"  CONSOLE [{msg.type}]: {msg.text}"))
        page.on("response", lambda res: print(f"  RESPONSE {res.status}: {res.url}") if res.status >= 400 else None)

        try:
            await page.goto(url, wait_until="networkidle", timeout=15000)
        except Exception as e:
            print("  Exception:", e)
        await page.wait_for_timeout(2000)
        await browser.close()

async def main():
    await check_page("http://127.0.0.1:3000/pages/principal/principal.html")
    await check_page("http://127.0.0.1:3000/pages/teacher/teacher.html")

if __name__ == "__main__":
    asyncio.run(main())
