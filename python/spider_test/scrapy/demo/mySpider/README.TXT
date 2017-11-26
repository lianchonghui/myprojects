scrapy原理
spiders/xxx.py 
-> parse(self,response):->response对象就是类型为Element的html(其实response.selector.xpath()/css())
-> 导入Item对象，将目标字段赋值给Item对象
-> yield返回Item对象给Pipline处理


crawlspider原理
spiders/xxx.py 
->spider类继承自CrawlSpider类
-> __init__里面定义LinkExtractor，Rule里面传入LinkExtractor对象和回调函数，注意这里不能重写parse函数，回调函数传入两个参数，self和response
->response对象就是类型为Element的html(其实response.selector.xpath()/css())
-> 导入Item对象，将目标字段赋值给Item对象
-> yield返回Item对象给Pipline处理
