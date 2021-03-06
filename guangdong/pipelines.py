# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


# class GuangdongPipeline(object):
#     def process_item(self, item, spider):
#         return item

class MysqlPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("MYSQL_HOST"),
            database=crawler.settings.get("MYSQL_DATABASE"),
            user=crawler.settings.get("MYSQL_USER"),
            password=crawler.settings.get("MYSQL_PASSWORD"),
            port=crawler.settings.get("MYSQL_PORT"),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        # 构造供应商数据字典
        data_supplier = {
            "name": data.pop("name"),
            "price": data.pop("price"),
            "ranking": data.pop("ranking"),
            "good_id": ""
        }
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        # cursor.lastrowid 获取插入数据的id 还有一种方法 db.insert_id()
        good_id = self.cursor.lastrowid
        data_supplier["good_id"] = good_id
        keys2 = ', '.join(data_supplier.keys())
        values2 = ', '.join(['%s'] * len(data_supplier))
        sql2 = 'insert into %s (%s) values (%s)' % (item.table2, keys2, values2)
        self.cursor.execute(sql2, tuple(data_supplier.values()))
        self.db.commit()
        print("写数据-------------------------")
        return item