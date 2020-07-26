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

    """
    Funcion para enviar mensajes de llegadas a todos los jugadores conectados
    Recibe como parametros 
    msg: mensaje entrante
    jugador: el jugador que envio el mensaje
    """
    """
    Funcion para aceptar una conexion
    
    No recibe parametros
     """

    def aceptarCon(self):
        while True:
            try:
                conn, addr = self.serv.accept()
                conn.setblocking(False)
                self.jugadores.append(conn)
                i = conn
                self.plays(i)
            except:
                pass
            """
            Metodo para procesar los mensajes entrantes
            
            No recibe parametros
            """

    def procesarCon(self):
        while True:
            if len(self.jugadores) > 0:
                for j in self.jugadores:
                    try:
                        data = j.recv(200000)
                        if data:
                            print(data.decode())
                            self.analizar(data.decode(), j)
                    except:
                        pass

    def barajar_repartir(self, datos):
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
        for i in self.jugadores:
            for c in range(0, 7):
                mazo= str('mazo'+ str((self.jugadores.index(i)+1)))
                datos[mazo].append(datos['baraja'][self.jugadores.index(i)])
                datos['baraja'].remove(datos['baraja'][self.jugadores.index(i)])
    def turnos(self, j):
        for c in self.jugadores:
            if c == j:
                if self.jugadores.index(c)== (len(self.jugadores)-1) :
                    jugador =0
                    self.jugadores[jugador].send("tu turno".encode())
                    self.turno = self.jugadores[jugador]
                else:
                    jugador = self.jugadores.index(c)
                    jugador += 1
                    self.jugadores[jugador].send("tu turno".encode())
                    self.turno = self.jugadores[jugador]
            else:
                pass


    def press_baraja(self, datos, j):
        if j == self.jugadores[0]:
            datos['mazo1'].append(datos['baraja'][0])
            datos['cartas_c'].append(datos['baraja'][0])
            datos['baraja'].remove(datos['baraja'][0])
            self.cargar(datos)
            self.msg_to_all("cargar".encode())
        elif j == self.jugadores[1]:
            datos['mazo2'].append(datos['baraja'][0])
            datos['cartas_c'].append(datos['baraja'][0])
            datos['baraja'].remove(datos['baraja'][0])
            self.cargar(datos)
            self.msg_to_all("cargar".encode())
        elif j == self.jugadores[2]:
            datos['mazo3'].append(datos['baraja'][0])
            datos['cartas_c'].append(datos['baraja'][0])
            datos['baraja'].remove(datos['baraja'][0])
            self.cargar(datos)
            self.msg_to_all("cargar".encode())
        elif j == self.jugadores[3]:
            datos['mazo4'].append(datos['baraja'][0])
            datos['cartas_c'].append(datos['baraja'][0])
            datos['baraja'].remove(datos['baraja'][0])
            self.cargar(datos)
            self.msg_to_all("cargar".encode())

    def defensa(self, datos, j):
        if j == self.jugadores[0]:
            datos['mazo1'].remove("defuse")
            datos['mazo1'].remove("bomb")
            datos['cartas_c'].append("defuse")
            datos['cartas_c'].append("bomb")
            self.cargar(datos)
            self.msg_to_all("cargar".encode())
        elif j == self.jugadores[1]:
            datos['mazo2'].remove("defuse")
            datos['cartas_c'].append("defuse")
            datos['mazo2'].remove("bomb")
            datos['cartas_c'].append("bomb")
            self.cargar(datos)
            self.msg_to_all("cargar".encode())
        elif j == self.jugadores[2]:
            datos['mazo3'].remove("defuse")
            datos['mazo3'].remove("bomb")
            datos['cartas_c'].append("defuse")
            datos['cartas_c'].append("bomb")
            self.cargar(datos)
            self.msg_to_all("cargar".encode())

        elif j == self.jugadores[3]:
            datos['mazo4'].remove("defuse")
            datos['mazo4'].remove("bomb")
            datos['cartas_c'].append("defuse")
            datos['cartas_c'].append("bomb")
            self.cargar(datos)
            self.msg_to_all("cargar".encode())

    def favor(self, datos, j):
        if j == self.jugadores[0]:
            datos['mazo1'].remove("defuse")
            datos['mazo1'].remove("bomb")
            datos['cartas_c'].append("defuse")
            datos['cartas_c'].append("bomb")
            self.cargar(datos)
            self.msg_to_all("cargar".encode())
        elif j == self.jugadores[1]:
            datos['mazo2'].remove("defuse")
            datos['cartas_c'].append("defuse")
            datos['mazo2'].remove("bomb")
            datos['cartas_c'].append("bomb")
            self.cargar(datos)
            self.msg_to_all("cargar".encode())
        elif j == self.jugadores[2]:
            datos['mazo3'].remove("defuse")
            datos['mazo3'].remove("bomb")
            datos['cartas_c'].append("defuse")
            datos['cartas_c'].append("bomb")
            self.cargar(datos)
            self.msg_to_all("cargar".encode())
        elif j == self.jugadores[3]:
            datos['mazo4'].remove("defuse")
            datos['mazo4'].remove("bomb")
            datos['cartas_c'].append("defuse")
            datos['cartas_c'].append("bomb")
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
            'baraja_a': []
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
        while n > 60:
            n += 1
        return True

    def analizar(self, data, j):
        turn= self.turno
        if data == "desconectado":
            print("Jugador desconectado")
            self.jugadores.remove(j)
        elif data == "iniciar partida":
            if self.partida ==False:
                self.create()
                print("Se ha iniciado la partida")
                self.jugadores[0].send("tu turno".encode())
                self.barajar_repartir(self.abrir())
                self.partida= True
                self.turno= self.jugadores[0]
                time= 0
                while time<120000:
                    time+= 1
                self.msg_to_all("partida iniciada".encode())
            else:
                print('Ya hay una partida iniciada')
        elif data == "baraja" and turn== j:
            self.press_baraja(self.abrir(),j)
        elif data== 'defensa' and turn == j:
            self.defensa(self.abrir(), j)
        elif data == 'Final turno' and turn == j:
            self.turnos(j)
            j.send('Listo'.encode())

        else:
            self.msg_to_all(data.encode())


s = serv()
