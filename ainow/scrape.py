import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import time
import csv
import math

LASTPAGE = 43
CSVDIR = 'editors_articles'

def getURLs():
    print('Start crawling!')
    num_csvs = math.ceil(LASTPAGE/20)
    end = False

    for each in range(num_csvs):
        file_path = '{}/pageurl{}.csv'.format(CSVDIR, each)
        if os.path.isfile(file_path):
            print(file_path, 'exists!')
            continue

        article_list = []
        for list_num in range(20):
            page_num = each*20 + list_num
            if page_num==1:
                url = 'https://ainow.ai/category/ainoweditor/'
            else:
                url = 'https://ainow.ai/category/ainoweditor/page/{}/'.format(page_num)
            res = requests.get(url)
            bs = BeautifulSoup(res.content, 'html.parser')

            articles = bs.find_all('article')
            for article in articles:
                a = article.find('a')
                link = a.get('href')
                try:
                    title = a.find('h1', class_='entry-title').text
                except:
                    end = True
                if end:
                    break
                article_list.append([title, link])
            time.sleep(1)
            if end:
                break

        print('-----------------------------')
        saveCsv(file_path, article_list)
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
