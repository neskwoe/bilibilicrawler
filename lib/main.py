# -*- coding:UTF-8 -*-
from DBConnection import MySQL
from bilibilicrawler import bilibilicrawler
import sys
from bs4 import BeautifulSoup
import time
import datetime

func = sys.argv

path = 'config.xml'

db = MySQL('bibiliviewdata') #连接mysql server，使用bibiliviewdata database

crawler = bilibilicrawler()

if ('getrank' == func):   #使用get rank data function

    for i in range(1, 39): #根据rid获取不同分类的data

        resultlist = crawler.retrieve_rank_data('https://api.bilibili.com/x/web-interface/ranking/region?rid={}'.format(i)) #使用api获得ranking data

        for result in resultlist:

            try:

                db.sql_insert('rank_data', result)

            except:

                print('data issue, please verify the result data: ' + result)

    print(str(datetime.datetime.now()) + 'data 获取完毕')

elif('getpic' == func):

    crawler.get_homepage_pic()

elif('getoverall' == func):

    crawler.requestViewData()


