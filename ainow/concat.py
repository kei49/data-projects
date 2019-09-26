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


LASTPAGE = 2411
#URLDIR = 'pageurls'
URLDIR = 'editors_articles'
RESULTS = 'e_articles.csv'

def arrange(li):
    l_dict = {}
    for l in li:
        num = re.search(r'(\d+)\.csv', l)
        l_dict[int(num.group(1))] = l
    l_list = []
    for i in range(len(l_dict)):
        l_list.append(l_dict[i])
    return l_list

def getData(file_name):
    with open(file_name) as f:
        reader = csv.reader(f)
        data= []
        for row in reader:
            data.append([row[0], row[1]])
    return data

def saveCsv(data):
    with open(RESULTS, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def main():
    url_files = arrange(glob.glob(URLDIR+'/*.csv'))
    num_files = len(url_files)

    all_data = []
    for i, url_file in enumerate(url_files):
        data = getData(url_file)

        all_data.extend(data)

        print('-------------------------------------------')
        print('Searched {}/{} csv files: {} % completed!'.format(i+1, num_files, round((i+1)/num_files*100, 1)))
        print('-------------------------------------------\n')
    saveCsv(all_data)


if __name__ == '__main__':
    main()
