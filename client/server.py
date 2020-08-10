import tornado.web
import tornado.websocket
import tornado.ioloop
import struct 
import math 
import random 
import time

Players={}
Lap=0
lastGate=0
# Zliczanie kółek pos tronie serwera 
#  Kontrola poruszania się auta 
# Dodac gracza jako klase, a potem zrobic z tego array 
# 
# class Player:
#     Lap=0
#     def __init__(self):

class GameHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("New Connection")
    def onClose(self):
        print("Connection closed")
    def on_message(self,message):
        global Lap,lastGate
        if isinstance(message,bytes):
            message=struct.unpack('hhhh',message)
            print(message)
            gate=message[0]+message[1]
            gates = message[2]
            if(gate!=lastGate):
                lastGate= gate
                if(gate>=gates-1):
                    Lap+=1
                    gate=0
                msg = struct.pack('hh',Lap,gate)

                self.write_message(msg,True)

        

    def checkOrigin(self,origin):
        print("Origin: ",origin)
        return True

    
class Loader(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html",title="CarRacing")


if __name__ == "__main__":
    app = tornado.web.Application([
        ("/",Loader),
        ("/ws",GameHandler),
        ("/(.*)", tornado.web.StaticFileHandler, {"path": ""}),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()