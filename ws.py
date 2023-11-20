from bs4 import BeautifulSoup
import requests


url = "https://u.gg/lol/top-lane-tier-list"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com"
}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, features='html.parser')
# x = soup.findAll("strong", className="champion-name")

print(soup)
with open("index.html", "w", encoding='utf-8') as f:
    f.write(str(soup))
# print(x)