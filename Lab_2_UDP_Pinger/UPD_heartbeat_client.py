import time
from socket import *

server_host = '127.0.0.1'  # Change this to the actual server IP or name
server_port = 12000

client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1.0)

sequence_number = 1

while True:
    start_time = time.time()
    message = f'Heartbeat {sequence_number} {start_time}'
    client_socket.sendto(message.encode(), (server_host, server_port))
    
    try:
        response, server_address = client_socket.recvfrom(1024)
        end_time = time.time()
        rtt = end_time - start_time
        print(f'Heartbeat response from {server_host}, RTT = {rtt} seconds')
    except timeout:
        print(f'Heartbeat request to {server_host} timed out')
    
    sequence_number += 1
    time.sleep(5)  # Sends a heartbeat every 5 seconds

client_socket.close()
