# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from redis import StrictRedis


class HousePipeline(object):
    def __init__(self):
        self.file = open('house.json','a')



    def process_item(self, item, spider):
        data = dict(item)
        print(data)
        data = json.dumps(data, ensure_ascii=False)
        self.file.write(data + '\n')
        return item

    def __del__(self):
        self.file.close()

