# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 00:59:32 2019

@author: USER
"""

import requests
import numpy as np
from bs4 import BeautifulSoup
import urllib

def fetch(url):
    response = requests.get(url)
    response = requests.get(url, cookies={'over18': '1'})  # 一直向 server 回答滿 18 歲了 !
    return response

def getphoto():
    
    url = 'https://www.ptt.cc/bbs/Beauty/index.html'
    addr = []
    for round in range(1):
        res = fetch(url)#抓取網站中的原始碼
        soup = BeautifulSoup(res.text,'html.parser')
        articles = soup.select('div.title a')#從<div>中抓取標題的連結
        paging = soup.select('div.btn-group-paging a')#找到上一頁(next_url)在哪
        next_url = 'https://www.ptt.cc' + paging[1]['href']#真正的上一頁的網址
        url = next_url
        print("round ",round)
        for article in articles:
            if '[正妹]' in article.text:#只抓正妹的
                addr.append('https://www.ptt.cc'+article['href'])
                #print(article['href'],article.text)
    print('已抓取文章網址')

    addr_img = []#抓取圖片網址
    for i in addr:
       url = i
       res = fetch(url)
       soup = BeautifulSoup(res.text,"lxml")
       for img in soup.select('div a'):
           if 'jpg' in img['href']:#抓取含有jpg的字串
               addr_img.append(img['href'])
               #print(img['href'])
    x = np.random.randint(0,5)
    return addr_img[x]

print(getphoto())
    