import socket
import threading
from time import time
import math, random

HEADER = 64
PORT = 50735
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT!"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
player1y = 290
player2y = 290
ballx = 400
bally = 300
playerCount = 0
ballDirection = random.randint(45, 135) * (random.randint(0, 1)-0.5)*2
SPEED = 200
lastFrame = time()
def Action(packet, addr, conn):
    global player1y, player2y, ballx, bally
    playery, timeSent = list(map(float, packet.split(" ")))
    
    if addr == player1:
        player1y = playery
        ballPhysics()
        conn.send(f"{player2y} {ballx} {bally}".encode(FORMAT))
    else:
        player2y = playery
        ballPhysics()
        conn.send(f"{player1y} {(ballx-400)*-1+400} {bally}".encode(FORMAT))



def handle_client(conn,addr):
    global player1, player2, playerCount
    print(f"{addr} connected")
    if playerCount == 0:
        player1 = addr
        playerCount += 1
    elif playerCount == 1:
        player2 = addr
        playerCount += 1
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
            Action(msg, addr, conn)

    conn.close()
    
"""def ballPhysics():
    global player1y, player2y, ballx, bally
    while True:
        ballx """

def ballPhysics():
    global lastFrame, ballx, bally, player1y, player2y, ballDirection

    distance = SPEED * (time() - lastFrame)
    lastFrame = time()
    ballx += math.sin(ballDirection) * distance
    bally += math.cos(ballDirection) * distance

    if 0 <= bally - player1y + 12.5 <= 25 and 20 <= ballx <= 26:
        ballDirection *= -1
        ballDirection = (((((ballDirection+180)%360-180)*-1)-90)*-1) - 90
        ballx += math.sin(ballDirection) * distance
        bally += math.cos(ballDirection) * distance
    if 0 <= bally - player2y + 12.5 <= 25 and 774 <= ballx <= 780:
        ballDirection *= -1
        ballDirection = (((((ballDirection+180)%360-180)*-1)+90)*-1) + 90 # I won't even pretend to understand what this monstrosity is. gl to any future debuggers
        ballx += math.sin(ballDirection) * distance
        bally += math.cos(ballDirection) * distance
    if ballx < 0 or ballx > 800:
        player1y = 9
        player2y = 290
        ballx = 400
        bally = 300
        ballDirection = random.randint(45, 135) * (random.randint(0, 1)-0.5)*2
    if bally > 600:
        ballDirection = ((ballDirection+90)*-1 - 90 )*-1
        print(ballx, bally, ballDirection)
        ballx += math.sin(ballDirection) * distance
        bally += math.cos(ballDirection) * distance
    if bally < 0:
        ballDirection = ((ballDirection-90)*-1 + 90 )*-1
        print(ballx, bally, ballDirection)
        ballx += math.sin(ballDirection) * distance
        bally += math.cos(ballDirection) * distance


def start():
    server.listen()
    print(f"listening on {SERVER}")
    while True:
        conn , addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"{threading.active_count()-1}")


print("server is starting")
start()
