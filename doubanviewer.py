# coding: utf-8
import requests
from bs4 import BeautifulSoup
import csv
import json
import re
import time

def fetch(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36'
    r = requests.get(url, headers=headers, timeout=20)
    return r.text
        
def parse_table(table):
    user_link = table.find('a')['href']
    user_img = table.find('a').find('img')['src']
    user_name = table.find('a').find('img')['alt']
    pdiv = table.find('div',{'class':"pl2"})
    try:
        user_place = pdiv.find('a').find('span').text
        user_place = user_place.replace('(','')
        user_place = user_place.replace(')','')
    except:
        user_place = ''
    vtime = table.find('p',{'class':"pl"}).text
    vtime = vtime.split()[0]
    try:
        vcontent = table.find_all('p')[1].text
    except:
        vcontent = ""
    try:
        star = table.find('p',{'class':"pl"}).find('span')['class'][0]
        star = re.sub(r'\D','',star)
    except:
        star = '.'
    try:
        sup = table.find('p',{'class':"pl"}).find('span')['title']
    except:
        sup = ''
    table_data = [user_img, user_name.encode('utf-8'), user_link, user_place.encode('utf-8'), vcontent.encode('utf-8'), vtime.encode('utf-8'), star, sup.encode('utf-8')]
    return table_data

#crawl review
def review_crawl():
    urls = []
    for i in range(10):
        start = 20*i
        url = 'https://movie.douban.com/subject/26411410/collections?start={}'.format(start)
        urls.append(url)
    rst = []
    for url in urls:
        print url
        try:
            text = fetch(url)
        except:
            text = fetch(url)
        soup = BeautifulSoup(text)
        tables = soup.find_all('table',{'width':'100%'})
        for table in tables:
            table_data = parse_table(table)
            rst.append(table_data)
        time.sleep(1)

    with open('doubanreview2.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(rst)

if __name__ == '__main__':
    review_crawl()
