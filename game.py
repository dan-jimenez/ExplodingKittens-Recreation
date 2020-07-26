import socket
import threading
from threading import Timer
import sys
import pygame
from typing import TextIO
import json


# Imagenes usadas en el juego
background = pygame.image.load("img/fondo.png")
fondo_trans = pygame.image.load("img/fondo_trans.png")
icon = pygame.image.load("img/Icono.png")
boton_play = pygame.image.load("img/boton_play.png")
boton_pause = pygame.image.load("img/boton_pausa.png")
Baraja = pygame.image.load("img/baraja.png")
jugador1peq = pygame.image.load("img/Jugador1peq.png")
jugador1 = pygame.image.load("img/Jugador1.png")
jugador2 = pygame.image.load("img/Jugador2.png")
jugador3 = pygame.image.load("img/Jugador3.png")
jugador4 = pygame.image.load("img/Jugador4.png")
game_over = pygame.image.load("img/game_over.png")
restart = pygame.image.load('img/restart.png')
attack = pygame.image.load("img/ATTACK.png")
favor = pygame.image.load("img/FAVOR.png")
bomb = pygame.image.load("img/BOMB.png")
nope = pygame.image.load("img/NOPE.png")
seethefuture = pygame.image.load("img/SEETHEFUTURE.png")
shuffle = pygame.image.load("img/SHUFFLE.png")
skip = pygame.image.load("img/SKIP.png")
defuse = pygame.image.load("img/DEFUSE.png")
comodin1 = pygame.image.load("img/COMODIN1.png")
comodin2 = pygame.image.load("img/COMODIN2.png")
comodin3 = pygame.image.load("img/COMODIN3.png")
comodin4 = pygame.image.load("img/COMODIN4.png")
comodin5 = pygame.image.load("img/COMODIN5.png")
turn= pygame.image.load('img/turno.png')
marco= pygame.image.load('img/marco_logo.png')

class cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, 0, 0, 1, 1)
    def update(self):
        self.left, self.top = pygame.mouse.get_pos()
class boton(pygame.sprite.Sprite):
    def __init__(self, imagen1, x, y):
        self.imagen_normal = imagen1
        self.imagen_actual = self.imagen_normal
        self.rect = self.imagen_actual.get_rect()
        self.rect.left, self.rect.top = (x, y)

    def draw(self, screen):
        botonDibujado = screen.blit(self.imagen_actual, self.rect)
        return botonDibujado
class imagenes(pygame.sprite.Sprite):
    def __init__(self, imagen):
        self.carta = imagen
        self.rect= self.carta.get_rect()

    def draw (self, screen, x, y):
        self.rect= self.carta.get_rect()
        self.rect.left, self.rect.top= (x,y)
        cartadraw = screen.blit(self.carta, self.rect)
        return cartadraw
    def update(self, screen, curso, x, y):
        self.rect= self.carta.get_rect()
        self.rect.left, self.rect.top= (x,y)
        if curso.colliderect(self.rect):
            y-=50
            self.rect.left, self.rect.top= (x,y)
        else:
            y= y
            self.rect.left, self.rect.top= (x, y)
        screen.blit(self.carta,self.rect)

class game():
    global blit_mazo, partida, turnos, t, timer
    def __init__(self, weithd=1020, height=712, host= "127.0.0.1", port= 8000):
        self.player=socket.socket()
        self.player.connect((str(host), int(port)))
        self.screen = pygame.display.set_mode((weithd, height))
        self.clock = pygame.time.Clock()
        self.cursor = cursor()
        self.exit= True
        self.mensaje= str
        self.datos= dict


        msg_recv = threading.Thread(target=self.msg_recv)
        msg_recv.daemon = True
        msg_recv.start()



        if True:
            self.inicializar()

    def msg_recv(self):
        while True:
            try:
                data = self.player.recv(200000)
                if data:
                    self.mensaje= data.decode()
                    print(data.decode())
            except:
                pass
    def send_msg(self, msg):
        self.player.send(msg.encode())

    def cargar(self, data):
        json.dumps(data)
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

    def abrir(self):
        with open('data.json') as file:
            self.datos= json.load(file)
        return self.datos

    def game_over(self):
        while True:
            self.screen.blit(game_over, (254, 175))
            restar_b.draw(self.screen)
    def part_in(self, msg):
        if msg == "partida iniciada":
            self.partida= True
        else:
            self.partida= False


    def imprimir_cartas(self,c ,x, y):
        global procces
        procces= True
        while procces:
            if c == self.datos['cartas_c'][0]:
                ataque.update(self.screen, self.cursor,x, y)
                procces = False
            elif c == self.datos['cartas_c'][1]:
                salto.update(self.screen, self.cursor, x, y)
                procces = False
            elif c == self.datos['cartas_c'][2]:
                favr.update(self.screen, self.cursor,x , y)
                procces = False
            elif c == self.datos['cartas_c'][3]:
                futuro.update(self.screen, self.cursor, x, y)
                procces = False
            elif c == self.datos['cartas_c'][4]:
                no.update(self.screen, self.cursor,x,y)
                procces = False
            elif c == self.datos['cartas_c'][5]:
                barajar.update(self.screen, self.cursor,x, y )
                procces = False
            elif c == self.datos['cartas_c'][6]:
                comodin_1.update(self.screen, self.cursor,x , y )
                procces = False
            elif c == self.datos['cartas_c'][7]:
                comodin_2.update(self.screen, self.cursor,x, y)
                procces = False
            elif c == self.datos['cartas_c'][8]:
                comodin_3.update(self.screen, self.cursor, x, y)
                procces = False
            elif c == self.datos['cartas_c'][9]:
                comodin_4.update(self.screen, self.cursor,x, y)
                procces = False
            elif c == self.datos['cartas_c'][10]:
                comodin_5.update(self.screen, self.cursor,x, y)
                procces = False
            elif c == self.datos['cartas_c'][12]:
                defensa.update(self.screen, self.cursor, x, y)
                procces = False
            if c == self.datos['cartas_c'][11]:
                bomba.draw(self.screen, 445, 266)
                self.send_msg("bomba")
                procces= False

    def dibujar_cartas(self,x, y, aumentox, aumentoy, cartas):
        x1= x
        if len(self.datos[cartas])<9:
            if cartas == "mazo1" or cartas == "mazo2" or cartas == "mazo3" or cartas == "mazo4":
                y+= aumentoy
            else:
                y= y
        if self.datos[cartas] != []:
            for c in self.datos[cartas]:
                self.imprimir_cartas(c, x, y)
                x += aumentox
                if self.datos[cartas].index(c) == 7:
                    y += aumentoy
                    x = x1
                elif self.datos[cartas].index(c) == 15:
                    y += 57
                    x = x1

    def inicializar(self):
        pygame.init()

        """
        Aqui vamos a cargar todas las imagenes necesarias para el juego
        """

        #Constructor de jugadores
        global id
        id= self.mensaje
        if id == "1":
            jugador_1 = boton(jugador1, 447, 593)
            jugador_2 = boton(jugador2, 0, 303)
            jugador_3 = boton(jugador3, 463, 0)
            jugador_4 = boton(jugador4, 903, 304)
        elif id == "2":
            jugador_1 = boton(jugador2, 447, 593)
            jugador_2 = boton(jugador3, 0, 303)
            jugador_3 = boton(jugador4, 463, 0)
            jugador_4 = boton(jugador1, 889, 298)
        elif id == "3":
            jugador_1 = boton(jugador3, 440, 593)
            jugador_2 = boton(jugador4, 0, 304)
            jugador_3 = boton(jugador1, 447, 0)
            jugador_4 = boton(jugador2, 915, 303)
        elif id == "4":
            jugador_1 = boton(jugador4, 447, 593)
            jugador_2 = boton(jugador1, 0, 296)
            jugador_3 = boton(jugador2, 457, 0)
            jugador_4 = boton(jugador3, 896, 298)

        #Constructor de cartas
        global ataque, salto, favr, futuro, bomba, defensa, comodin_1, comodin_2, comodin_3,comodin_4, comodin_5, barajar, no
        ataque = imagenes(attack)
        salto = imagenes(skip)
        favr = imagenes(favor)
        futuro = imagenes(seethefuture)
        bomba = imagenes(bomb)
        defensa = imagenes(defuse)
        comodin_5 = imagenes(comodin5)
        comodin_4 = imagenes(comodin4)
        comodin_3 = imagenes(comodin3)
        comodin_2 = imagenes(comodin2)
        comodin_1 = imagenes(comodin1)
        barajar = imagenes(shuffle)
        no = imagenes(nope)

        #Botones, baraja y otros
        global baraja, restar_b
        baraja= imagenes(Baraja)
        pause= boton(boton_pause, 905, 5)
        play= boton(boton_play, 435 , 500)
        restar_b = boton(restart, 418, 501)
        boton_azul= boton(turn, 5 , 637)
        mark= imagenes(marco)
        font= pygame.font.SysFont("Showcard Gothic", 80)
        texto1= font.render("Exploding Kittens", 0, (255,255,255))

        #variables
        blit_mazo= False
        partida= False
        turnos= False

        #Ponerle el icono y el nombre a la ventana
        pygame.display.set_caption("Exploding Kittens")
        pygame.display.set_icon(icon)

        while self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = False
                    self.player.send("desconectado".encode())
                    self.player.close()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.cursor.colliderect(pause.rect):
                        self.send_msg("pausar")
                    elif self.cursor.colliderect(play.rect):
                        self.send_msg("iniciar partida")
                        partida= True
                    elif self.cursor.colliderect(restar_b.rect):
                        self.inicializar()
                    elif self.cursor.colliderect(baraja.rect) and turnos:
                        self.send_msg("baraja")
                    elif self.cursor.colliderect(boton_azul.rect) and turnos:
                        self.send_msg("Final turno")
                    elif self.cursor.colliderect(defensa.rect) and turnos:
                        self.send_msg("defensa")
                    elif self.cursor.colliderect(no.rect) and turnos:
                        self.send_msg("no")
                    elif self.cursor.colliderect(barajar.rect) and turnos:
                        self.send_msg("barajar")
                    elif self.cursor.colliderect(favr.rect) and turnos:
                        self.send_msg("favor")
                    elif self.cursor.colliderect(futuro.rect) and turnos:
                        self.send_msg("futuro")
                    elif self.cursor.colliderect(ataque.rect) and turnos:
                        self.send_msg("ataque")
                    elif self.cursor.colliderect(salto.rect) and turnos:
                        self.send_msg("saltar")





                self.screen.blit(background, (0,0))
                if partida== False:
                    mark.draw(self.screen, 0, 0)
                    play.draw(self.screen)
                else:
                    baraja.draw(self.screen, 360, 283)
                    pause.draw(self.screen)
                    if self.mensaje == "cargar" or self.mensaje == "partida iniciada" or blit_mazo:
                        self.abrir()
                        time = 0
                        while time < 120:
                            time += 1
                        blit_mazo = True
                        m = 'mazo' + id
                        self.dibujar_cartas(110, 450, 100, 77, m)
                        if self.datos['baraja_a'] != []:
                            self.dibujar_cartas(510, 266, 0, 0, 'baraja_a')
                    if self.mensaje == "Listo":
                        turnos = False
                    if self.mensaje == "tu turno":
                        turnos = True
                    if turnos:
                        boton_azul.draw(self.screen)

                    jugador_1.draw(self.screen)
                    jugador_2.draw(self.screen)
                    jugador_3.draw(self.screen)
                    jugador_4.draw(self.screen)


                self.cursor.update()
                self.clock.tick(60)

                pygame.display.update()
                pygame.display.flip()


game= game()
