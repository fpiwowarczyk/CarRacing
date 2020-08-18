
#   TODO
#   1. Sprawdzic czy gracz wczesniej grał 
#   2. Pokazać innych gracz ktorzy sie lacza, zrobic max 2 graczy
#   3. Pokazac wygranego 
#   4. Zrobic kilka gier na raz 
#   5. Znalezc rzeczy ktore jeszcze musze zrobic ? 
#   6. Ogarnac dlaczego tak przyspiesza jak klikam w 
#
#
#
#   Struktura wiadomosci  OD KLIENTA  
#   1:0
#   2:Gate
#   3:0
#   4:Gate Len
#   5:Wielokrotnosci 256 PosX
#   6:PosX%256
#   7:Wielokrotnosci 256 PosY
#   8:PosY%256
#   9:0
#   10:F Letter of Nick and so on 
#
#   Struktura wiadomości OD SERVERA 
#   1:
#   2:
#   3:
#   4:
#   5:
#   6:
#   7:
#   8:
#
# class Player:
#     Lap=0
#     def __init__(self):
import tornado.web
import tornado.websocket
import tornado.ioloop
import struct 
import math 
import random 
import time

Lap=0
lastGate=0
nick=''
gates = 32


class Car():
    nick =None
    posX = 100
    posY = 200
    gate = 0
    id=None
    def __init__(self,posX,posY):
        self.posX=posX
        self.posY=posY

P1=Car(100,200)
P2=Car(500,500)

class GameHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("New Connection")
    def onClose(self):
        print("Connection closed")
    def on_message(self,message):
        global Lap,lastGate,nick
        if isinstance(message,bytes):
            if(len(message)==16):
                message=struct.unpack('hh'*4,message)
                #print(message)
                #----------------Position of player 
                gate=message[0]+message[1]
                rotation = message[2]+message[3]
                posX= message[4]+message[5]
                posY=message[6]+message[7]

                if(gate!=lastGate):
                    lastGate= gate
                    if(gate>=gates-1):
                        Lap+=1
                        gate=0
                msg = struct.pack('hhhhh',Lap,gate,posX,posY,rotation)
                #print(msg)
                self.write_message(msg,True)
            elif(len(message)==132):
                #-----------------Nick name of Player 
                message=struct.unpack('hh'*33,message)
                for n in message[2:]:
                    if(n!= 0):
                        nick=nick+chr(n)
                print(nick)
                nick=''
                
            elif(len(message)==4):
                message=struct.unpack('hh',message)
                if(P1.id==None):
                    P1.id=self
                    msg = struct.pack('h',0)
                    P1.id.write_message(msg,True)
                elif(P2.id==None and P1.id!=None):
                    P2.id=self
                    msg = struct.pack('h',1)
                    P1.id.write_message(msg,True)
                    P2.id.write_message(msg,True)
            print(P1.id)
            print(P2.id)
            print(message)

        

    def checkOrigin(self,origin):
        print("Origin: ",origin)
        return True

    
class Loader(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html",title="CarRacing")


if __name__ == "__main__":
    print("Server started")
    app = tornado.web.Application([
        ("/",Loader),
        ("/ws",GameHandler),
        ("/(.*)", tornado.web.StaticFileHandler, {"path": ""}),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()