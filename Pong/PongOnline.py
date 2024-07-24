import socket, time 
import pygame


pygame.init()
HEIGHT = 600
WIDTH = 800
display = pygame.display.set_mode((WIDTH, HEIGHT))
def connect():
    global HEADER, PORT, FORMAT, DISCONNECT, SERVER, ADDR, client
    HEADER = 64
    PORT = 50735
    FORMAT = 'utf-8'
    DISCONNECT = "!DISCONNECT!"
    SERVER = '192.168.0.4'
    ADDR = (SERVER,PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

def send(msg:str):
    global HEADER, PORT, FORMAT, DISCONNECT, SERVER, ADDR, enemyy, ballx, bally
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    enemyy, ballx, bally = list(map(float, (client.recv(2048)).decode().split(" ")))

pygame.display.set_caption("Pong")

def exitMenu():
    global show_exit_menu
    if show_exit_menu:
        show_exit_menu = False
    else:
        show_exit_menu = True
    
def renderExitMenu():

    button(300, 100, "resume", 200, 40)
    button(300, 200, "settings", 200, 40)
    button(300, 300, "exit to main menu", 200, 40)

def button(x, y, text, sizex, sizey):
    pygame.draw.rect(display, black, ( x, y, sizex, sizey))
    
    text = font.render(text, True, white)
    textRect = text.get_rect(center=(WIDTH // 2, y+sizey/2))
    display.blit(text, textRect)

def checkIfButtonClicked():
    global show_exit_menu
    (mx, my) = pygame.mouse.get_pos()
    
    if show_exit_menu:
        if 300 < mx < 500 and 100 < my < 140:
            show_exit_menu = False
        if 300 < mx < 500 and 200 < my < 240:
            show_exit_menu = False
            show_settings_menu = True
        if 300 < mx < 500 and 300 < my < 340:
            show_exit_menu = False
            exit_game()

def sendPackets():
    send(f"{playery} {time.time()}")

def exit_game():
    quit()

def quit():
    
    if inGame:
        global DISCONNECT
        send(DISCONNECT)
    exit()

def player_up():
    global playery
    if playery > 0:
        playery -= 0.15
def player_down():
    global playery
    if playery < 580:
        playery += 0.15

def render_game():
    global playery
    
    pygame.draw.rect(display, black, (20, playery, 6, 25)) # render player bat
    pygame.draw.rect(display, black, (774, enemyy, 6, 25)) # render enemy bat
    pygame.draw.circle(display, black, (ballx, bally), 4)


def resetVars():
    global playery, enemyy, ballx, bally
    playery = 290
    enemyy = 290
    ballx = 400
    bally = 300
resetVars()
white = (255, 255, 255)
black = (0, 0, 0)
darkMode = False
TEXTSIZE = 30
font = pygame.font.Font(None, TEXTSIZE)
show_exit_menu = False
show_settings_menu = False
inGame = True # change this to False later
kUp = False
kDown = False
connect()
while True:
    display.fill(white)
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if inGame:
                if event.key == pygame.key.key_code("escape"):

                    exitMenu()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    kDown = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    kUp = True
        if event.type == pygame.KEYUP:
            if inGame:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    kDown = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    kUp = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            checkIfButtonClicked()
    if kUp:
        player_up()
    if kDown:
        player_down()
    if show_exit_menu:
        renderExitMenu()
    else:
        sendPackets()
        render_game()
        
    pygame.display.flip()


