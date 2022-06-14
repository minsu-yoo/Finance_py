# DBUpdater.py

import pandas as pd
from bs4 import BeautifulSoup
import urllib
import pymysql
import calendar
import time
import json
from urllib.request import urlopen
from datetime import datetime
from threading import Timer


class DBUpdater:
    def __init__(self):
        """ 생성자: MariaDB 연결 및 종목코드 딕셔너리 생성 """

        self.conn = pymysql.connect(host='localhost', user='root',
                                    password='Rktnek0806^^', db='Investar', charset='utf8')

        with self.conn.cursor() as curs:
            sql = """

            CREATE TABLE IF NOT EXIST company_info (
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (code)
            );

            """

            curs.execute(sql)
            sql = """

            CREATE TABLE IF NOT EXIST daily_price (
                code VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                diff BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date)

            );

            """

            curs.execute(sql)

        self.conn.commit()

        self.codes = dict()
        self.update_comp_info()

    def __del__(self):
        """소멸자: MariaDB 연결 해제 """
        self.conn.close()


if __name__ == '__main__':
    dbu = DBUpdater()
    dbu.execute_daily()
