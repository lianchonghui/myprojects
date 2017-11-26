# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
'''
class MyspiderPipeline(object):
    def process_item(self, item, spider):
        return item
'''
class ItcastPipeline(object):
    def __init__(self):
        self.file = open('teacher.json','wb')

    def process_item(self,item,spider):
        print '-'*8
        print type(item)
        print item

        content = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.file.write(content)
        return item

    def close_spider(self,spider):
        self.file.close()


class Tencent_spiderJsonPipeline(object):
    def __init__(self):
        self.file = open('tencent_spider.json','wb')

    def process_item(self,item,spider):
        content = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.file.write(content)
        return item
        
    def close_spider(self,spider):
        self.file.close()


