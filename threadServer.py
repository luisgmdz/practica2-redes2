# !/usr/bin/env python3

import socket
import sys
import threading
import random


def servirPorSiempre(socketTcp, listaconexiones):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Conectado a", client_addr)
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr])
            thread_read.start()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)

def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("hilos activos:", threading.active_count())
    print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    print(listaconexiones)

def creaMatriz(n):
    n=n+1
    matriz=[]
    minas=[]
    #print(n)
    for i in range(n):#este for nos permite crear un arreglo de listas de n*n
        a=[0]*n
        matriz.append(a)
    for i in range(n):
        matriz[i][0]=i#asignamos numero al eje y
        matriz[0][i]=i#asignamos letras al eje x
    if n==10:    
        for i in range (10):
            x=int(random.randint(1,n-1))
            y=int(random.randint(1,n-1))
            matriz[x][y]=1#asignamos las minas a la matriz de manera aleatoria 
            minas.append([x,y])#guardamos la posicion de las minas 
    if n==17:
        for i in range (40):
            x=int(random.randint(1,n-1))
            y=int(random.randint(1,n-1))
            matriz[x][y]=1#asignamos las minas a la matriz de manera aleatoria
            minas.append([x,y])#guardamos la posicion de las minas 
    return matriz, minas

def recibir_datos(conn, addr):
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
        while True:
            '''data = conn.recv(256).decode()
                                                print("data:",data)
                                                response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')'''
            #while True:
            print("Esperando a recibir datos... ")
            data = conn.recv(1024)
            print ("los datos recibidos son:",str(data))
            data=data.decode(encoding="utf-8")
            #print("Dificultad*= ",data)
            if data =='1':
                matriz, minas=creaMatriz(9)
                for i in range (10):
                    print(matriz[i])
            elif data == '2':
                matriz, minas=creaMatriz(16)
                for i in range (17): 
                    print(matriz[i])
            else:
                print("El valor ingresado es incorrecto")
            print(minas)
            while True:
                verificar=conn.recv(1024)
                verificar=verificar.decode('utf-8')
                verificar=verificar.split(",")
                print("verificar es:", verificar)
                aux=[]
                print(verificar[0],verificar[1])
                aux.append([int(verificar[0]),int(verificar[1])])
                print(aux[0])
                if aux[0] in minas:
                    flag='0'
                    flag=flag.encode('utf-8')
                    conn.send(flag)
                    break                    
                else:
                    flag='1'
                    flag=flag.encode('utf-8')
                    conn.send(flag)
                conn.sendall(response)
        TCPServerSocket.close()
        '''if not data:
                                    print("Fin")
                                    break'''
        conn.sendall(response)
    except Exception as e:
        print(e)
    finally:
        conn.close()



listaConexiones = []
host, port, numConn = sys.argv[1:4]

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

serveraddr = (host, int(port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")

    servirPorSiempre(TCPServerSocket, listaConexiones)
