import socket
from _thread import *
import pickle
from player import Player

sever = "192.168.1.196"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((sever, port))

except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection, Server Started")

current_player = 0
players = [Player(25, 250, 5, 100, (255, 255, 255), current_player),
           Player(475, 250, 5, 100, (255, 255, 255), current_player)]


def threaded_client(conn, player):
    conn.send((pickle.dumps(players[player-2])))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    connection, address = s.accept()
    print("Connected to", address)

    start_new_thread(threaded_client, (connection, current_player))
    current_player += 1
    for i in players:
        i.players += 1
