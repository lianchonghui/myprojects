# -*- coding: utf-8 -*-
import scrapy
from mySpider.items import ItcastItem


class ItcastSpider(scrapy.Spider):
    name = "itcast"
    allowed_domains = ["itcast.cn"]
    start_urls = (
        'http://www.itcast.cn/channel/teacher.shtml',
    )

    def parse(self, response):
        #filename = 'teacher.html'
        #open(filename,'w').write(response.body)

        items = []

        for each in response.xpath('//div[@class="li_txt"]'):
            #将得到的数据封装到一个ItcastItem对象
            item = ItcastItem()

            #extract()方法返回的都是unicode对象
            name = each.xpath('h3/text()').extract()
            title = each.xpath('h4/text()').extract()
            info = each.xpath('p/text()').extract()

            #xpath返回的是包含一个元素的列表
            #如果这里采用utf-8编码，在pipelines处理的时候json.dumps(dict(item),ensure_ascii=False)就会报错
            item['name'] = name[0].encode('utf-8')
            item['title'] = title[0].encode('utf-8')
            item['info'] = info[0].encode('utf-8')
            '''
            #以下报错，说明scrapy.item是一个类似与字典的对象
            item.name = name[0]
            item.title = title[0]
            item.info = info[0]
            items.append(item)
            '''
            #return items
            yield item
