import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 2345  # The port used by the server
buffer_size = 1024

def creaMatriz(n):
    n=n+1
    matriz=[]
    minas=[]
    #print(n)
    for i in range(n+1):#este for nos permite crear un arreglo de listas de n*n
        a=[0]*n
        matriz.append(a)
    for i in range(n):
        matriz[i][0]=i#asignamos numeros al eje y
        matriz[0][i]=i#asignamos numeros al eje x
    return matriz



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Elige la dificultad:\n1)Principiante (9x9)\n2)Avanzado(16x16)")
    dificultad=input()
    if dificultad == '1':
        n=9
    elif dificultad =='2':
        n=16
    else:
        print("Opción incorrecta")
    dificultad=dificultad.encode('utf-8')
    print("La dificultad es: ",dificultad)
    TCPClientSocket.send(dificultad) #la letra b transforma a binario el mensaje
    matriz=creaMatriz(n)
    for i in range (n+1):
        print(matriz[i])
    while True:
        casilla=input("Envía casilla a verificar:")
        aux=casilla
        aux=aux.split(",")
        casilla=casilla.encode()
        TCPClientSocket.send(casilla)
        #print("Esperando bandera")
        flag=TCPClientSocket.recv(buffer_size)
        flag=flag.decode('utf-8')
        #print("la bandera es:",flag)
        if flag=='1':
            matriz[int(aux[0])][int(aux[1])]=1
            for i in range (n+1):
                print(matriz[i])
        else:
            print("Haz perdidoooo")
            matriz[int(aux[0])][int(aux[1])]='x'
            for i in range (n+1):
                print(matriz[i])
            break
    TCPClientSocket.close()
    '''data = TCPClientSocket.recv(buffer_size)
                print("Recibí,", repr(data), " de", TCPClientSocket.getpeername())'''
    