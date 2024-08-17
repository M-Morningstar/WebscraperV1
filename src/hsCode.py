# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options

# class HSCode:

#     def __init__(self, country, description):
#         self.country = country
#         self.description = description

#     def findCode(self):
#         print(f'Looking up the HS Code for {self.country}...')
#         # Path to the chromedriver
#         chromedriver_path = '/usr/local/bin/chromedriver'

#         chrome_options = Options()
#         chrome_options.add_argument("--headless")  # Run in headless mode
#         chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
#         chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
#         chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

#         # Initialize the WebDriver
#         service = Service(executable_path=chromedriver_path)
#         driver = webdriver.Chrome(service=service, options=chrome_options)

#         # Open the website
#         driver.get('https://www.canadapost-postescanada.ca/information/app/wtz/business/findHsCode?execution=e1s1')

#         try:
#             # Wait for the page to load
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'findHsCode_tz0001:selectDestination')))  # ID of the drop-down

#             # Close cookie banner or overlay if it exists
#             # Close cookie banner if it exists
#             try:
#                 cookie_accept_button = WebDriverWait(driver, 5).until(
#                     EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
#                 )
#                 cookie_accept_button.click()
#             except TimeoutException:
#                 pass

#             # Select destination from the drop-down menu
#             select_element = Select(driver.find_element(By.ID, 'findHsCode_tz0001:selectDestination'))  # ID of the drop-down
#             select_element.select_by_visible_text(self.country)  # Text of the option

#             WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'findHsCode_tz0001:productDescription')))  # Replace with actual ID of the text box
#             item_description_field = driver.find_element(By.ID, 'findHsCode_tz0001:productDescription')  # Replace with actual ID of the text box

#             # Clear any pre-filled text and enter item description
#             item_description_field.clear()
#             item_description_field.send_keys(self.description)  # Replace with the actual item description

#             # Click the "Find" button
#             find_button = driver.find_element(By.ID, 'findHsCode_tz0001:searchButton')  # ID of the button
#             find_button.click()

#             try:
#                 while True:
#                     next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'findHsCode_tz0003:searchButton')))
#                     next_button.click()
#                     time.sleep(1)  # Small delay to allow the page to load new content
#             except TimeoutException:
#                 # If the button is not found, assume there are no more pages
#                 pass

#             # Wait for the results page to load and display the results
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'results')))  # Replace with actual ID of the result element

#             # Extract the HS code from the results page
#             results_div = driver.find_element(By.ID, 'results')
#             hs_code_element = results_div.find_element(By.XPATH, './/b[contains(text(), "HS Code:")]/..')
#             hs_code = hs_code_element.text.split(":")[1].strip()

#             return hs_code

#         except TimeoutException:
#             print('Loading took too much time or an element was not found.')
#             return None

#         finally:
#             print('Done!')
#             # Close the WebDriver
#             driver.quit()

# # Code that will only run when this script is executed directly from terminal for example
# if __name__ == "__main__":
#     code = HSCode('Turkey', "Board Game")
#     tariffCode = code.findCode()
#     print(f'The HS code for the given item is: {tariffCode}')




import asyncio
from playwright.async_api import async_playwright, TimeoutError

class HSCode:

    def __init__(self, country, description):
        self.country = country
        self.description = description

    async def findCode(self):
        print(f'Looking up the HS Code for {self.country}...')

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            # Open the website
            await page.goto('https://www.canadapost-postescanada.ca/information/app/wtz/business/findHsCode?execution=e1s1')

            try:
                # Wait for the page to load and select the country
                await page.wait_for_selector('#findHsCode_tz0001\\:selectDestination')
                
                # Close cookie banner if it exists
                try:
                    cookie_accept_button = await page.wait_for_selector('#onetrust-accept-btn-handler', timeout=5000)
                    await cookie_accept_button.click()
                except TimeoutError:
                    pass

                # Select destination from the drop-down menu
                await page.select_option('#findHsCode_tz0001\\:selectDestination', label=self.country)

                # Wait for the item description field and fill it in
                await page.wait_for_selector('#findHsCode_tz0001\\:productDescription')
                item_description_field = await page.query_selector('#findHsCode_tz0001\\:productDescription')
                await item_description_field.fill(self.description)

                # Click the "Find" button
                find_button = await page.query_selector('#findHsCode_tz0001\\:searchButton')
                await find_button.click()

                try:
                    while True:
                        next_button = await page.wait_for_selector('#findHsCode_tz0003\\:searchButton', timeout=5000)
                        await next_button.click()
                        await asyncio.sleep(1)  # Small delay to allow the page to load new content
                except TimeoutError:
                    # If the button is not found, assume there are no more pages
                    pass

                # Wait for the results page to load and display the results
                await page.wait_for_selector('#results')

                # Extract the HS code from the results page
                results_div = await page.query_selector('#results')
                hs_code_element = await results_div.query_selector('xpath=//b[contains(text(), "HS Code:")]/..')
                hs_code = (await hs_code_element.text_content()).split(":")[1].strip()

                return hs_code

            except TimeoutError:
                print('Loading took too much time or an element was not found.')
                return None

            finally:
                print('Done!')
                await browser.close()

# Code that will only run when this script is executed directly from terminal for example
if __name__ == "__main__":
    code = HSCode('Turkey', "Board Game")
    tariffCode = asyncio.run(code.findCode())
    print(f'The HS code for the given item is: {tariffCode}')
