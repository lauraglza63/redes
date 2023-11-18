import socket
import sys


# Check the number of command line arguments
if len(sys.argv) < 4:
    print("Use: python multi_short_client.py server_host server_port file_name")
    
else:
    server_host = sys.argv[1]  # Server IP address or host name
    server_port = int(sys.argv[2])  # Server port
    file_path = sys.argv[3]  # Path of the requested object on the server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server
        client_socket.connect((server_host, server_port))

        # Send an HTTP GET request to the server
        request = f"GET /{file_path} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
        client_socket.sendall(request.encode())

        # Receive response from server
        response = client_socket.recv(1024)
        print(response.decode())

    except Exception as e:
        print(f"Error connecting to server: {e}")

    finally:
        # Close the client socket
        response = client_socket.recv(1024)
        print(response.decode())
        client_socket.close()




#python3 multi_short_client.py 127.0.0.1 12000 index.html