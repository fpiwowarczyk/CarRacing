
#   #TODO
#   1. Sprawdzic czy gracz wczesniej grał 



import tornado.web
import tornado.websocket
import tornado.ioloop
import struct 
import math 
import random 
import time
class Car():
    nick =None
    color=None
    posX = 0
    posY = 0
    gate = 0
    angle = 0
    Laps=0
    lastGate=0
    def __init__(self,posX,posY):
        self.posX=posX
        self.posY=posY
        self.id=None
        

class GameObj(): 
    def __init__(self,id):
        self.Waiting=True
        self.id=id
        self.P1=Car(300,220)
        self.P2=Car(300,170)
Numbers=1
nick=''
color=''
gates = 32
Connections=0
Games = [GameObj(Numbers)]

class GameHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("New Connection")
    def onClose(self):
        print("Connection closed")

    def on_message(self,message):
        global nick,color,Numbers
        if isinstance(message,bytes):
            for Game in Games:
                if((playersPresent(self,Game)) and GameNotWaiting(Game)):
                    if(len(message)==16):
                        if(self==Game.P1.id):
                            Task=3
                            Game.P1 = unpackMessage(message,Game.P1)
                            if(Game.P1.lastGate!=Game.P1.gate):
                                Game.P1 = updatePlayerProgress(Game.P1,gates)
                            if(Game.P1.Laps>=3):
                                setWinner(self,message,Game)
                            else:
                                sendStateToPlayers(Task,Game.P1,Game.P2)
                        elif(self==Game.P2.id):
                            Task=3
                            Game.P2 = unpackMessage(message,Game.P2)
                            if(Game.P2.lastGate!=Game.P2.gate):
                                Game.P2 = updatePlayerProgress(Game.P2,gates)
                            if(Game.P2.Laps>=3):
                                setWinner(self,message,Game)
                            else:
                                sendStateToPlayers(Task,Game.P2,Game.P1)
                    elif(len(message)==160): # Take info about colors and nicknames and broadcast them 
                        message=struct.unpack('h'*80,message)
                        color = unpackColor(message)
                        nick = unpackNickName(message)
                        if(Game.P1.id==self):
                            broadcastSetup(self,Game,1)
                        elif(Game.P2.id==self):
                            broadcastSetup(self,Game,2)
                        nick=''
                        color=''
                    break   
                elif (Game.Waiting==True and (Game.P1.id==None or Game.P2.id==None)):
                    if(len(message)==4):
                        addPlayers(self,message,Game)
                    break
           
    def checkOrigin(self,origin):
        print("Origin: ",origin)
        return True


def addPlayers(self,message,Game):
    global nick,color,Numbers
    message=struct.unpack('h'*2,message)
    if(Game.P1.id==None):
        Task=0
        Game.P1.id=self
        msg = struct.pack('h',Task)
        Game.P1.id.write_message(msg,True)
    elif(Game.P2.id==None and Game.P1.id!=None):
        Game.P2.id=self
        Task=1
        msg = struct.pack('h',Task)
        Game.P1.id.write_message(msg,True)
        Game.P2.id.write_message(msg,True)
        Game.Waiting=False
        Numbers+=1
        Games.append(GameObj(Numbers))

def setNickNames(self,Task,Game):
    global nick,color,Numbers
    #---------- Message for Player 1 
    message=struct.pack('h'*7,Task,Game.P1.posX,Game.P1.posY,Game.P1.angle,Game.P2.posX,Game.P2.posY,Game.P2.angle)
    for n in range(0,len(Game.P2.color)):
        message=message+struct.pack('h',ord(Game.P2.color[n]))
    for n in range(0,len(Game.P2.nick)):
        message=message+struct.pack('h',ord(Game.P2.nick[n]))
    Game.P1.id.write_message(message,True)
    #----------- Message for Player 2 \
    message=struct.pack('h'*7,Task,Game.P2.posX,Game.P2.posY,Game.P2.angle,Game.P1.posX,Game.P1.posY,Game.P1.angle)
    for n in range(0,len(Game.P1.color)):
        message=message+struct.pack('h',ord(Game.P1.color[n]))
    for n in range(0,len(Game.P1.nick)):
        message=message+struct.pack('h',ord(Game.P1.nick[n]))
    Game.P2.id.write_message(message,True)#Coordinate nicknames and colors

def setWinner(self,message,Game):
    Task=4
    Winner=1
    msg=struct.pack('h'*2,Task,Winner)
    Game.P2.id.write_message(msg,True)
    Winner=2
    msg=struct.pack('h'*2,Task,Winner)
    Game.P1.id.write_message(msg,True)

def sendStateToPlayers(Task,Player,OtherPlayer):
    msg = struct.pack('h'*7,Task,OtherPlayer.Laps,Player.Laps,OtherPlayer.gate,Player.posX,Player.posY,Player.angle)
    OtherPlayer.id.write_message(msg,True)

def unpackMessage(message,Player):
    message=struct.unpack('h'*8,message)
    Player.gate = message[0]+message[1]
    Player.angle = message[2]+message[3]
    Player.posX = message[4]+message[5]
    Player.posY = message[6]+message[7]
    return Player

def playersPresent(self,Game):
    return self==Game.P1.id or self==Game.P2.id

def GameNotWaiting(Game):
    return Game.Waiting==False

def updatePlayerProgress(Player,gates):
    Player.lastGate=Player.gate 
    if(Player.gate>=gates):
        Player.gate=0
        Player.Laps=Player.Laps+1
    return Player

def unpackColor(message):
    color=''
    for n in message[2:16]:
        if(n!= 0):
            color=color+chr(n)
    return color

def unpackNickName(message):
    nick =''
    for n in message[16:]:
        if(n!=0):
            nick=nick+chr(n)
    return nick
  
def broadcastSetup(self,Game,Player):
    Task=2
    if(Player==1):
        Game.P1.color=color
        Game.P1.nick=nick
    elif(Player==2):
        Game.P2.color=color
        Game.P2.nick=nick
    if(Game.P1.nick!=None and Game.P2.nick!= None):  
        Task=2
        setNickNames(self,Task,Game)




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