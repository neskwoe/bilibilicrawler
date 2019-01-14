# -*- coding:UTF-8 -*-
import MySQLdb
from bs4 import BeautifulSoup
import io

class MySQL():

    def __init__(self, database): #类的初始化操作

        path = 'config.xml'

        configfile = io.open(path, encoding='utf-8')

        connectioninf = BeautifulSoup(configfile, 'xml')

        server = connectioninf.find('Server').text.strip()

        profile = connectioninf.find('Profile').text.strip()

        pwd = connectioninf.find('Pwd').text.strip()

        self.db = MySQLdb.connect(server, profile, pwd, database)

        self.db.set_character_set('utf8')

        self.cursor = self.db.cursor()


    def sql_insert(self, table_name, values):

        print('insert in process')

        req = self.sql_retrevefields(table_name)

        field = ''

        for f in req:

            field = field + ',' + f[0]

        sql = 'insert into ' + table_name + '(' + field[1:len(field)] + ') values(' + values + ')'

        self.cursor.execute(sql)

        self.db.commit()

        print('insert done')

    def sql_select(self):

        print('select in process')

    def sql_retrevefields(self, table_name):

        print('retrieving field name of table' + table_name)

        sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '" + table_name + "';"

        self.cursor.execute(sql)

        resultlist = []

        for row in self.cursor.fetchall():

            resultlist.append(row)

        return resultlist

    def select_data(self, sql):

        cursor = self.cursor(cursorclass=MySQLdb.cursors.DictCursor)

        cursor.execute(sql)

        result = cursor.fetchall()

        resultList = []

        for i in result:

            resultList.append(i)

        cursor.close()

        # 得到的结果是字典格式
        return resultList
