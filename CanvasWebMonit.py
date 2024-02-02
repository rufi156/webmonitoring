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
def get_page_hash(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        # Wait for dynamic content to load (adjust the sleep duration accordingly)
        time.sleep(5)
        page_content = driver.page_source.encode('utf-8')
        return hashlib.md5(page_content).hexdigest()
    finally:
        driver.quit()

if __name__ == "__main__":
    discord = Discord(url=DISCORD_WEBHOOK_URL)

    # Initial request before entering the loop
    initial_hash = get_page_hash(WEBSITE_URL)

    # Save the initial HTML to a file
    with open('initial_output.html', 'w', encoding='utf-8') as file:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        try:
            driver.get(WEBSITE_URL)
            file.write(driver.page_source)
        finally:
            driver.quit()

    while True:
        current_hash = get_page_hash(WEBSITE_URL)

        if current_hash and current_hash != initial_hash:
            discord.post(content=f'Website content changed: {WEBSITE_URL}')
            # No need to update the initial hash/template

        time.sleep(1800)
