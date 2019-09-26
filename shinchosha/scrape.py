import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import time
import pandas as pd
import csv
import math
import glob
import re

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


LASTPAGE = 494
# LASTPAGE = 41
URLDIR = 'pageurls'
DATADIR = 'data'
BOOKS = DATADIR + '/books.csv'
AUTHORS = DATADIR + '/authors.csv'

def arrange(li):
    l_dict = {}
    for l in li:
        num = re.search(r'(\d+)\.csv', l)
        l_dict[int(num.group(1))] = l
    l_list = []
    for i in range(len(l_dict)):
        l_list.append(l_dict[i])
    return l_list

def resultsCsv():
    try:
        os.makedirs(DATADIR)
    except FileExistsError:
        pass

    try:
        books = pd.read_csv(BOOKS)
    except:
        books = pd.DataFrame(columns=['title', 'authors', 'price', 'published_date', 'head', 'detail', 'icons', 'ebook', 'csv', 'num'])

    return books

def getUrls(file_name):
    with open(file_name) as f:
        reader = csv.reader(f)
        urls= []
        for row in reader:
            urls.append(row[0])
    return urls

def searchBook(df, url, i, j):
    res = requests.get(url)
    bs = BeautifulSoup(res.content, 'html.parser')
    bs = bs.find('div', class_='mod-detail')

    head = bs.find('div', class_='mod-detail__head')
    body = bs.find('div', class_='mod-detail__main')

    try:
        headding = head.find('h1').text
    except:
        headding = False

    try:
        head_icons = []
        icons = head.find('ul').find_all('li')
        for icon in icons:
            head_icons.append(icon.text)
    except:
        head_icons = False

    try:
        title = body.find('h2', class_='mod-detail__title').text
    except:
        title = False

    try:
        authors = body.find('p', class_='mod-detail__author').text
    except:
        authors = False

    try:
        date = body.find('p', class_='mod-detail__date').text
    except:
        date = False

    try:    
        price = body.find('p', class_='mod-detail__price').text
    except:
        price = False

    try:
        detail = body.find('div', class_='mod-detail__textbox').find('p').text
    except:
        detail = False

    #print(headding, head_icons)
    #print(title, authors, price, date, detail)

    if 'ebook' in url:
        ebook = True
    else:
        ebook = False

    tmp_se = pd.Series([title, authors, price, date, headding, detail, head_icons, ebook, i, j], index=df.columns)
    df = df.append(tmp_se, ignore_index=True)
    return df


def main():
    books = resultsCsv()
    url_files = arrange(glob.glob(URLDIR+'/*.csv'))
    num_files = len(url_files)

    print(books.head())
    have_csv = books['csv'].value_counts().index.tolist()
    print(have_csv) 
    # books = searchBook(books, 'https://www.shinchosha.co.jp/ebook/E042111/')

    for i, url_file in enumerate(url_files):
        if i in have_csv:
            print('Already have', url_file)
            continue
        urls = getUrls(url_file)
        for j, url in enumerate(urls):
            books = searchBook(books, url, i, j)
            print('Checked {}-{}: {}'.format(i, j, url))
            time.sleep(1)
        books.to_csv(BOOKS, index=False)

        print('-------------------------------------------')
        print('Searched {}/{} csv files: {} % completed!'.format(i+1, num_files, round((i+1)/num_files*100, 1)))
        print('-------------------------------------------\n')


if __name__ == '__main__':
    #urlCsv()
    main()
