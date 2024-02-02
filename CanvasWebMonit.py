import requests
import hashlib
import time
from discordwebhook import Discord

DISCORD_WEBHOOK_URL = ''
with open('webhook.txt', 'r') as f:
    DISCORD_WEBHOOK_URL = f.readline()

DISCORD = Discord(url=DISCORD_WEBHOOK_URL)

WEBSITE_URL = 'https://canvas-student.securerc.co.uk/onlineleasing/canvas-utrecht/floorplans.aspx'

# Function to get the MD5 hash of a webpage content
def get_page_hash(url):
    response = requests.get(url)
    if response.status_code == 200:
    # Save the HTML content to a file
        with open('output.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        print('HTML content saved to output.html')
    else:
        print(f'Error: {response.status_code}')
    return hashlib.md5(response.content).hexdigest()

if __name__ == "__main__":

    current_hash = get_page_hash(WEBSITE_URL)

    while True:
        # Fetch the current hash value
        new_hash = get_page_hash(WEBSITE_URL)

        # Check for changes
        #if new_hash != current_hash:
        if new_hash == current_hash:
            DISCORD.post(content=f'Website content not changed: {WEBSITE_URL}')
            #current_hash = new_hash

        # Wait for 30 minutes before checking again
        #time.sleep(1800)
        break
