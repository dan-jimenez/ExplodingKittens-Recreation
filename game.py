import socket
import threading
from threading import Timer
from time import *
import sys
import pygame
import json

"""
Primero declaramos todas las imagenes que vamos a utilizar en el juego
"""
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
    """ 
    Esta es la clase cursor que hereda de la clase Rect de pygame
    
    Esta es usada para convertir la posicion del cursor en un retangulo
    """
    def __init__(self):
        #Constructor de la clase cursor
        pygame.Rect.__init__(self, 0, 0, 1, 1)
    def update(self):
        #Funcion update de la clase cursor, no recibe parametros
        self.left, self.top = pygame.mouse.get_pos()
class boton(pygame.sprite.Sprite):
    """
    Clase boton
    Hereda de la clase sprite importada con la libreria pygame
    """
    def __init__(self, imagen1, x, y):
        #Constructor de la clase boton
        self.imagen_normal = imagen1
        self.imagen_actual = self.imagen_normal
        self.rect = self.imagen_actual.get_rect()
        self.rect.left, self.rect.top = (x, y)

    def draw(self, screen):
        """
        Funcion draw de la clase boton
        Sirve para dibujar el boton

        Recibe como unico parametro _screen_ la cual es la pantalla donde se dibujara el boton
        """
        botonDibujado = screen.blit(self.imagen_actual, self.rect)
        return botonDibujado
class imagenes(pygame.sprite.Sprite):
    """
    Clase imagenes, hereda de la clase sprite de la libreria pygame
    """
    def __init__(self, imagen):
        #Constructor de la clase boton
        self.carta = imagen
        self.rect= self.carta.get_rect()

    def draw (self, screen, x, y):
        """
        Funcion draw de la clase imagenes
        Sirve para dibujar las cartas de 
        """
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
    """
    Clase game 
    Aqui se ve contenido todo el juego
    """
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
        """
        Abre un hilo para recibir mensajes
        """

        if True:
            self.inicializar()
        """
        Inicializa el programa
        """

    def msg_recv(self):
        """
        Funcion para recibir los mensajes entrantes desde el servidor

        No recibe parametros
        """
        while True:
            try:
                data = self.player.recv(200000)
                if data:
                    self.mensaje= data.decode()
                    print(data.decode())
            except:
                pass

    def send_msg(self, msg):
        """
        Funcion para enviar mensajes al servidor

        Parametros:

        msg= String con el mensaje
        """
        self.player.send(msg.encode())

    def cargar(self, data):
        """
        Funcion cargar
        Esta funcion carga un diccionario a un json 

        recibe como parametros:
        data= diccionario a cargar
        
        """
        json.dumps(data)
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

    def abrir(self):
        """
        Funcion abrir
        Abre el json que se este utilizando

        No recibe parametros
        """
        with open('data.json') as file:
            self.datos= json.load(file)
        return self.datos

    def game_over(self):
        """
        Funcion game over esta sirve para cuando el jugador pierde

        No recibe parametros
        """
        self.datos['baraja'].remove(self.datos['baraja'][0])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = False
                    self.player.send("desconectado".encode())
                    self.player.close()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.cursor.colliderect(restar_b.rect):
                        self.inicializar()

            self.screen.blit(background, (0,0))
            self.screen.blit(game_over, (254, 175))
            restar_b.draw(self.screen)
            self.cursor.update()
            self.clock.tick(60)

            pygame.display.update()
            pygame.display.flip()


    def imprimir_cartas(self,c ,x, y):
        """
        Funcion para imprimir las cartas en la pantalla

        Parametros:

        c= lista con las cartas que se desea imprimir
        x= entero con la posicion en x
        y = entero con la posicion en y
        """
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

    def dibujar_cartas(self,x, y, aumentox, aumentoy, cartas):
        """
        Funcion para recorrer la lista de cartas que se van a dibujar

        Parametros:
        x= posicion en x(entero)
        y = posicion en y (entero)
        aumentox= entero con el aumento que se hara en x por cada carta
        aumentoy= entero con el aumento que se hara en y por cada 8 cartas
        cartas= string con el nombre de la lista de cartas que se va a imprimir
        """
        x1= x
        if len(self.datos[cartas])<=8:
            if cartas == "mazo1" or cartas == "mazo2" or cartas == "mazo3" or cartas == "mazo4" or cartas == 'cartas_c':
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
                elif self.datos[cartas].index(c) == 16:
                    y += 57
                    x = x1
    def pausa(self):
        """
        Menu pausa

        No recibe parametros
        """
        pausa= True
        while pausa:
            play= boton(boton_play, 435 , 400)
            font= pygame.font.SysFont("Showcard Gothic", 50)
            texto3= font.render("JUEGO PAUSADO", 0, (255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = False
                    self.player.send("desconectado".encode())
                    self.player.close()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.cursor.colliderect(play.rect):
                        pausa= False
            self.screen.blit(background, (0,0))
            self.screen.blit(texto3, (320,250))
            play.draw(self.screen)
            self.cursor.update()
            self.clock.tick(60)

            pygame.display.update()
            pygame.display.flip()
    def escoger_jugador(self):
        """
        Menu para escoger a los jugadores cuando se usa la carta favor
        """
        escoger= True
        font= pygame.font.SysFont("Showcard Gothic", 50)
        texto= font.render("Escoge un jugador", 0, (255,255,255))
        while escoger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = False
                    self.player.send("desconectado".encode())
                    self.player.close()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.cursor.colliderect(player1.rect):
                        self.send_msg('favor1')
                        escoger= False
                    elif self.cursor.colliderect(player2.rect):
                        self.send_msg('favor2')
                        escoger= False
                    elif self.cursor.colliderect(player3.rect):
                        self.send_msg('favor3')
                        escoger = False
                    elif self.cursor.colliderect(player4.rect):
                        self.send_msg('favor4')
                        escoger= False
            self.screen.blit(background, (0,0))
            self.screen.blit(texto, (275,200))
            player1.draw(self.screen, 216, 296)
            player2.draw(self.screen, 362, 303)
            player3.draw(self.screen, 487, 292)
            player4.draw(self.screen,636 ,304)
            self.cursor.update()
            self.clock.tick(60)

            pygame.display.update()
            pygame.display.flip()
    def escoger_jugador2(self):
        """
        Menu para escoger al jugador cuando se usa la carta ataque
        """
        escoger= True
        font= pygame.font.SysFont("Showcard Gothic", 50)
        texto= font.render("Escoge un jugador", 0, (255,255,255))
        while escoger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = False
                    self.player.send("desconectado".encode())
                    self.player.close()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.cursor.colliderect(player1.rect):
                        self.send_msg('ataque1')
                        escoger= False
                    elif self.cursor.colliderect(player2.rect):
                        self.send_msg('ataque2')
                        escoger= False
                    elif self.cursor.colliderect(player3.rect):
                        self.send_msg('ataque3')
                        escoger = False
                    elif self.cursor.colliderect(player4.rect):
                        self.send_msg('ataque4')
                        escoger= False
            self.screen.blit(background, (0,0))
            self.screen.blit(texto, (275,200))
            player1.draw(self.screen, 216, 296)
            player2.draw(self.screen, 362, 303)
            player3.draw(self.screen, 487, 292)
            player4.draw(self.screen,636 ,304)
            self.cursor.update()
            self.clock.tick(60)

            pygame.display.update()
            pygame.display.flip()
    def escoger_carta(self, carta):
        """
        Menu para escoger la carta que deseas dar cuando tienes que hacer un favor
        """
        escoger= True
        font= pygame.font.SysFont("Showcard Gothic", 30)
        texto= font.render("Te ha tocado hacer un favor, escoge una carta para dar", 0, (255,255,255))
        while escoger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = False
                    self.player.send("desconectado".encode())
                    self.player.close()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.cursor.colliderect(defensa.rect):
                        self.send_msg("s_defuse")
                        escoger= False
                    elif self.cursor.colliderect(no.rect):
                        self.send_msg("s_nope")
                        escoger= False
                    elif self.cursor.colliderect(barajar.rect):
                        self.send_msg("s_shuffle")
                        escoger= False
                    elif self.cursor.colliderect(favr.rect):
                        self.send_msg('s_favor')
                        escoger= False
                    elif self.cursor.colliderect(futuro.rect):
                        self.send_msg("s_seethefuture")
                        escoger= False
                    elif self.cursor.colliderect(ataque.rect):
                        self.send_msg("s_attack")
                        escoger= False
                    elif self.cursor.colliderect(salto.rect):
                        self.send_msg('s_skip')
                        escoger= False
                    elif self.cursor.colliderect(comodin_1.rect):
                        self.send_msg('s_comodin1')
                        escoger= False
                    elif self.cursor.colliderect(comodin_2.rect):
                        self.send_msg('s_comodin2')
                        escoger= False
                    elif self.cursor.colliderect(comodin_3.rect):
                        self.send_msg('s_comodin3')
                        escoger= False
                    elif self.cursor.colliderect(comodin_4.rect):
                        self.send_msg('s_comodin4')
                        escoger= False
                    elif self.cursor.colliderect(comodin_5.rect):
                        self.send_msg('s_comodin5')
                        escoger= False

            self.screen.blit(background, (0,0))
            self.screen.blit(texto, (100,60))
            crt= carta
            self.dibujar_cartas(20, 166, 120, 190, crt)
            self.cursor.update()
            self.clock.tick(60)

            pygame.display.update()
            pygame.display.flip()
    def escoger_carta2(self, carta):
        """
        Menu para escoger la carta que deseas obtener cuando usas los 3 comodines
        """
        escoger= True
        font= pygame.font.SysFont("Showcard Gothic", 30)
        texto= font.render("Escoge la carta que quieres que te den", 0, (255,255,255))
        while escoger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = False
                    self.player.send("desconectado".encode())
                    self.player.close()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.cursor.colliderect(defensa.rect):
                        self.datos['cart'].append('defuse')
                        escoger= False
                    elif self.cursor.colliderect(no.rect):
                        self.datos['cart'].append('nope')
                        escoger= False
                    elif self.cursor.colliderect(barajar.rect):
                        self.datos['cart'].append('shuffle')
                        escoger= False
                    elif self.cursor.colliderect(favr.rect):
                        self.datos['cart'].append('favor')
                        escoger= False
                    elif self.cursor.colliderect(futuro.rect):
                        self.datos['cart'].append('seethefuture')
                        escoger= False
                    elif self.cursor.colliderect(ataque.rect):
                        self.datos['cart'].append('attack')
                        escoger= False
                    elif self.cursor.colliderect(salto.rect):
                        self.datos['cart'].append('skip')
                        escoger= False
                    elif self.cursor.colliderect(comodin_1.rect):
                        self.datos['cart'].append('comodin1')
                        escoger= False
                    elif self.cursor.colliderect(comodin_2.rect):
                        self.datos['cart'].append('comodin2')
                        escoger= False
                    elif self.cursor.colliderect(comodin_3.rect):
                        self.datos['cart'].append('comodin3')
                        escoger= False
                    elif selef.cursor.colliderect(comodin_4.rect):
                        self.datos['cart'].append('comodin4')
                        escoger= False
                    elif self.cursor.colliderect(comodin_5.rect):
                        self.datos['cart'].append('comodin5')
                        escoger= False

            self.screen.blit(background, (0,0))
            self.screen.blit(texto, (100,60))
            crt= carta
            self.dibujar_cartas(20, 166, 120, 190, crt)
            self.cursor.update()
            self.clock.tick(60)

            pygame.display.update()
            pygame.display.flip()

    def inicializar(self):
        """
        Funcion que inicializa el juego
        """
        pygame.init()
        #Constructor de jugadores
        global id, m
        id= self.mensaje
        m= 'mazo' + id 
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
        global player1, player2, player3, player4, bombas
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
        player1= imagenes(jugador1)
        player2= imagenes(jugador2)
        player3= imagenes(jugador3)
        player4= imagenes(jugador4)

        #Botones, baraja y otros
        global baraja, restar_b, comodines
        comodines = 0 
        baraja= imagenes(Baraja)
        pause= boton(boton_pause, 905, 5)
        play= boton(boton_play, 435 , 500)
        restar_b = boton(restart, 418, 501)
        boton_azul= boton(turn, 5 , 637)
        mark= imagenes(marco)
        font= pygame.font.SysFont("Showcard Gothic", 50)
        texto1= font.render("¿Que carta vas a dar?", 0, (255,255,255))
        texto2= font.render("¿A quien quieres pedir un favor?", 0, (255,255,255))


        #variables
        blit_mazo= False
        partida= False
        turnos= 0
        muestras= False
        favorr = False

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
                        self.pausa()
                    elif self.cursor.colliderect(play.rect) and partida == False:
                        partida= True
                        self.send_msg("iniciar partida")
                    elif self.cursor.colliderect(baraja.rect) and turnos != 0:
                        bombas=True
                        while self.datos['baraja'][0]== 'bomb' and bombas ==True:
                            bomba.draw(self.screen, 445, 266)
                            sleep(4)
                            self.game_over()
                        self.send_msg("baraja")
                        turnos-= 1
                        sleep(0.3)
                        if turnos == 0:
                            self.send_msg("Final turno")
                    elif self.cursor.colliderect(defensa.rect):
                        self.send_msg("defensa")
                        bombas= False
                    elif self.cursor.colliderect(no.rect) and turnos != 0:
                        self.send_msg("no")
                    elif self.cursor.colliderect(barajar.rect) and turnos != 0:
                        self.send_msg("barajar")
                    elif self.cursor.colliderect(favr.rect) and  turnos != 0:
                        self.escoger_jugador()
                    elif self.cursor.colliderect(futuro.rect) and  turnos != 0:
                        self.send_msg("futuro")
                    elif self.cursor.colliderect(ataque.rect)  and  turnos != 0:
                        self.send_msg('ataque')
                        sleep(0.3)
                        self.send_msg('Final Turno')
                    elif self.cursor.colliderect(salto.rect):
                        turnos -= 1
                        if turnos == 0 :
                            self.send_msg("saltar")
                    elif self.cursor.colliderect(comodin_1.rect) and turnos != 0:
                        comodines += 1
                        self.datos['men'].append("comodin1")
                    elif self.cursor.colliderect(comodin_2.rect) and turnos != 0:
                        comodines += 1
                        self.datos['men'].append("comodin2")
                    elif self.cursor.colliderect(comodin_3.rect) and turnos != 0:
                        comodines += 1
                        self.datos['men'].append('comodin3')
                    elif self.cursor.colliderect(comodin_4.rect) and turnos != 0:
                        comodines += 1
                        self.datos['men'].append('comodin4')
                    elif self.cursor.colliderect(comodin_5.rect) and turnos != 0:
                        comodines += 1
                        selfl.datos['men'].append('comodin5')
                    elif self.cursor.colliderect(jugador_1) and turnos !=0:
                        if comodines == 2:
                            self.send_msg('comodinesCon2para1')
                        elif comodines == 3:
                            self.escoger_carta2('cartas_c')
                            self.send_msg('comodinesCon3para1')
                    elif self.cursor.colliderect(jugador_2) and turnos !=0:
                        if comodines == 2:
                            self.send_msg('comodinesCon2para2')
                        elif comodines == 3:
                            self.send_msg('comodinesCon3para2')
                            self.escoger_carta2('cartas_c')
                    elif self.cursor.colliderect(jugador_3) and turnos !=0:
                        if comodines == 2:
                            self.send_msg('comodinesCon2para3')
                        elif comodines == 3:
                            self.escoger_carta2('cartas_c')
                            self.send_msg('comodinesCon3para3')
                    elif self.cursor.colliderect(jugador_4) and turnos !=0:
                        if comodines == 2:
                            self.send_msg('comodinesCon2para4')
                        elif comodines == 3:
                            self.escoger_carta2('cartas_c')
                            self.send_msg('comodinesCon3para4')



                self.screen.blit(background, (0,0))
                if partida:
                    baraja.draw(self.screen, 360, 283)
                    pause.draw(self.screen)
                    if self.mensaje == "Listo":
                        turnos = 0
                    if self.mensaje == "tu turno":
                        turnos += 1
                    if self.mensaje == "muestra":
                        muestras= True
                    if self.mensaje == "favor":
                        self.escoger_carta(m)
                    if turnos > 0:
                        boton_azul.draw(self.screen)
                    if self.mensaje == "cargar" or self.mensaje == "partida iniciada" or blit_mazo:
                        self.abrir()                     
                        blit_mazo = True
                        self.dibujar_cartas(110, 450, 100, 77, m)
                        self.dibujar_cartas(510, 266, 0, 0, 'baraja_a')
                        if muestras:
                            self.dibujar_cartas(225, 266, 140, 0, 'muestras')
                            sleep(2)
                            self.datos['muestras']= []
                            self.send_msg("cargar")
                            muestras = False

                    jugador_1.draw(self.screen)
                    jugador_2.draw(self.screen)
                    jugador_3.draw(self.screen)
                    jugador_4.draw(self.screen)
                else:
                    mark.draw(self.screen, 0, 0)
                    play.draw(self.screen)

                self.cursor.update()
                self.clock.tick(60)

                pygame.display.update()
                pygame.display.flip()


game= game()
