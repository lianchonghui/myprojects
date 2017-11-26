# coding:utf-8

from tornado.web import Application,RequestHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
class IndexHandler(RequestHandler):
    def get(self):
        self.write('hello tornado')
    def post(self):
        print self.request.body

def main():
    app = Application(
        [
            (r'/',IndexHandler),
        ]

    )
    http_server = HTTPServer(app)
    http_server.listen(8000)
    IOLoop.current().start()

if __name__ == '__main__':
    main()
