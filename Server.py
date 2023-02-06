import socket
from _thread import *
import pickle

server = "192.168.1.4"
port = 5555

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((server,port))

s.listen()

players = []

def ipP(ip):
    for p in players:
        if p[7] == ip:
            if p[6] == "False":
                return "at"

            else:
                return int(players.index(p))
    else:
        return "ekle"     

def threaded_client(conn,player):    
    run = True

    msg = pickle.loads(conn.recv(2048))
    
    if (len(players) < player+1) == True:
        try:
            players.append(msg)
            players[player][5] = player
            players[player][6] = "False"
            run = True
            conn.send(pickle.dumps("ADDED"))
            
        except:
            run = False

    else:
        players[player][6] = "False"
        pld = players[player]
        print(pld)
        conn.send(pickle.dumps("LİST"))
        conn.send(pickle.dumps(pld))
        print(players)
        print("hoşgeldin paşam!")

    while run:
        players[player]
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data
        
            if not data:
                players[player][6] = "True"
                conn.close()
                break

            else:
                players[player][6] = "False"
                ram_data = []
                ram_data.extend(players)
                ram_data.pop(player)
                conn.send(pickle.dumps(ram_data))

        except:
            players[player][6] = "True"
            conn.close()
            break
        
currentPlayer = 0
while True:
    conn,addr = s.accept()
    ipp = pickle.loads(conn.recv(2048))
    print(f"{addr} oyuna katıldı!")

    if ipP(ipp) == "at":
        conn.close()
        print("Oyuncu atıldı!")
    
    elif ipP(ipp) == "ekle":
        start_new_thread(threaded_client,(conn,currentPlayer))
        currentPlayer += 1
        print("Yeni oyuncu girişi!")

    elif type(ipP(ipp)) is int:
        start_new_thread(threaded_client,(conn,ipP(ipp)))
        print(f"{ipP(ipp)} numaralı oyuncu tekrar oyuna girdi!")
    
    
