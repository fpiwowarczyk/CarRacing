import tornado.web
import tornado.websocket
import tornado.ioloop
import struct 
import math 
import random 
import time


if __name__ == "__main__":
    app = tornado.web.Application([
        ("/",Loader),
        ("/ws",GameHandler),
        ("/(.*)",tornado.web.StaticFileHandler,{"path": ""}),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()