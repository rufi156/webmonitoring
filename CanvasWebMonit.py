import requests
from bs4 import BeautifulSoup
import hashlib
import time
from datetime import datetime
from discordwebhook import Discord

DISCORD_WEBHOOK_URL = ''
with open('webhook.txt', 'r') as f:
    DISCORD_WEBHOOK_URL = f.readline()

WEBSITE_URL = 'https://canvas-student.securerc.co.uk/onlineleasing/canvas-utrecht/floorplans.aspx'

SELECTOR = 'DIV#CustMsgDivBottom H3'

# Function to get the MD5 hash of a specific element's text content using requests and BeautifulSoup
def get_specific_element_text(url, selector):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        specific_element = soup.select_one(selector)

        if specific_element:
            return specific_element.text.strip()
        else:
            print(f'Error: Element {selector} not found on the page')
            return None
    else:
        print(f'Error: {response.status_code}')
        return None

if __name__ == "__main__":
    discord = Discord(url=DISCORD_WEBHOOK_URL)

    # Initial request before entering the loop
    initial_text = get_specific_element_text(WEBSITE_URL, SELECTOR)

    while True:
        current_text = get_specific_element_text(WEBSITE_URL, SELECTOR)

        if not current_text:
            print(f"{datetime.now()} Error: Cannot retrieve specified element on website.\n")
            discord.post(content=f'Error: Cannot retrieve specified element on website {WEBSITE_URL}') 

        elif current_text != initial_text:
            print(f"{datetime.now()} Website changed!\n")
            discord.post(content=f'Website changed!\n Initial text: {initial_text}\n Current text: {current_text}')

        else:
            #discord.post(content=f'Same old same old\n"{current_text}"')
            print(f"{datetime.now()} Same old same old...", end='\r')
        
        time.sleep(30*60)
