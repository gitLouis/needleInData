import requests
from bs4 import BeautifulSoup
import re
import time
import json

LIMIT_OF_PRODUCT_PER_CATEGORY = 3
SLEEP_BETWEEN_REQUESTS_SECONDS = 4
NA = 'NA'


def parseProductPage(pageUrl : str) -> dict:
    print('Parsing product page: ' + pageUrl + '...')
    productOutput = dict()
    time.sleep(SLEEP_BETWEEN_REQUESTS_SECONDS)
    productRequest = requests.get(pageUrl)
    productBS = BeautifulSoup(productRequest.text, "lxml")
    productOutput['title'] = productBS.find(id = 'productName').text
    sizesTag = productBS.find(id = "productSizes")
    productOutput['sizes'] = NA if not sizesTag else sizesTag.text
    productWeightTag =  productBS.find(id = "productWeight")
    productOutput['sizes'] = NA if not productWeightTag else productWeightTag.text
    productOutput['description'] = productBS.find(id = "productUpper").find(id = "productDesignShort").text
    productOutput['imgSrc'] = productBS.find(id = "productUpper").find("img")["src"]
    #productOutput['reviews'] = parseRatingReviews(productBS)

    #print('product done!')
    return productOutput

def parseCategoryPage(pageUrl : str) -> dict:
    productCounter = 0
    print("Parsing category page: " + pageUrl + '...')
    time.sleep(SLEEP_BETWEEN_REQUESTS_SECONDS)
    CategoryRequest = requests.get(pageUrl)
    categoryBS = BeautifulSoup(CategoryRequest.text, "lxml")
    categoryOutput = dict()

    for productTag in categoryBS.find_all("div", { "class" : re.compile("^searchResult")}):
        if productCounter>=LIMIT_OF_PRODUCT_PER_CATEGORY:
            break
        productURL = 'http://www.arcteryx.com/' + productTag.find('a')['href']
        categoryOutput[productURL] = parseProductPage('http://www.arcteryx.com/' + productTag.find('a')['href'])
        productCounter = productCounter+1

    print('Category done! ' + str(productCounter) + ' products.')

    return categoryOutput


r = requests.get('http://www.arcteryx.com/Home.aspx?country=il&language=en')
mainPage = BeautifulSoup(r.text, "lxml")
mainResults = dict()

for categoryTag in mainPage.find_all("dd", { "class" : re.compile("^category")}):
    gender = categoryTag.find_parent('li' , {"class":re.compile("^top-nav")}).find("h3").text
    mainCategoryName = categoryTag.parent.find('dd', {'class' : 'heading'}).text
    categoryName = categoryTag.text
    categoryProductsOutput = parseCategoryPage('http://www.arcteryx.com' + categoryTag.next['href'])
    try:
        mainResults[gender][mainCategoryName][categoryName] = categoryProductsOutput
    except KeyError:
        try:
            mainResults[gender][mainCategoryName] = dict()
            mainResults[gender][mainCategoryName][categoryName] = categoryProductsOutput

        except KeyError:
            mainResults[gender] = dict()
            mainResults[gender][mainCategoryName] = dict()
            mainResults[gender][mainCategoryName][categoryName] = categoryProductsOutput

print('Saving as Json file...')
with open('result_3_product_per_cat.json', 'w') as fp:
    json.dump(mainResults, fp)

fp.close()
print('Done!')



