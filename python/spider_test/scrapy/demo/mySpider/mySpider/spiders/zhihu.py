# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy import Request,FormRequest


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://www.zhihu.com/',
    )
    rules = (
        Rule(LinkExtractor(allow = ('/question/\d+#.*?',)),callback = 'parse_page',follow = True),
        Rule(LinkExtractor(allow = ('/question/\d+',)),callback = 'parse_page',follow = True),
    )


    headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
            "Connection": "keep-alive",
            "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
            "Referer": "http://www.zhihu.com/"
            }

    #重写爬虫类的方法，实现了自定义请求，运行成功后会调用callback回调函数
    def start_request(self):
        return [Request("https://www.zhihu.com/login",meta = {'cookiejar': 1},callback = self.post_login)]

    def post_login(self,response):
        print 'Preparing login'
        xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print xsrf

        #FormRequest.from_response是Scrapy提供的一个函数，用于post表单
        #登录成功后会调用after_login回调函数
        return [FormRequest.from_response(response,
                                          meta = {'cookiejar': response.meta['cookiejar']},
                                          headers = self.headers,
                                          formdata = {
                                              '_xsrf':xsrf,
                                              'email':'1095511864@qq.com',
                                              'password':'123456'
                                          },
                                          callback = self.after_login,
                                          dont_filter = True
                                         )]

    def after_login(self,response):
        for url in self.start_urls:
            yield self.make_resquests_from_url(url)


    def parse_page(self,response):
        problem = Selector(response)
        item = ZhihuItem()
        item['url'] = response.url
        item['name'] = problem.xpath('//span[@class="name"]/text()').extract()
        item['title'] = problem.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()').extract()
        item['description'] = problem.xpath('//div[@class="zm-editable-content"]/text()').extract()
        item['answer']= problem.xpath('//div[@class=" zm-editable-content clearfix"]/text()').extract() 
        return item
