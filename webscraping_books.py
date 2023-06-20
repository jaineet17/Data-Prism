# Author
# archoudh , dpatnaik, jaineets, namitb, niyatim
# The purpose of this file is to extract the data from amazon using
# BeautifulSoup. We make use of the html tags present on the amazon website to extract
# book title, book author, book price, book ratings, books average rating and the link for each book

import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                  '103.0.5060.53 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

terms = ['python', 'data+science', 'natural+language+processing', 'computer+vision', 'machine+learning',
         'deep+learning', 'sql', 'Data+Visualization', 'R+Programming', 'AWS', 'Business+Intelligence',
         'data+mining', 'Tableau', 'Analytics', 'artificial+intelligence', 'cloud+computing']
filtered_set = {'by ', ' and ', ', et al.', ', '}


# Function to extract the book data from amazon. BeautifulSoup has been used for this very purpose using html tags.
def getbooks():
    datascience_items = []
    for i in terms:
        url = 'https://www.amazon.com/s?k={0}'.format(i)
        print('Processing {0}'.format(url + '&page=1'))
        response = requests.get(url + '&page=1', headers=headers)
        sleep(1.5)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})
        for result in results:
            product_name = result.h2.text
            single_list = []
            temp = result.find('div', {'class': 'a-row a-size-base a-color-secondary'})
            for j in temp.findAll('a', {'class': 'a-size-base'}):
                authors = j.findAll(text=True)
                single_list.append(authors)
            for j in temp.findAll('span', {'class': 'a-size-base'}):
                authors = j.findAll(text=True)
                single_list.append(authors)
            filtered_single_list = []
            for k in single_list:
                for m in k:
                    filtered_single_list.append(m)
            product_authors = [a for a in filtered_single_list if a not in filtered_set]
            stringified_product_authors = ', '.join(product_authors)
            try:
                rating_count = result.find('div', {'class': 'a-row a-size-small'}).find(
                    {'span': 'aria-label'}).next_sibling.text
            except AttributeError:
                rating_count = 'NA'
            try:
                rating = result.find('div', {'class': 'a-row a-size-small'}).find({'span': 'aria-label'}).text.replace(
                    'out of 5 stars', '')
            except AttributeError:
                rating = 'NA'
            try:
                price1 = result.find('span', {'class': 'a-price-whole'}).text
                price2 = result.find('span', {'class': 'a-price-fraction'}).text
                try:
                    price = float(price1 + price2)
                except:
                    price = 'NA'
                product_url = 'https://www.amazon.com' + result.h2.a['href']
            except AttributeError:
                continue

            datascience_items.append(
                [product_name, stringified_product_authors, rating_count, rating, price, product_url])
    df = pd.DataFrame(datascience_items,
                      columns=['product', 'author', 'rating_count', 'rating', 'price', 'product_url'])
    df.to_csv('raw_books.csv', index=False)


if __name__ == '__main__':
    getbooks()
