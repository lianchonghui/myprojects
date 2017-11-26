# -*- coding: utf-8 -*-
import scrapy
import re
from mySpider.items import Tencent_spiderItem
class TencentSpiderSpider(scrapy.Spider):
    name = "tencent_spider"
    allowed_domains = ["hr.tencent.com"]
    start_urls = (
        'http://hr.tencent.com/position.php?&start=0#a',
    )

    def parse(self, response):
        
        for each in response.xpath('//*[@class="even"]'):
            item = Tencent_spiderItem()
            name = each.xpath('./td[1]/a/text()').extract()[0]
            detailLink = each.xpath('./td[1]/a/@href').extract()[0]
            positionInfo = each.xpath('./td[2]/text()').extract()[0]
            peopleNumber = each.xpath('./td[3]/text()').extract()[0]
            workLocation = each.xpath('./td[4]/text()').extract()[0]
            publishTime = each.xpath('./td[5]/text()').extract()[0]

            item['name'] = name.encode('utf-8')
            item['detailLink'] = detailLink.encode('utf-8')
            item['peopleNumber'] = peopleNumber.encode('utf-8')
            item['workLocation'] = workLocation.encode('utf-8')
            item['publishTime'] = publishTime.encode('utf-8')
            
            curpage = re.search('(\d+)',response.url).group(1)
            page = int(curpage) + 10
            url = re.sub('\d+',str(page),response.url)
            if int(page) <50:
                yield scrapy.Request(url,callback = self.parse)

            yield item
