# -*- coding:UTF-8 -*-
import requests  #导入requests 库
from bs4 import BeautifulSoup  #导入BeautifuoSoup
import os #导入os 库
from selenium import webdriver                      #导入selenium 的 webdriver
from selenium.webdriver.common.keys import Keys     #导入keys
from selenium.webdriver.chrome.options import Options
import time
from utility import utility
import datetime
import sys
import io
from crawlerlog import crawlerlog
from DBConnection import MySQL



class bilibilicrawler():

    def __init__(self): #类的初始化操作

        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '

                                      '(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'} #给定义一个请求头来模拟EDGE

        self.web_url = 'https://www.bilibili.com/'

        path = 'config.xml'

        configfile = io.open(path, encoding='utf-8')

        pathinfo = BeautifulSoup(configfile, 'xml')

        self.photo_path = pathinfo.find('picpath').text.strip()

        self.crawlerlogging = crawlerlog()

    def request(self, url):

        r = requests.get(url, headers=self.headers)

        return r

    def __save_img(self, url, name):   #保存图片

        self.crawlerlogging.log_event('开始请求图片地址',20)

        if ('https:' not in url):

            img = self.request('https:' + url)

        else:

            img = self.request(url)

        file_name = self.photo_path + name + '.jpg'

        self.crawlerlogging.log_event('开始保存文件', 20)

        f = open(file_name, 'ab')

        f.write(img.content)

        self.crawlerlogging.log_event('文件保存成功!', 20)

        f.close

    def get_homepage_pic(self):  #使用selenium获取主页图片

        print("开始网页get请求")

        chrome_options = Options()

        chrome_options.add_argument('--headless')

        driver = webdriver.Chrome(chrome_options=chrome_options)   #无头模式

        driver.get(self.web_url)

        utility_1 = utility() #实例化utility类

        utility_1.scoll_down(driver, 1)   #下拉滚动条

        print('开始获取标签')

        pic = BeautifulSoup(driver.page_source, 'lxml')

        print("开始获取img标签")

        pic_list = pic.find_all("img")  # 获取img 标签

        print("开始创建文件夹")

        utility_1.mkdir(self.photo_path)   # 创建文件夹

        for pic1 in pic_list:   # 遍历所有img标签

            pic_url = pic1['src']
            if ('.jpg' in pic_url):

                if('@' in pic_url):

                    pic_url_sliced = pic_url[0:pic_url.index('@')]

                else:
                    pic_url_sliced = pic_url

                try:

                    start_p = len(pic_url_sliced) - 1 - pic_url_sliced[::-1].index('/')

                except IndexError:

                    start_p = 0

                end_p = pic_url_sliced.index('.jpg')

                img_name = pic_url_sliced[start_p: end_p]

                self.__save_img(pic_url_sliced, img_name)

            elif ('.png' in pic_url):

                if('@' in pic_url):

                    pic_url_sliced = pic_url[0:pic_url.index('@')]

                else:
                    pic_url_sliced = pic_url

                try:

                    start_p = len(pic_url_sliced) - 1 - pic_url_sliced[::-1].index('/')

                except IndexError:

                    start_p = 0

                end_p = pic_url_sliced.index('.png')

                img_name = pic_url_sliced[start_p: end_p]

                self.__save_img(pic_url_sliced, img_name)

            elif('.bmp' in pic_url):

                if('@' in pic_url):

                    pic_url_sliced = pic_url[0:pic_url.index('@')]

                else:
                    pic_url_sliced = pic_url

                try:

                    start_p = len(pic_url_sliced) - 1 - pic_url_sliced[::-1].index('/')

                except IndexError:

                    start_p = 0

                end_p = pic_url_sliced.index('.bmp')

                img_name = pic_url_sliced[start_p: end_p]

                self.__save_img(pic_url_sliced, img_name)
        sys.stdout.flush()
        sys.stderr.flush()

    def get_rank_data(self, db):

        for i in range(1, 39):  # 根据rid获取不同分类的data

            resultlist = self.__retrieve_rank_data(

                'https://api.bilibili.com/x/web-interface/ranking/region?rid={}'.format(i))  # 使用api获得ranking data

            for result in resultlist:

                try:

                    db.sql_insert('rank_data', result)

                except:

                    print('data issue, please verify the result data: ' + result)

        self.crawlerlogging.log_event(str(datetime.datetime.now()) + ' data 获取完毕', 20)

        sys.stdout.flush()

        sys.stderr.flush()

    def __requestSrcList(self):

        print("开始网页get请求")

        chrome_options = Options()

        chrome_options.add_argument('--headless')

        driver = webdriver.Chrome(chrome_options=chrome_options)   #无头模式

        driver.get(self.web_url)

        bflodingSrcList = driver.page_source   #拿到加载全部页面前的srclist

        pic = BeautifulSoup(bflodingSrcList, 'lxml')

        pic_list = pic.find_all('img')

        print('开始保存文件--下拉前image')

        f = open('srcb.txt', 'w', encoding="utf-8")


        for pic1 in pic_list:  # 遍历所有img标签

            pic_src = pic1['src']

            try:

                pic_alt = pic1['alt']

            except:

                pic_alt = 'n/a'

            f.write(pic_alt + '\t' + pic_src + '\n')

        f.close()

        print('保存完成')

        self.scoll_down(driver, 1)

        aflodingSrcList = driver.page_source  # 拿到加载全部页面的srclist

        pic = BeautifulSoup(aflodingSrcList, 'lxml')

        pic_list = pic.find_all('img')

        print('开始保存文件--下拉后image')

        f = open('srca.txt', 'w', encoding="utf-8")

        for pic1 in pic_list:  # 遍历所有img标签

            pic_src = pic1['src']

            try:

                pic_alt = pic1['alt']

            except:

                pic_alt = 'n/a'

            f.write(pic_alt + '\t' + pic_src + '\n')

        f.close()

        print('保存完成')

    def __requestViewData(self, urls):

        result = ''

        try:

            req = requests.get(urls[0]).json()

        except:

            pass

        time.sleep(0.6)

        try:
            title = req['data']['title']
            data = req['data']['stat']

            video = (
                data['aid'],                #视频编号
                title,                      #主题
                data['view'],               #播放量
                data['danmaku'],            #弹幕数
                data['reply'],              #回复数
                data['favorite'],           #收藏数
                data['coin'],               #硬币数
                data['share'],              #分享
                data['now_rank'],           #排名
                data['his_rank'],           #历史排名
                data['like'],               #点赞数
                data['dislike']             #点踩数
            )

            title = title.replace("'", '')

            result = str(data['aid']) + ",'" + title[0:40] + "'," + str(data['view']) + ',' + str(data['danmaku']) + ','\
                     + str(data['reply']) + ',' + str(data['favorite']) + ',' + str(data['coin']) + ',' + \
                     str(data['share']) + ','+ str(data['now_rank']) + ',' + str(data['his_rank']) + ',' \
                     + str(data['like']) + ',' + str(data['dislike'])

        except:

            pass

        return result

    def __retrieve_rank_data(self, urls):   #

        resultlist = []

        try:

            req = requests.get(urls).json()

            for list in req['data']:

                title = list['title'].replace("'", '')

                title = "'" + title[0:48] + "'"

                aid = str(list['aid'])

                play = str(list['play'])

                review = str(list['review'])

                video_review = str(list['video_review'])

                favorites = str(list['favorites'])

                typename = list['typename'].replace("'", '')

                typename = "'" + typename[0:43] + "'"

                result = aid + ',' + title + ',' + play + ',' + review + ',' + video_review + ',' + favorites + ',' + \
                         typename[0:50] + ', sysdate()'
                #获得值加上系统时间
                resultlist.append(result)

        except Exception as e:

            print(e)

            pass

        return resultlist