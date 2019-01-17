# -*- coding:UTF-8 -*-
from DBConnection import MySQL
from bilibilicrawler import bilibilicrawler
import sys
import time


func = sys.argv[1]

path = 'config.xml'  #配置文件

db = MySQL('bibiliviewdata') #连接mysql server，使用bibiliviewdata database

crawler = bilibilicrawler()

if ('getrank' == func):   #使用get rank data function

    try:

        repeat_days = sys.argv[2]

        for i in repeat_days():

            crawler.get_rank_data(db)

            time.sleep(86400)

    except:

        print('default to 60 days')

        for i in range(1, 60):
            
            crawler.get_rank_data(db)

            time.sleep(86400)

elif('getpic' == func):

    crawler.get_homepage_pic()


elif('getoverall' == func):

    crawler.requestViewData()

else:

    print('please provide correct parameter')


