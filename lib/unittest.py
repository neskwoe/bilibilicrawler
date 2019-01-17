# -*- coding:UTF-8 -*-
from crawlerlog import crawlerlog
from bilibilicrawler import bilibilicrawler
from DBConnection import MySQL

db = MySQL('bibiliviewdata') #连接mysql server，使用bibiliviewdata database

crawler = bilibilicrawler()

log = crawlerlog()
crawler = bilibilicrawler()

#log.log_event('test',40)

crawler.get_rank_data(db)