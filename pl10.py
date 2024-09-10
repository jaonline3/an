import asyncio
from playwright.async_api import async_playwright
import requests

async def main():
    # Open a browser and navigate to an IP-checking site
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for i in range(100):  # Loop to check IP 100 times
            # Visit an IP-checking service
            await page.goto('https://httpbin.org/ip')

            # Extract the IP information from the page
            content = await page.text_content('pre')
            print(f"{i + 1}: Detected IP from Playwright: {content.strip()}")

        # Close the browser
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
