import asyncio
from playwright.async_api import async_playwright

async def main():
    uniswap_url = "https://app.uniswap.org/swap"

    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(uniswap_url)
        inputs = page.get_by_placeholder('0')

        print(len(await inputs.all()))

        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
