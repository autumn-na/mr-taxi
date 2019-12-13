from socket import *

port = 8080

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('10.42.0.1', port))

print('connected')

while True:
    recvData = clientSock.recv(1024)
    print('Enemy :', recvData)

    sendData = input('>>>')
    clientSock.send(sendData)
