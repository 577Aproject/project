import requests
import json
import time
from bs4 import BeautifulSoup

def parseOnePage(response):
    data = response.text
    soup = BeautifulSoup(data, "html.parser")

    allInfo = json.loads(soup.find('script', attrs={'type':'application/ld+json'}).text)
    return allInfo

if __name__ == "__main__":

    for i in range(100):
        print(i)
        movieId = '0' * (7 - len(str(i))) + str(i)
        response = requests.get('https://www.imdb.com/title/tt{}/'.format(movieId))
        if response.status_code == 404:
            continue
        info = parseOnePage(response)