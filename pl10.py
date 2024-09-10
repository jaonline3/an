from playwright.sync_api import sync_playwright
import time

# Function to initialize Playwright and configure Tor proxy
def get_hotel_data_with_tor(url):
    with sync_playwright() as p:
        # Launch a browser instance with Tor proxy
        browser = p.chromium.launch(proxy={"server": "socks5://127.0.0.1:9050"})  # Tor's default SOCKS5 proxy address
        context = browser.new_context()
        page = context.new_page()

        try:
            # Navigate to the URL
            page.goto(url)

            # Wait for the page to load and for the target element to be present
            page.wait_for_selector('h2.d2fee87262.pp-header__title', timeout=10000)

            # Allow some time for the page to fully load
            time.sleep(6)
            
            # Scroll to the bottom of the page to ensure all elements are loaded
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(6)
            
            # Find the "data" button and click it
            data_button = page.locator('(//div[@class="f73e6603bf"])[2]')
            data_button.click()

            # Wait for any updates or changes after the click
            time.sleep(6)
            
            # Print confirmation of the click
            print("Data button clicked successfully.")
            
            # Extract dates and prices
            dates = []
            prices = []
            main_elements = page.locator('//tbody[1]//tr/td')

            for main_element in main_elements:
                try:
                    date_elem = main_element.locator('./span')
                    price_elem = main_element.locator('./span/div/span')
                    
                    # Extract date and price text
                    date_text = date_elem.inner_text() if date_elem.is_visible() else ""
                    price_text = price_elem.inner_text() if price_elem.is_visible() else ""
                    
                    if date_text and price_text:
                        dates.append(date_text)
                        prices.append(price_text)
                except Exception as e:
                    print(f"Error extracting data from element: {e}")
            
            # Print extracted data
            print("Dates:", dates)
            print("Prices:", prices)
            
            # Alternatively, print specific data like hotel name
            hotel_name = page.locator('h2.d2fee87262.pp-header__title').inner_text()
            print(f"Hotel name: {hotel_name}")

        except Exception as e:
            print(f"Error occurred: {e}")

        finally:
            browser.close()

# Example usage
if __name__ == "__main__":
    url = 'https://www.booking.com/hotel/gb/clayton-city-of-london.html'  # Replace with the actual hotel URL
    get_hotel_data_with_tor(url)
