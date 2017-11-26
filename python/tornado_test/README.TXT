tornado原理
1.main函数下创建一个tornado.web.Application对象
	<- url列表（url和路由处理对象）,注意，这里是列表，不是解包的列表元素
		<-路由处理对象：tornado.web.RequestHandler该类子类有个def get(self)方法
	<- 创建一个tornado.httpserver.HTTPServer(app)对象，bind()绑定一个端口,start(num_process=n)启动n个进程，n<=0根据cpu创建子进程个数
2.tornado.ioloop.IOLoop.current().start()：启动
如果需要链接数据库，在入口出创建一个Application类，继承自tornado.web.Application
重写__init__方法，调用父类的__init__方法super(Application,self).__init__(*args,**kwargs)
	<-链接数据库的配置：self.db = torndb.Connection(**config.mysql_options)
			    self.redis = redis.StrictRedis(**config.redis_options)
	mysql_options和redis_options皆为字典，包含数据哭的链接参数（注意这里参数都是解包的，即多个参数）
