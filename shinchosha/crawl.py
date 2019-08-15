import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import time
import csv
import math

LASTPAGE = 494
# LASTPAGE = 41
CSVDIR = 'pageurls'

def getURLs():
    print('Start crawling!')
    num_csvs = math.ceil(LASTPAGE/20)

    for each in range(num_csvs):
        file_path = '{}/pageurl{}.csv'.format(CSVDIR, each)
        if os.path.isfile(file_path):
            print(file_path, 'exists!')
            continue

        book_links = []
        for list_num in range(20):
            url = 'https://www.shinchosha.co.jp/search/result.php?query=&start={}#result-list'.format((each*20+list_num)*20)
            res = requests.get(url)
            bs = BeautifulSoup(res.content, 'html.parser')
            bs = bs.find('div', class_='l-each-4')

            books = bs.find_all('div', class_='l-col-3')
            for book in books:
                link = book.find('a').get('href')
                book_links.append([link])
            time.sleep(1)

        print('-----------------------------')
        saveCsv(file_path, book_links)
        print('{}/{} csv files were created: {} % completed!'.format(each+1, num_csvs, round((each+1)/num_csvs*100, 1)))
        print('-----------------------------\n')


def saveCsv(file_path, links):
    try:
        os.makedirs(CSVDIR)
    except FileExistsError:
        pass

    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(links)
        print('Created {}'.format(file_path))

if __name__ == '__main__':
    getURLs()
