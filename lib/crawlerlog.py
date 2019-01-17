# -*- coding:UTF-8 -*-
import logging
import io
import datetime
from bs4 import BeautifulSoup

class crawlerlog():

    def __init__(self):

        path = 'config.xml'

        configfile = io.open(path, encoding='utf-8')

        pathinfo = BeautifulSoup(configfile, 'xml')

        self.log_path = pathinfo.find('picpath').text.strip()

        logging.basicConfig(filename=self.log_path + str(datetime.date.today()) + '.log',
                            format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level=logging.DEBUG,
                            filemode='a', datefmt='%Y-%m-%d%I:%M:%S %p')

    def log_event(self, msg, severity):

        logging.error(msg)
