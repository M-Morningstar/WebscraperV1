import asyncio
import csv
from playwright.async_api import async_playwright
import os, time, re, random
from fake_useragent import UserAgent

# Function to create a random delay between requests
def random_delay():
    return random.randint(2000, 5000) / 1000

async def scrape_product(playwright, product_id, countries):
    browser = await playwright.chromium.launch()

    product_dir = os.path.join(os.getcwd(), product_id)
    os.makedirs(product_dir, exist_ok=True)

    for country_code, (currency, country_name) in countries.items():
        user_agent = UserAgent(platforms='pc')

        context = await browser.new_context(user_agent=user_agent.random)
        page = await context.new_page()

        try:
            url = f'https://www.amazon.{country_code}/dp/{product_id}?language=en_GB'
            print(f'Scraping: {url}')

            await page.goto(url)
            html = await page.content()

            # Save the html of the dynamic page to a file
            file_name = f'{country_name}_{currency}.html'
            file_path = os.path.join(product_dir, file_name)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(html)

            print(f'Successfully scraped: {url}')
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
        finally:
            await page.close()

        delay_time = random_delay()
        print(f'Waiting for {delay_time} seconds before next request...')
        time.sleep(delay_time)

    await browser.close()

def validate_product_id(product_id):
    # Make sure it's 10 characters long
    if len(product_id) != 10:
        print("Product ID must be exactly 10 characters.")
        return False
    
    # Ensure the product ID starts with 'B' and contains only uppercase letters and numbers
    if not re.match(r'^B[A-Z0-9]{9}$', product_id):
        print("Product ID must start with 'B' and contain only uppercase letters and numbers.")
        return False
    
    return True

def load_countries(file_path):
    countries = {}

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            countries[row['code']] = [row['currency'], row['name']]
    return countries

async def main():
    product_list = []

    countries = load_countries('countries.csv')

    while True:
        id = input("Please enter the Amazon Product code of the product you wish to compare prices for (q to quit): ")
        
        if id.lower() == 'q':
            break

        if validate_product_id(id):
            product_list.append(id)
            answer = input("Do you want to continue entering product IDs? (y/n): ")
            if answer.lower() == 'n':
                break
        else:
            print("Wrong format entered for the Amazon Product ID. Try Again!")

    if not product_list:
        print("No valid product IDs entered. Exiting the program.")
        return

    async with async_playwright() as p:
        tasks = [scrape_product(p, product_id, countries) for product_id in product_list]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())