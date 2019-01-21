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

    crawler.get_rank_data(db)

elif('getpic' == func):    #使用getpic function

    crawler.get_homepage_pic()

elif('getoverall' == func):  #使用getoverall function

    crawler.requestViewData()

else:

    print('please provide correct parameter')


