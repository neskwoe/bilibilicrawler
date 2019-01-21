# -*- coding:UTF-8 -*-
import logging
import io
import datetime
from bs4 import BeautifulSoup
import os

class crawlerlog():

    def __init__(self):

        module_path = os.path.dirname(__file__)

        path = module_path + '\config.xml'

        configfile = io.open(path, encoding='utf-8')

        pathinfo = BeautifulSoup(configfile, 'xml')

        self.log_path = pathinfo.find('logpath').text.strip()

        logging.basicConfig(filename=self.log_path + str(datetime.date.today()) + '.log',
                            format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level=logging.DEBUG,
                            filemode='a', datefmt='%Y-%m-%d%I:%M:%S %p')

    def log_event(self, msg, severity):

        if (severity == 10):

            logging.debug(msg)
        elif (severity == 20):

            logging.info(msg)

        elif (severity == 30):

            logging.warning(msg)

        elif (severity == 40):

            logging.error(msg)

        elif (severity == 50):

            logging.critical(msg)