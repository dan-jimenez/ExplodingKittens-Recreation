import socket
import json
import threading
import random
import sys
from typing import TextIO

class serv():
    def __init__(self):
        self.jugadores = []
        self.playing = 0
        self.serv = socket.socket()
        self.serv.bind(('localhost', 8000))
        self.serv.listen(4)
        self.serv.setblocking(False)
        self.partida= False
        self.turno= str

        self.create()
        aceptar = threading.Thread(target=self.aceptarCon)
        aceptar.daemon = True
        aceptar.start()

        procesar = threading.Thread(target=self.procesarCon)
        procesar.daemon = True
        procesar.start()

        self.cerrar()

        """
        Bucle con un input para detectar cuando el usuario quiera cerrar el servidor
        """
    def plays(self, i):
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
        datos= diccionario donde se almacenan datos del juego
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
        datos=  diccionario donde se manejan datos del juego
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

    def saber_player(self,j, jugador):
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
        jugador = ''
        jugador = self.saber_player(j, jugador)
        mazo = 'mazo' + jugador
        datos[mazo].remove("shuffle")
        datos['baraja_a'].append("shuffle")
        random.shuffle(datos['baraja'])
        self.cargar(datos)
        self.msg_to_all("cargar".encode())
    def favor(self, datos, j):
        jugador = ''
        jugador = self.saber_player(j, jugador)
        mazo = 'mazo' + jugador
        datos[mazo].remove("favor")
        datos['baraja_a'].append("favor")
        carta = ""
        while carta == "":
            pass
        cart = carta.removeprefix("send-")
        datos[mazo].append(cart)
        self.cargar(datos)
        self.msg_to_all("cargar".encode())


    def create(self):
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
            'muestras': []
        }
        self.cargar(data)

    def cargar(self, data):
        json.dumps(data)
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

    def cerrar(self):
        while True:
            try:
                msg = input('->')
                if msg == 'salir':
                    self.serv.close()
                    sys.exit()
            except:
                pass

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
        with open('data.json') as file:
            datos = json.load(file)
        return datos

    def contador(self):
        n = 0
        while n > 99990000:
            n += 1
        pass

    def analizar(self, data, j):
        if data == "desconectado":
            print("Jugador desconectado")
            self.jugadores.remove(j)
        elif data == "iniciar partida":
            if self.partida ==False:
                self.create()
                print("Se ha iniciado la partida")
                j.send("tu turno".encode())
                self.barajar_repartir(self.abrir())
                self.partida= True
                self.turno= j
                self.contador()
                self.msg_to_all("partida iniciada".encode())
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
            self.contador()
            j.send("muestra".encode())
        elif data == 'saltar' and self.turno ==j:
            self.saltar(self.abrir(), j)
        elif data == 'Final turno' and self.turno == j:
            self.turnos(j)
            j.send('Listo'.encode())
        elif data == "favor1":
            favor_para= j
            self.jugadores[0].send("favor".encode())
        elif data == "favor2":
            favor_para= j
            self.jugadores[1].send('favor'.encode())
        elif data == "favor3":
            favor_para= j
            self.jugadores[2].send('favor'.encode())
        elif data == "favor4":
            favor_para= j
            self.jugadores[3].send('favor'.encode())
        elif data == "send-nope":
            self.favor(self.abrir(), j, "nope")
        elif data == "send-attack":
            self.favor(self.abrir(), j, "attack")
        elif data == "send-seethefuture":
            self.favor(self.abrir(), j, "seethefuture")
        elif data == "send-shuffle":
            self.favor(self.abrir(), j, "shuffle")
        elif data == "send-comodin1":
            self.favor(self.abrir(), j, "comodin1")
        elif data == "send-comodin2":
            self.favor(self.abrir(), j, "comodin2")
        elif data == "send-comodin3":
            self.favor(self.abrir(), j, "comodin3")
        elif data == "send-comodin4":
            self.favor(self.abrir(), j, "comodin4")
        elif data == "send-comodin5":
            self.favor(self.abrir(), j, "comodin5")
        elif data == "send-skip":
            self.favor(self.abrir(), j, "skip")
        elif data == "send-defuse":
            self.favor(self.abrir(), j, "defuse")
        elif data == "send-favor":
            self.favor(self.abrir(), j, "favor")
        else:
            self.msg_to_all(data.encode())


s = serv()
