import hashlib
import time
from discordwebhook import Discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DISCORD_WEBHOOK_URL = ''
with open('webhook.txt', 'r') as f:
    DISCORD_WEBHOOK_URL = f.readline()

WEBSITE_URL = 'https://canvas-student.securerc.co.uk/onlineleasing/canvas-utrecht/floorplans.aspx'

# Function to get the MD5 hash of a webpage content using Selenium
def get_page_hash(url, save_to_file=False, filename='output.html'):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        # Wait for dynamic content to load (adjust the sleep duration accordingly)
        time.sleep(5)
        page_content = driver.page_source.encode('utf-8')
        current_hash = hashlib.md5(page_content).hexdigest()

        # Save the content to a file if specified
        if save_to_file:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(driver.page_source)

        return current_hash
    finally:
        driver.quit()

if __name__ == "__main__":
    discord = Discord(url=DISCORD_WEBHOOK_URL)
    print(DISCORD_WEBHOOK_URL)
    print(discord)

    # Initial request before entering the loop
    initial_hash = get_page_hash(WEBSITE_URL, save_to_file=True, filename='initial_output.html')

    while True:
        current_hash = get_page_hash(WEBSITE_URL, save_to_file=True, filename='current_output.html')

        if not current_hash: discord.post(content=f'Error: Cannot retrieve website {WEBSITE_URL}')
        
        if current_hash != initial_hash:
            discord.post(content=f'Website content changed: {WEBSITE_URL}')
        else:
            discord.post(content=f'Website content not changed: {WEBSITE_URL}')

        #time.sleep(1800)
        break
