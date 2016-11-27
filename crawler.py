import requests
from bs4 import BeautifulSoup
import re
import time

LIMIT_OF_PRODUCT_PER_CATEGORY = 2
SLEEP_BETWEEN_REQUESTS_SECONDS = 6

def parseProductPage(pageUrl : str) -> int:
    print('Parsing product page: ' + pageUrl + '...')
    CategoryRequest = requests.get(pageUrl)
    time.sleep(SLEEP_BETWEEN_REQUESTS_SECONDS)
    productRequest = requests.get(pageUrl)
    productPage = BeautifulSoup(productRequest.text, "lxml")

    print('product done!')

def parseCategoryPage(pageUrl : str) -> int:
    productCounter = 0
    print("Parsing category page: " + pageUrl + '...')
    time.sleep(SLEEP_BETWEEN_REQUESTS_SECONDS)
    CategoryRequest = requests.get(pageUrl)
    categoryPage = BeautifulSoup(CategoryRequest.text, "lxml")

    for productTag in categoryPage.find_all("div", { "class" : re.compile("^searchResult")}):
        if productCounter>LIMIT_OF_PRODUCT_PER_CATEGORY:
            break
        parseProductPage('http://www.arcteryx.com' + productTag.find('a')['href']
)

        productCounter = productCounter+1

    print('Category done! ' + str(productCounter) + ' products.')
    return


r = requests.get('http://www.arcteryx.com/Home.aspx?country=il&language=en')
mainPage = BeautifulSoup(r.text, "lxml")

for categoryTag in mainPage.find_all("dd", { "class" : re.compile("^category")}):
    print(categoryTag.next['href'])
    parseCategoryPage('http://www.arcteryx.com' + categoryTag.next['href'])


