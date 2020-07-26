import socket
import json
import threading
import random
from random import randint
import sys
from time import *
from typing import TextIO

class serv():
    """
    Clase serv es la clase que contiene el servidor
    """
    def __init__(self):
        self.jugadores = []
        self.playing = 0
        self.serv = socket.socket()
        self.serv.bind(('localhost', 8000))
        self.serv.listen(4)
        self.serv.setblocking(False)
        self.partida= False
        self.turno= str


        aceptar = threading.Thread(target=self.aceptarCon)
        aceptar.daemon = True
        aceptar.start()
        """
        Abre un hilo para aceptar conexiones
        """

        procesar = threading.Thread(target=self.procesarCon)
        procesar.daemon = True
        procesar.start()
        """
        Abre un hilo para recibir los mensajes y procesarlos
        """

        self.cerrar()
        """
        Llama a la funcion cerrar para poder detectar cuando el usuario quiere cerrar el servidor
        """

    def plays(self, i):
        """
    Funcion Plays sirve para imprimir en la consola cuando alguien se conecta y mandarle su id
    
    Recibe como parametros:
    i= es la ip del jugador que se conecto
        """
        if len(self.jugadores) > 1:
            print("Jugador " + str(len(self.jugadores)) + " conectado")
            i.send((str(len(self.jugadores))).encode())
        else:
            print("Jugador 1 conectado")
            i.send("1".encode())

    def aceptarCon(self):
        """
        Funcion para aceptar una conexion

        No recibe parametros
        """
        while True:
            try:
                conn, addr = self.serv.accept()
                conn.setblocking(False)
                self.jugadores.append(conn)
                i = conn
                self.plays(i)
            except:
                pass
    def cerrar(self):
        """
        Funcion cerrar
        Esta sirve para estar a la espera de que el usuario ingrese ciertas palabras como exit o salir
        para así cerrar el servidor
        """
        while True:
            msg = input('->')
            if msg == 'salir' or msg == 'Salir' or msg == 'exit' or msg == "Exit":
                self.serv.close()
                sys.exit()

    def procesarCon(self):
        """
        Funcion que se encarga de recibir los mensajes

        No recibe parametros
        """
        while True:
            if len(self.jugadores) > 0:
                for j in self.jugadores:
                    try:
                        data = j.recv(200000)
                        if data:
                            print('llegada ' + data.decode())
                            self.analizar(data.decode(), j)
                    except:
                        pass

    def barajar_repartir(self, datos):
        """
        Funcion que se encarga de barajar las cartas y repartirlas cuando se inicia el juego

        Parametros:
        datos= un diccionario con datos del juego

        Tambien llama a la funcion de repartir para poder así repartir las cartas
        """
        for d in datos['defuse']:
            for j in self.jugadores:
                mazo = str('mazo' + str((self.jugadores.index(j) + 1)))
                datos[mazo].append(d)
        for b in datos['cartas']:
            for r in range(0, 4):
                datos['baraja'].append(b)
        random.shuffle(datos['baraja'])
        self.repartir(datos)
        for c in datos['bomb']:
            if len(self.jugadores)>0:
                for i in range(0, (len(self.jugadores)-1)):
                    datos['baraja'].append(c)
        for c in datos['defuse']:
            if len(self.jugadores)==2:
                for i in self.jugadores:
                    datos['baraja'].append(c)
            else:
                for i in range(0, (6- len(self.jugadores))):
                    datos['baraja'].append(c)
        random.shuffle(datos['baraja'])
        self.cargar(datos)
        print("Se ha barajado y repartido las cartas")

    def repartir(self, datos):
        """
        Funcion para repartir las cartas

        Parametros:
        datos= json donde se almacenan datos del juego
        """
        for i in self.jugadores:
            for c in range(0, 7):
                mazo= str('mazo'+ str((self.jugadores.index(i)+1)))
                datos[mazo].append(datos['baraja'][self.jugadores.index(i)])
                datos['baraja'].remove(datos['baraja'][self.jugadores.index(i)])
    def turnos(self, j):
        """
        Funcion para asignar turnos

        Parametros:
        j= El jugador que esta en turno y acaba de terminarlo
        """
        for c in self.jugadores:
            if c == j:
                if self.jugadores.index(c)== (len(self.jugadores)-1):
                    self.jugadores[0].send("tu turno".encode())
                    self.turno = self.jugadores[0]
                else:
                    jugador = self.jugadores.index(c)
                    jugador += 1
                    self.jugadores[jugador].send("tu turno".encode())
                    self.turno = self.jugadores[jugador]
            else:
                pass
    def press_baraja(self, datos, j):
        """
        Funcion para cuando presionan la baraja de cartas
        Le quita una carta a la baraja y se la agrega al jugador

        Parametros:
        datos=  json donde se manejan datos del juego
        j= jugador que hace la accion
        """
        jugador = ''
        jugador = self.saber_player(j, jugador)
        mazo = 'mazo' + jugador
        datos[mazo].append(datos['baraja'][0])
        datos['baraja'].remove(datos['baraja'][0])
        self.cargar(datos)
        self.msg_to_all("cargar".encode())

    def defensa(self, datos, j):
        """
        Funcion Defensa sirve para cuando se usa la carta defuse
        
        Recibe como parametros:

        datos= json donde se manejan los datos
        j= jugador que uso la carta
        """
        jugador = ''
        jugador = self.saber_player(j, jugador)
        mazo = 'mazo' + jugador
        datos[mazo].remove("defuse")
        datos[mazo].remove('bomb')
        datos['baraja_a'].append("defuse")
        datos['baraja'].append('bomb')
        random.shuffle(datos['baraja'])
        self.cargar(datos)
        self.msg_to_all("cargar".encode())
    def futuro(self, datos, j):
        """
        Funcion Futuro sirve para cuando se usa la carta seethefuture
        
        Recibe como parametros:

        datos= json donde se manejan los datos
        j= jugador que uso la carta
        """
        jugador = ''
        jugador = self.saber_player(j, jugador)
        mazo = 'mazo' + jugador
        datos[mazo].remove("seethefuture")
        datos['baraja_a'].append("seethefuture")
        datos['muestras'].append(datos['baraja'][0])
        datos['muestras'].append(datos['baraja'][1])
        datos['muestras'].append(datos['baraja'][2])
        self.cargar(datos)
        self.msg_to_all("cargar".encode())
        print ('si futuro')

    def saber_player(self,j, jugador):
        """
        Funcion Saber_player
        Sirve para detectar el id del jugador que está haciendo una acción

        recibe como parametros:
        j= ip del jugador
        jugador= un string vacio
        """
        if j == self.jugadores[0]:
            jugador= '1'
            return  jugador
        elif j== self.jugadores[1]:
            jugador= '2'
            return jugador
        elif j == self.jugadores[2]:
            jugador = '3'
            return jugador
        elif j== self.jugadores[3]:
            jugador = '4'
            return jugador

    def saltar(self, datos, j):
        
        """
        Funcion saltar sirve para cuando se usa la carta skip
        
        Recibe como parametros:

        datos= json donde se manejan los datos
        j= jugador que uso la carta
        """
        jugador= ''
        jugador= self.saber_player(j, jugador)
        mazo= 'mazo' + jugador
        datos[mazo].remove("skip")
        datos['baraja_a'].append("skip")
        self.cargar(datos)
        self.msg_to_all("cargar".encode())
        self.contador()
        self.turnos(j)
        j.send("Listo".encode())

    def barajar(self, datos, j):
        """
        Funcion barajar sirve para cuando se usa la carta shuffle
        
        Recibe como parametros:

        datos= json donde se manejan los datos
        j= jugador que uso la carta
        """
        jugador = ''
        jugador = self.saber_player(j, jugador)
        mazo = 'mazo' + jugador
        datos[mazo].remove("shuffle")
        datos['baraja_a'].append("shuffle")
        random.shuffle(datos['baraja'])
        self.cargar(datos)
        self.msg_to_all("cargar".encode())
    def favor(self, datos, j, cart):
        
        """
        Funcion favor sirve para cuando se usa la carta favor
        
        Recibe como parametros:

        datos= json donde se manejan los datos
        j= jugador que uso la carta
        """
        jugador = ''
        jugador = self.saber_player(j, jugador)
        mazo = 'mazo' + jugador
        datos[mazo].remove("favor")
        datos['baraja_a'].append("favor")
        datos[mazo].append(cart)
        self.cargar(datos)
        self.msg_to_all("cargar".encode())

    def comodinesCon2(self, datos, j, jugador):
        
        """
        Funcion comodinesCon2 sirve para cuando se usan dos comodines
        
        Recibe como parametros:

        datos= json donde se manejan los datos
        j= jugador que uso la carta
        """
        jugador = ''
        jugador = self.saber_player(j, jugador)
        mazo = 'mazo' + jugador
        for i in datos['men']:
            datos['baraja_a'].append(i)
            datos[mazo].remove(i)
        datos['men']= []
        num= randint(0, (len(datos[jugador])-1))
        datos[mazo].append(datos[jugador][num])
        datos[jugador].remove(datos[jugador][num])
        
        self.cargar(datos)
        self.msg_to_all("cargar".encode())

    def comodinesCon3(self, datos, j, jugador):
        
        """
        Funcion comosdinCon3 sirve para cuando se usan tres comodines
        
        Recibe como parametros:

        datos= json donde se manejan los datos
        j= jugador que uso la carta
        """
        jugador = ''
        jugador = self.saber_player(j, jugador)
        mazo = 'mazo' + jugador
        for i in datos['men']:
            datos['baraja_a'].append(i)
            datos[mazo].remove(i)
        datos['men']= []
        for i in datos[mazo]:
            if i == datos['cart'][0]:
                datos[mazo].append(i)
                datos[jugador].remove(i)
        
        self.cargar(datos)
        self.msg_to_all("cargar".encode())



    def create(self):
        """
        Funcion create
        Crea un diccionario y lo convierte en un json para manejar la informacion

        Parametros:
        Ninguno
        """
        data = {
            'baraja': ["seethefuture", "nope"],
            'cartas': ["attack", "skip", 'favor', "seethefuture", "nope",
                       "shuffle", "comodin1", "comodin2", "comodin3", "comodin4",
                       "comodin5"],
            'bomb': ["bomb"],
            'defuse': ["defuse"],
            'mazo1': [],
            'mazo2': [],
            'mazo3': [],
            'mazo4': [],
            'cartas_c': ["attack", "skip", 'favor', "seethefuture", "nope",
                       "shuffle", "comodin1", "comodin2", "comodin3", "comodin4",
                       "comodin5", "bomb", "defuse"],
            'baraja_a': [],
            'muestras': [],
            'men': [],
            'cart': []
        }
        self.cargar(data)

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

    def msg_to_all(self, msg):
        """
        Funcion para enviar mensajes de llegadas a todos los jugadores conectados
            Recibe como parametros
            msg: mensaje entrante
            jugador: el jugador que envio el mensaje
            """
        for j in self.jugadores:
            try:
                if msg:
                    j.send(msg)
            except:
                pass

    def abrir(self):
        """
        Funcion abrir
        Abre el json que se este utilizando

        No recibe parametros
        """
        with open('data.json') as file:
            datos = json.load(file)
        return datos

    def analizar(self, data, j):
        """
        Funcion analizar 
        Aqui es donde sucede la magia

        Esta funcion recibe todos los mensajes y los procesa para así poder ejecutar una acción

        Recibe como parametros:

        data= el mensaje que acaba de recibir
        j= jugador que realiza la accion
        """
        if data == "desconectado":
            print("Jugador desconectado")
            self.jugadores.remove(j)
        elif data == "iniciar partida":
            if self.partida ==False:
                self.create()
                j.send("tu turno".encode())
                self.barajar_repartir(self.abrir())
                self.partida= True
                self.turno= j
                sleep(0.2)
                self.msg_to_all("partida iniciada".encode())
                print("Se ha iniciado la partida")
            else:
                print('Ya hay una partida iniciada')
        elif data == "baraja" and self.turno ==j:
            self.press_baraja(self.abrir(),j)
        elif data == 'barajar' and self.turno == j:
            self.barajar(self.abrir(), j)
        elif data== 'defensa':
            self.defensa(self.abrir(), j)
        elif data == 'futuro' and self.turno == j:
            self.futuro(self.abrir(), j)
            sleep(0.3)
            j.send("muestra".encode())
            print('si muestra')
        elif data == 'saltar' and self.turno ==j:
            self.saltar(self.abrir(), j)
        elif data == 'Final turno' and self.turno == j:
            self.turnos(j)
            j.send('Listo'.encode())
        elif data == "favor1" and self.turno == j:
            favor_para= j
            self.jugadores[0].send("favor".encode())
        elif data == "favor2"and self.turno == j:
            favor_para= j
            self.jugadores[1].send('favor'.encode())
        elif data == "favor3" and self.turno == j:
            favor_para= j
            self.jugadores[2].send('favor'.encode())
        elif data == "favor4" and self.turno == j:
            favor_para= j
            self.jugadores[3].send('favor'.encode())
        elif data == 's_defuse' and self.turno== favor_para:
            self.favor(self.abrir(), favor_para, 'defuse')
        elif data == 's_nope' and self.turno == favor_para:
            self.favor(self.abrir(), favor_para, 'nope')
        elif data == 's_seethefuture' and self.turno == favor_para:
            self.favor(self.abrir(), favor_para, 'sethefuture')
        elif data == 's_comodin1' and self.turno == favor_para:
            self.favor(self.abrir(), favor_para, 'comodin1')
        elif data == 's_comodin2' and self.turno == favor_para:
            self.favor(self.abrir(), favor_para, 'comodin2')
        elif data == 's_comodin3' and self.turno == favor_para:
            self.favor(self.abrir(), favor_para, 'comodin3')
        elif data == 's_comodin4' and self.turno == favor_para:
            self.favor(self.abrir(), favor_para, 'comodin4')
        elif data == 's_comodin5' and self.turno == favor_para:
            self.favor(self.abrir(), favor_para, 'comodin5')
        elif data == 's_attack' and self.turno == favor_para:
            self.favor(self.abrir(), favor_para, 'attack')
        elif data == 's_skip' and self.turno == favor_para:
            self.favor(self.abrir(), favor_para, 'skip')
        elif data == 's_favor' and self.turno == favor_para:
            self.favor(self.abrir(), favor_para, 'favor')
        elif data == 's_shuffle' and self.turno == favor_para:
            self.favor(self.abrir(), favor_para, 'shuffle')
        elif data== 'ataque' and self.turno == j:
            self.turno(j)
            sleep(0.5)
            self.turno(j)
            sleep(0.5)
            j.send('Listo'.encode())        
        elif data == 'comodinesCon2para1' and self.turno == j:
            self.comodinesCon2(self.abrir(), j, 'mazo1')
        elif data == 'comodinesCon2para2' and self.turno == j:
            self.comodinesCon2(self.abrir(), j, 'mazo2')
        elif data == 'comodinesCon2para3' and self.turno == j:
            self.comodinesCon2(self.abrir(), j, 'mazo3')
        elif data == 'comodinesCon2para4' and self.turno == j:
            self.comodinesCon2(self.abrir(), j, 'mazo4')
        elif data == 'comodinesCon3para1' and self.turno == j:
            self.comodinesCon3(self.abrir(), j, "mazo1")
        elif data == 'comodinesCon3para2' and self.turno == j:
            self.comodinesCon3(self.abrir(), j, "mazo2")
        elif data == 'comodinesCon3para3' and self.turno == j:
            self.comodinesCon3(self.abrir(), j, "mazo3")
        elif data == 'comodinesCon3para4' and self.turno == j:
            self.comodinesCon3(self.abrir(), j, "mazo4")    
        else:
            self.msg_to_all(data.encode())


s = serv()
