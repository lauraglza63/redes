import socket
import sys

cache = {}

if len(sys.argv) <= 1:
    print(
        'Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server]'
    )
    sys.exit(2)

tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(1)

print("Ready to serve...")

while True:
    tcpCliSock, addr = tcpSerSock.accept()
    print("Received a connection from:", addr)

    message = tcpCliSock.recv(4096).decode()
    print(message)
    print("--------------------------------------------")

    request_parts = message.split("\r\n\r\n")
    header = request_parts[0]
    request_method = header.split()[0]
    filename = header.split()[1].partition("/")[2]

    print(f"Request Parts: {request_parts}")
    print(f"Request header: {header}")
    print(f"Request method: {request_method}")
    print(f"Filename: {filename}")

    if filename in cache:
        print("Cache hit")
        for data in cache[filename]:
            tcpCliSock.send(data)

        print("Read from cache")
    else:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostn = filename.replace("www.", "", 1)

        print(f"Connecting to {hostn} on port 80")
        print("--------------------------------------------")

        try:
            c.connect((hostn, 80))

            fileobj = c.makefile("wb", 0)
            fileobj.write(f"{request_method} http://{filename} HTTP/1.0\r\n".encode())
            fileobj.write("\r\n".encode())

            response = []

            while True:
                resp = c.recv(4096)
                if not resp:
                    break
                response.append(resp)
                tcpCliSock.send(resp)

            cache[filename] = response

            print("Connected successfully")
        except socket.error as e:
            print(f"Illegal request: {e}")

    tcpCliSock.close()

