import socket
from _thread import *
import pickle
from game import Game

server = "Yours IPv4 address"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try :
    s.bind((server , port))
except socket.error as e :
    str(e)

s.listen(2)
print("WAITING FOR CONNECTIONS , SERVER STARTED !")

connected = set()
games = {}
idCount = 0

def threadedClient(conn , p , gameId) :
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True :
        try :
            data = conn.recv(4096).decode()
            if gameId in games :
                game = games[gameId]

                if not data :
                    break
                else :
                    if data == "reset" :
                        game.reset()
                    elif data != "get" :
                        game.play(p, data)
                    
                    conn.sendall(pickle.dumps(game))
            else :
                break
        except :
            break
    print("Lost connection !")
    try :
        del games[gameId]
        print("Closing Game " , gameId)
    except :
        pass
    idCount -= 1
    conn.close()

while True :
    conn , addr = s.accept()
    print("Connected to : " , addr)

    idCount += 1
    p = 0 
    gameId = (idCount - 1)//2
    if idCount%2 == 1 :
        games[gameId] = Game(gameId)
        print("CREATING A NEWW GAME ....")
    else :
        games[gameId].ready = True
        p = 1
    
    start_new_thread(threadedClient , (conn , p , gameId))
