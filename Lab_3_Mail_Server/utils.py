import socket

def connect_to_server(server, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server, port))
        return client_socket
    except socket.error as e:
        print(f"Error connecting to server: {e}")
        raise e

def send_command(socket, command):
    try:
        socket.send(command.encode())
        return socket.recv(1024).decode()
    except socket.error as e:
        print(f"Error sending command: {e}")
        raise e