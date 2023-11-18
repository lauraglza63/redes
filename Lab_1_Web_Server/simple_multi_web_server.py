import socket
import threading
import sys

def serve_client(connectionSocket, clientAddr):
    try:
        print('Client Listening on port', clientAddr[1]) 
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        #Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        #Send the content of the requested file to the client
        send = ''
        for i in range(0, len(outputdata)):
            send += outputdata[i]
        connectionSocket.send(f"{send}\r\n".encode())
        connectionSocket.close()
    except IOError:
        # Handle file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html> <head></head> <body><h1>404 Not Found</h1></body> </html>".encode())
        connectionSocket.close()


#Prepare a sever socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 12000))

serverSocket.listen(5)

print('Listening on port', serverSocket.getsockname()[1]) 
print('Ready to serve...')

while True:
    connectionSocket, addr = serverSocket.accept()

    #Serve client in a new thread
    client_handler = threading.Thread(target=serve_client, args=(connectionSocket, addr))
    client_handler.start()
    print(f'Active client {threading.active_count() -1}')

serverSocket.close()
sys.exit()