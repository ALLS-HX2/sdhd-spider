#!/usr/bin/env python3
import pymysql.cursors

class MySQLUtil:
    def __init__(self):
        self.conn = self.get_conn()
        self.cursor = self.get_cursor()

    def get_conn(self):
        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='sample',
                               database='SDHD',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        return conn

    def get_cursor(self):
        cursor = self.conn.cursor()
        return cursor

    def select_all(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def select_one(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def select_many(self, sql, num):
        self.cursor.execute(sql)
        return self.cursor.fetchmany(num)

    def commit_data(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except pymysql.Error as e:
            print(e)
            self.conn.rollback()

    def commit_data_many(self, sql):
        try:
            for el in sql:
                self.cursor.execute(el)
            self.conn.commit()
        except pymysql.Error as e:
            print(e)
            self.conn.rollback()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
