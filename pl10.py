import asyncio
from playwright.async_api import async_playwright

async def main():
    # Open a browser and navigate to an IP-checking site through Tor proxy
    async with async_playwright() as p:
        # Configure browser to use Tor's SOCKS5 proxy
        browser = await p.chromium.launch(headless=True, proxy={"server": "socks5://127.0.0.1:9050"})
        page = await browser.new_page()

        # Visit an IP-checking service
        await page.goto('https://httpbin.org/ip')

        # Extract the IP information from the page
        content = await page.text_content('pre')
        print("Detected IP from Playwright via Tor:", content)

        # Close the browser
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
