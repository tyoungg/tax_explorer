import asyncio
from playwright.async_api import async_playwright

async def check_for_errors():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        url = "http://localhost:8501"

        pages = ["Price_Endings", "Tax_Rate_Explorer", "County_Comparison"]
        for pg in pages:
            print(f"Checking {pg}...")
            await page.goto(f"{url}/{pg}", wait_until="networkidle")
            await asyncio.sleep(5)
            # Take a screenshot just in case
            await page.screenshot(path=f"debug_{pg}.png")

            # Look for red boxes (stException, stError)
            is_error = await page.query_selector(".stException") or await page.query_selector(".stError")
            if is_error:
                print(f"❌ Error found on {pg}:")
                print(await is_error.inner_text())
            else:
                print(f"✅ {pg} looks OK")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_for_errors())
