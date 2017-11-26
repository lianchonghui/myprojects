# coding:utf-8

'''
糗事百科 基于requests的爬虫
数据<-Element被xpath解析出来<-etree.HTML()函数将html数据转换成Element对象<-requests.get()获取html文本
'''

import requests
from lxml import etree

page = 1
url = 'http://www.qiushibaike.com/8hr/page/' + str(page)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8'
    }

try:
    response = requests.get(url,headers=headers)
    resHtml = response.text

    html = etree.HTML(resHtml)
    #获取属性id包含qiushi_tag的div元素
    result = html.xpath('//div[contains(@id,"qiushi_tag")]')
    #xpath解析返回的对象是Element对象，即result与html是同一类对象 
    for site in result:
        item = {}
        #在result的当前节点上获取字节点的数据
        imgUrl = site.xpath('./div/a/img/@src')[0].encode('utf-8')
        username = site.xpath('./div/a/@title')[0].encode('utf-8')
        content = site.xpath('.//div[@class="content"]/span')[0].text.strip().encode('utf-8')

        vote = site.xpath('.//i')[0].text

        comments = site.xpath('.//i')[1].text

        print imgUrl,username,content,vote,comments

except Exception,e:
    print e


