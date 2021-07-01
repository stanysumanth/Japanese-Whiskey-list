import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = 'https://www.thewhiskyexchange.com/'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}


productlinks = []                                                    # link to each product

for x in range(1,7):
    r = requests.get(f'https://www.thewhiskyexchange.com/search?q=japanese+whiskey&pg={x}&psize=24')
    soup = BeautifulSoup(r.content, 'lxml')

    productlist = soup.find_all('li', class_='product-grid__item')   # list of all products

    for product in productlist:
        link = product.find('a').get('href')
        productlinks.append(baseurl + link)


whiskeylist = []

for link in productlinks:
    r = requests.get(link, headers=headers)

    soup = BeautifulSoup(r.content, 'lxml')

    try:
        name = soup.find('h1', class_='product-main__name').text.strip()
    except:
        name= ''

    # try:
    #     rating = soup.find('div', class_='review-overview').text.strip()
    # except:
    #     rating = ''
    # # review = soup.find('span', class_='review-overview__count').text.strip().replace('(', '').replace(')', '')
    
    try:
        price = soup.find('p', class_='product-action__price').text.strip()
    except:
        price = ''

    whiskey = {
        'name': name,
        # 'rating' : rating,
        'price' : price,
        }

    whiskeylist.append(whiskey)
    # print(whiskey['name'])

df = pd.DataFrame(whiskeylist)
print(df.head(15))

df.to_csv('Japanese_whiskey_list.csv', index=False)