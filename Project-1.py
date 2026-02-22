
import sys
import requests
from bs4 import BeautifulSoup


if (len(sys.argv) < 2):
    print("Invalid Command, add website.")
    sys.exit()

url = sys.argv[1]

try:
    response = requests.get(url)

    if(response.status_code != 200):
        print("Unable to fetch webpage.")
        sys.exit()
    
    print(response)

except request.RequestException:
    print("Failed to fetch webpage.")
    sys.exit()

html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

print("\n")
title_tag = soup.find('title')
if title_tag:
    print("Title of the webpage - ",title_tag.get_text())
else:
    print("No Title Found")

print("\n")
print("Body of page - \n ", soup.get_text())

print("Links present on the webpage - ")
links = soup.find_all('a')
if links:
    for link in links:
        print(link.get('href'))
else:
    print("No links found")

