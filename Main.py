import pygame
import socket
import pickle

#Sınıflar

class Player:
    def __init__(self,x,y,width,height,color,afk):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3
        self.ip = "192.168.1.4"
        self.afk = afk
        self.player = 0
        self.list = [self.x,self.y,self.width,self.height,self.color,self.player,self.afk,self.ip]
        
    def setter(self,v,v1):
        if v == "x":
            self.x = v1

        if v == "y":
            self.y = v1

        if v == "width":
            self.width = v1

        if v == "height":
            self.height = v1

        if v == "color":
            self.color = v1

        if v == "player":
            self.player = v1

        if v == "afk":
            self.afk = v1

        if v == "ip":
            self.ip = v1

        self.update()

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.list = [self.x,self.y,self.width,self.height,self.color,self.player,self.afk,self.ip]

class Arkaplan:
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x += self.vel

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x -= self.vel

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y += self.vel

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y -= self.vel

        self.update()
        

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

#Sınıflar Bitiş

#Atamalar

local_x = 340
local_y = 210

p = Player(local_x,local_y,30,30,"red","False")

b = Arkaplan(local_x,local_y,600,300,"green")

#Atamalar Bitiş

#Socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server = "192.168.1.4"
port = 5555
client.connect((server,port))

client.send(pickle.dumps(p.ip))
print("ip")


client.send(pickle.dumps(p.list))
print(p.list)
print("list")

choice = pickle.loads(client.recv(2048))

cstr = str(choice)

print(choice)
print(cstr)

def setBackgroundPosWithPlayerPos(x,y):
    global local_x,local_y

    b.x = local_x + (local_x - x)
    b.y = local_y + (local_y - y)
    b.update()
    print("yapıldı")

def setListOfPlayer(liste):
    print(liste)
    p.setter("x",liste[0])
    p.setter("y",liste[1])
    p.setter("width",liste[2])
    p.setter("height",liste[3])
    p.setter("color",liste[4])
    p.setter("player",liste[5])
    p.setter("afk",liste[6])
    p.setter("ip",liste[7])
    setBackgroundPosWithPlayerPos(liste[0],liste[1])
    print("hazır")

if cstr.startswith("LİST") == True:
    print("geldi")
    datalist = pickle.loads(client.recv(4096))
    print(datalist)
    print("^")
    setListOfPlayer(datalist)

#Socket Bitiş

#Pencere 

width = 700
height = 450
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Project")

#Pencere Bitiş

#Main Fonsiyonlar

def updateWin(pla):
    win.fill((255,255,255))
    pygame.draw.rect(win,b.color,b.rect)
    for pl in pla:
        print(pl)
        if pl[6] == False:
            z_x = pl[0] + b.x - 340
            z_y = pl[1] + b.y - 210
            z_w = pl[2]
            z_h = pl[3]
            z_c = pl[4]
            z_rect = (z_x,z_y,z_w,z_h)
            pygame.draw.rect(win,z_c,z_rect)
        
    pygame.draw.rect(win,p.color,p.rect)
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        
        players = []

        client.send(pickle.dumps(p.list))
    
        data = pickle.loads(client.recv(2048))
        players.extend(data)

        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.afk = "False"
        b.move()
        p.move()
        updateWin(players)

main()

#Main Fonksiyonlar Bitiş
