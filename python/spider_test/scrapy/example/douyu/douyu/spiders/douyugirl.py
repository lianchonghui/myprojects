# -*- coding: utf-8 -*-
import scrapy
import json
from douyu.items import DouyugirlItem

class DouyugirlSpider(scrapy.Spider):
    name = "douyugirl"
    allowed_domains = ["http://capi.douyucdn.cn"]

    offset = 0
    url = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset="
    start_urls = [url+str(offset)]

    def parse(self, response):
        #api获取到的是json数据，通过json.loads加载json数据并提取data段数据集合
        data = json.loads(response.body)["data"]
        for each in data:
            item =  DouyugirlItem()
            item['name'] = each['nickname']
            item['imagesUrls'] = each['vertical_src']
            print '&'*18
            print item['imagesUrls']
            print type(item['imagesUrls'])
            yield item
            #return item
            self.offset += 20
            yield scrapy.Request(self.url+str(self.offset),callback = self.parse)

