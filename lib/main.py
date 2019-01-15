# -*- coding:UTF-8 -*-
from DBConnection import MySQL
from bilibilicrawler import bilibilicrawler
from bs4 import BeautifulSoup
import time
import datetime

path = 'config.xml'

db = MySQL('bibiliviewdata') #连接mysql server，使用bibiliviewdata db

crawler = bilibilicrawler()

for day in range(1, 60):   #循环获得60天的data

    for i in range(1, 39): #根据rid获取不同分类的data

        resultlist = crawler.retrieve_rank_data('https://api.bilibili.com/x/web-interface/ranking/region?rid={}'.format(i)) #使用api获得ranking data

        for result in resultlist:

            try:

                db.sql_insert('rank_data', result)

            except:

                print('data issue, please verify the result data: ' + result)

    print(str(datetime.datetime.now()) + 'data 获取完毕')

    time.sleep(86400) #停留一天

