# coding:utf-8

import json
import logging
from tornado.web import RequestHandler, StaticFileHandler
from utils.session import Session
import tornado.web
'''
 RequestHandler(object)
    def __init__(self, application, request, **kwargs):
RequestHandler对象的创建必须传入一个application,一个request
我们在Application中创建了数据库的链接，在继承自RequestHandler来在Handler中调用数据库的功能
'''

'''
在正常情况未抛出错误时，调用顺序为：

set_defautl_headers()
initialize() #路由中的字典参数会传入这个方法
prepare() #每次执行HTTP（get,post...）前都会调用该方法
HTTP方法
on_finish()

在有错误抛出时，调用顺序为：

set_default_headers()
initialize()
prepare()
HTTP方法
set_default_headers()
write_error()
on_finish()

'''

class BaseHandler(RequestHandler):
    """自定义基类"""
    @property
    def db(self):
        """作为RequestHandler对象的db属性"""
        return self.application.db

    @property
    def redis(self):
        """作为RequestHandler对象的redis属性"""
        return self.application.redis

    #响应过程中，调用完initialize()以后调用prepare()
    #这里采用json数据传输，在prepare中传见json_args来接收请求的json数据
    def prepare(self):
        """预解析json数据"""
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = {}
    
    #每次Http请求返回的时候都会首先调用set_default_header(self)方法,HTTP调用过程报错会再次调用该方法
    def set_default_headers(self):
        """设置默认json格式"""
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def get_current_user(self):
        """判断用户是否登录"""
        self.session = Session(self)
        return self.session.data


'''
    application = web.Application([
        (r"/content/(.*)", web.StaticFileHandler, {"path": "/var/www"}),
'''
class StaticFileBaseHandler(StaticFileHandler):
    """自定义静态文件处理类, 在用户获取html页面的时候设置_xsrf的cookie"""
    def __init__(self, *args, **kwargs):
        super(StaticFileBaseHandler, self).__init__(*args, **kwargs)
        self.xsrf_token


