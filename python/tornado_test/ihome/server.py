# coding:utf-8

'''
    tornado main入口
'''

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import os
import torndb
import config
import redis
import logging

from urls import urls
from tornado.options import options,define
from tornado.web import RequestHandler

'''
tornado.options.options下的参数可以用define定义，在python server.py --help中会显示log.py的options
都是通过该类来定义的，比如log_file_prefix,logging等
tornado.options.define()方法用于定义默认参数值
tornado.options.parse_command_line()方法用于解析python server.py --port=8000中的参数,如果命令行中没有给
就给difine中的定义值
tornado.options.parse_config_file(path,final=True)用于读去键值对的配置文件，如有配置文件config，port=8000
'''

define("port",default = 8000,type = int,help = "run server on the given port")
'''
#自定义Application类，继承自tornado.web.Application在__init__方法中配置db,redis链接
#我们可以看到tornado只需要创建一个Application对像，以及HTTPServer对象监听端口，启动IOLoop就可以运行了。
#所以我们可以通过继承tornado.web.Application来实现额外的功能，比如数据库链接
#我们也注意到，对于ReqeuestHandler对象的创建需要传递一个Application对象，一个Reqeust对象，及其他非必要参数
#所以我们可以通过继承RequestHandler来实现在Handler调用自定义的Application功能

'''
class Application(tornado.web.Application):
    def __init__(self,*args,**kwargs):
        super(Application,self).__init__(*args,**kwargs)
        # 注意Connection()的参数是**kwargs
        #torndb.Connection(self,host,database,user=None,password=None,...)其他参数皆有默认值，一般不必配置
        self.db = torndb.Connection(**config.mysql_options)
        
        #redis.StrictRedis(self,host='localhost',port=6379,db=0,password=None,...)其他参数一般不用配置
        self.redis = redis.StrictRedis(**config.redis_options)

def main():
    #tornado.options.options属性值
    #1.define自定义
    #2.python server.py --help可以查看自定义和框架定义的options
    #options.log...是tornado/log.py下定义的参数，用来控制日志
    options.log_file_prefix = config.log_path
    options.logging = config.log_level

    # tornado.optons.parse_command_line()用来解析命令行参数,如python server.py --port=8000将获取port的值
    tornado.options.parse_command_line()

    #Application对象的创建，主要参数1.路由映射列表，2.其他配置选项
    #tornado.web.Application(self,handlers=None,default_host=None,transforms=None,**settings)
    app = Application(
        urls,
        **config.settings
    )

    #tornado.httpserver.HTTPServer(self,*args,**kwargs)
    #返回的对象如果采用listen()方法都是单进程，采用bind()方法就是多进程
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    #调用start()对epoll进行论询
    tornado.ioloop.IOLoop.current().start()

'''
1. `~tornado.tcpserver.TCPServer.listen`: simple single-process::

        server = HTTPServer(app)
        server.listen(8888)
        IOLoop.current().start()

   In many cases, `tornado.web.Application.listen` can be used to avoid
   the need to explicitly create the `HTTPServer`.

2. `~tornado.tcpserver.TCPServer.bind`/`~tornado.tcpserver.TCPServer.start`:
   simple multi-process::

        server = HTTPServer(app)
        server.bind(8888)
        server.start(0)  # Forks multiple sub-processes
        IOLoop.current().start()

   When using this interface, an `.IOLoop` must *not* be passed
   to the `HTTPServer` constructor.  `~.TCPServer.start` will always start
   the server on the default singleton `.IOLoop`.

3. `~tornado.tcpserver.TCPServer.add_sockets`: advanced multi-process::

        sockets = tornado.netutil.bind_sockets(8888)
        tornado.process.fork_processes(0)
        server = HTTPServer(app)
        server.add_sockets(sockets)
        IOLoop.current().start()

'''

if __name__ == '__main__':
    main()
