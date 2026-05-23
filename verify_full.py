import asyncio
from playwright.async_api import async_playwright
import os

async def verify_pages():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Base URL for Streamlit
        url = "http://localhost:8501"

        pages_to_check = [
            "", # Main page
            "Single_Transaction",
            "Price_Endings",
            "Tax_Rate_Explorer",
            "County_Comparison",
            "Monte_Carlo",
            "Shelf_Price_Optimizer",
            "Heatmaps",
            "Methodology"
        ]

        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        for p_name in pages_to_check:
            target_url = f"{url}/{p_name}"
            print(f"Checking {target_url}...")
            try:
                await page.goto(target_url, wait_until="networkidle", timeout=10000)
                await asyncio.sleep(3) # Wait for Streamlit to finish rendering

                # Check for common error indicators
                content = await page.content()
                if "Traceback" in content or "Exception" in content or "Error:" in content:
                    print(f"❌ Error detected on page: {p_name}")
                    # Find the error text
                    errors = await page.query_selector_all(".stException, .stAlert")
                    for err in errors:
                        print(f"Error detail: {await err.inner_text()}")
                else:
                    print(f"✅ Page {p_name} looks OK.")

                await page.screenshot(path=f"screenshots/{p_name or 'home'}.png")
            except Exception as e:
                print(f"Failed to check {p_name}: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_pages())
