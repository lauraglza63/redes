from socket import *
import sys
if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 8888)) # Fill in start.
tcpSerSock.listen(1) # Fill in end.

while 1:
    # Strat receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(4096).decode() # Fill in start. # Fill in end.
    print(message)
    print("--------------------------------------------")
    
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/cache/" + filename
    print(filetouse)
    try: 
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "r") 
        outputdata = f.readlines() 
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode()) 
        tcpCliSock.send("Content-Type:text/html\r\n".encode())
        
        for i in range(len(outputdata)): # Fill in start.
            tcpCliSock.send(outputdata[i].encode()) # Fill in end.

        print('Read from cache')
        f.close()

    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false": 
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM) # Fill in start. # Fill in end.
            hostn = filename.replace("www.","",1) 
            print(hostn) 
            try:
                print('inicio ilegal')
                # Connect to the socket to port 80
                c.connect((hostn, 80)) # Fill in start. # Fill in end.
                print('aqui')

                # Create a temporary file on this socket and ask port 80 for the file requested by the client               
                fileobj = c.makefile("wb", 0)
                fileobj.write(f"GET http://{filename} HTTP/1.0\r\n".encode())
                fileobj.write("\r\n".encode())

                # Create a new file in the cache for the requested file. 
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./cache/" + filename,"wb") 

                while True:
                    resp = c.recv(4096)
                    if not resp:
                        break
                    tmpFile.write(resp)
                    tcpCliSock.send(resp)
                tmpFile.close()


            except:
                print("Illegal request")    
        else:
            # HTTP response message for file not found
            
            tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode()) # Fill in start.
            tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
            tcpCliSock.send("<html><body><h1>404 Not Found</h1></body></html>".encode()) # Fill in end.

    # Close the client and the server sockets 
    tcpCliSock.close() 

tcpSerSock.close() # Fill in start. # Fill in end.