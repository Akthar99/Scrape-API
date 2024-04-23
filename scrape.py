from bs4 import BeautifulSoup
import requests
import sys

def serch(title: str, pull: int = 50):
    res = requests.get(f"https://en.wikipedia.org/w/index.php?title=Special:Search&limit={pull}&offset=0&ns0=1&search={title}",
                       proxies={"http":"152.67.9.179:8100",
                                "https":"152.67.9.179:8100"}, timeout=20)
    content = res.text
    
    soup = BeautifulSoup(content, 'lxml')
    tags = soup.find_all('div', class_="searchresult")
    heading = soup.find_all('div', class_="mw-search-result-heading")
    links = soup.find_all("a")

    for link in links:
        extracted_link = link.get("href")
        print(extracted_link)

    for tag in tags:
        print(tag.text)

def Input():
    while True:
        try:
            user_input = input("what do you wants to search : ")
            user_input_pull = input("how much data do you wants to pull(leave blanks if you wants to pull 20) : ")
            serch(user_input, user_input_pull)
        except KeyboardInterrupt:
            print("turning down")
            sys.exit()
Input()
            
