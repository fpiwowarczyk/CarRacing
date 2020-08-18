
#   #TODO
#   1. Sprawdzic czy gracz wczesniej grał 
#   2. Pokazać innych gracz ktorzy sie lacza, zrobic max 2 graczy
#   3. Pokazac wygranego 
#   4. Zrobic kilka gier na raz 
#   5. Znalezc rzeczy ktore jeszcze musze zrobic ? 
#   6. Zmiana nicku w trakcie gry mozliwa 
#   7. Te same kolory u kazdego gracza 
#   8. Wylonic zwyciesce 
#   9. Naprawic blad z naliczaniem kolek 


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
color=''
gates = 32


class Car():
    nick =None
    id=None
    color=None
    posX = 100
    posY = 200
    gate = 0
    angle = 0
    def __init__(self,posX,posY):
        self.posX=posX
        self.posY=posY

P1=Car(200,220)
P2=Car(200,170)

class GameHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("New Connection")
    def onClose(self):
        print("Connection closed")
    def on_message(self,message): # Its messedup but ill fixed it later 
        global Lap,lastGate,nick,color
        if isinstance(message,bytes):
            if(len(message)==16):
                Task=3
                message=struct.unpack('hh'*4,message)
                #----------------Position of player 
                gate = message[0]+message[1]
                rotation = message[2]+message[3]
                posX = message[4]+message[5]
                posY = message[6]+message[7]

                if(gate != lastGate):
                    lastGate = gate
                    if(gate >= gates-1):
                        Lap += 1
                        gate = 0
                msg = struct.pack('hhhhhh',Task,Lap,gate,posX,posY,rotation)
                if(self==P1.id):
                    P2.id.write_message(msg,True)
                elif(self==P2.id):
                    P1.id.write_message(msg,True)
            elif(len(message)==160):
                #-----------------Nick name of Player 
                message=struct.unpack('hh'*40,message)
                for n in message[2:16]:
                    if(n!= 0):
                        color=color+chr(n)
                for n in message[16:]:
                    if(n!=0):
                        nick=nick+chr(n)
                print(color)
                print(nick)
                if(P1.id==self):
                    P1.nick=nick
                    if(P1.nick!=None and P2.nick!= None):
                        Task=2
                        #---------- Message for Player 1 
                        message=struct.pack('hhhhhhh',Task,P1.posX,P1.posY,P1.angle,P2.posX,P2.posY,P2.angle)
                        for n in range(0,len(P1.nick)):
                            message=message+struct.pack('h',ord(P2.nick[n]))
                        P1.id.write_message(message,True)
                        #----------- Message for Player 2 
                        message=struct.pack('hhhhhhh',Task,P2.posX,P2.posY,P2.angle,P1.posX,P1.posY,P1.angle)
                        for n in range(0,len(P2.nick)):
                            message=message+struct.pack('h',ord(P1.nick[n]))
                        P2.id.write_message(message,True)
                elif(P2.id==self):
                    P2.nick=nick
                    if(P1.nick!=None and P2.nick!= None):
                        Task=2
                        #---------- Message for Player 1 
                        message=struct.pack('hhhhhhh',Task,P1.posX,P1.posY,P1.angle,P2.posX,P2.posY,P2.angle)
                        for n in range(0,len(P2.nick)):
                            message=message+struct.pack('h',ord(P2.nick[n]))
                        P1.id.write_message(message,True)
                        #----------- Message for Player 2 
                        message=struct.pack('hhhhhhh',Task,P2.posX,P2.posY,P2.angle,P1.posX,P1.posY,P1.angle)
                        for n in range(0,len(P1.nick)):
                            message=message+struct.pack('h',ord(P1.nick[n]))
                        P2.id.write_message(message,True)
                nick=''
                color=''

                
            elif(len(message)==4):
                message=struct.unpack('hh',message)
                if(P1.id==None):
                    Task=0
                    P1.id=self
                    msg = struct.pack('h',Task)
                    P1.id.write_message(msg,True)
                elif(P2.id==None and P1.id!=None):
                    P2.id=self
                    Task=1
                    msg = struct.pack('h',Task)
                    P1.id.write_message(msg,True)
                    P2.id.write_message(msg,True)

        

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