
#   #TODO
#   1. Sprawdzic czy gracz wczesniej grał 
#   2. Pokazać innych gracz ktorzy sie lacza, zrobic max 2 graczy #DONE
#   3. Pokazac wygranego #DONE
#   4. Zrobic kilka gier na raz ---> INPROGRESS 1
#   5. Zmiana nicku w trakcie gry mozliwa #W ogole to robic ?
#   6. Te same kolory u kazdego gracza #DONE 
#   7. Wylonic zwyciesce #DONE
#   8. Naprawic blad z naliczaniem kolek #DONE


import tornado.web
import tornado.websocket
import tornado.ioloop
import struct 
import math 
import random 
import time

Lap=0
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
    Laps=0
    lastGate=0
    def __init__(self,posX,posY):
        self.posX=posX
        self.posY=posY



P1=Car(300,220)
P2=Car(300,170)

    
class GameHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("New Connection")
    def onClose(self):
        print("Connection closed")
    def on_message(self,message): # Its messedup but ill fixed it later 
        global Lap,lastGate,nick,color
        if isinstance(message,bytes):
            if(len(message)==16): #-------------- Send position to other player 
                if(self==P1.id):
                    Task=3
                    message=struct.unpack('hh'*4,message)
                    P1.gate = message[0]+message[1]
                    P1.angle = message[2]+message[3]
                    P1.posX = message[4]+message[5]
                    P1.posY = message[6]+message[7]
                    if(P1.lastGate!=P1.gate):
                        P1.lastGate=P1.gate 
                        if(P1.gate>=gates):
                            P1.gate=0
                            P1.Laps=P1.Laps+1
                    if(P1.Laps>=3):
                        Task=4
                        Winner=1
                        msg=struct.pack('hh',Task,Winner)
                        P1.id.write_message(msg,True)
                        Winner=2
                        msg=struct.pack('hh',Task,Winner)
                        P2.id.write_message(msg,True)
                    else:
                        msg = struct.pack('hhhhhhh',Task,P2.Laps,P1.Laps,P2.gate,P1.posX,P1.posY,P1.angle)
                        P2.id.write_message(msg,True)
                elif(self==P2.id):
                    Task=3
                    message=struct.unpack('hh'*4,message)
                    P2.gate = message[0]+message[1]
                    P2.angle = message[2]+message[3]
                    P2.posX = message[4]+message[5]
                    P2.posY = message[6]+message[7]
                    if(P2.lastGate!=P2.gate):
                        P2.lastGate=P2.gate 
                        if(P2.gate>=gates):
                            P2.gate=0
                            P2.Laps=P2.Laps+1
                    if(P2.Laps>=3):
                        Task=4
                        Winner=1
                        msg=struct.pack('hh',Task,Winner)
                        P2.id.write_message(msg,True)
                        Winner=2
                        msg=struct.pack('hh',Task,Winner)
                        P1.id.write_message(msg,True)
                    else:
                        msg = struct.pack('hhhhhhh',Task,P1.Laps,P2.Laps,P1.gate,P2.posX,P2.posY,P2.angle)
                        P1.id.write_message(msg,True)

            elif(len(message)==160):
                #-----------------Color of Player 
                message=struct.unpack('hh'*40,message)
                for n in message[2:16]:
                    if(n!= 0):
                        color=color+chr(n)
                #-----------------Nick name of Player 
                for n in message[16:]:
                    if(n!=0):
                        nick=nick+chr(n)
                if(P1.id==self):
                    P1.color=color
                    P1.nick=nick
                    if(P1.nick!=None and P2.nick!= None):  
                        coord() #Coordinate nicknames and colors
                elif(P2.id==self):
                    P2.color=color
                    P2.nick=nick
                    if(P1.nick!=None and P2.nick!= None):
                        coord()#Coordinate nicknames and colors
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

def coord():
    Task=2
    #---------- Message for Player 1 
    message=struct.pack('hhhhhhh',Task,P1.posX,P1.posY,P1.angle,P2.posX,P2.posY,P2.angle)
    for n in range(0,len(P2.color)):
        message=message+struct.pack('h',ord(P2.color[n]))
    for n in range(0,len(P2.nick)):
        message=message+struct.pack('h',ord(P2.nick[n]))
    P1.id.write_message(message,True)
    #----------- Message for Player 2 \
    message=struct.pack('hhhhhhh',Task,P2.posX,P2.posY,P2.angle,P1.posX,P1.posY,P1.angle)
    for n in range(0,len(P1.color)):
        message=message+struct.pack('h',ord(P1.color[n]))
    for n in range(0,len(P1.nick)):
        message=message+struct.pack('h',ord(P1.nick[n]))
    P2.id.write_message(message,True)

if __name__ == "__main__":
    print("Server started")
    app = tornado.web.Application([
        ("/",Loader),
        ("/ws",GameHandler),
        ("/(.*)", tornado.web.StaticFileHandler, {"path": ""}),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()