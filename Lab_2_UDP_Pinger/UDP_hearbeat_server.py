import random
import threading
import time
from socket import *

#Detect client loss
def client_lost_handle(client_status, ):
    while True:
        current_time = time.time()
        for client_address, last_time in list(client_status.items()):
            #If no heartbeat is received in 30 seconds, it is assumed that the client has failed
            if current_time - last_time > 30:  
                print(f'Client at {client_address} has failed')
                del client_status[client_address]


serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12000))

client_status = {}  # Store the last time a heartbeat was received from each client
client_seq = {}     #Store the last sequence number of each PING client

print('Ready to serve...')

client_handler = threading.Thread(target=client_lost_handle, args=(client_status, ))
client_handler.start()

while True:
    rand = random.randint(0, 10)
    message, address = serverSocket.recvfrom(1024)
    message = message.decode()

    print(message)
    word, sequence_number, current_time = message.split()
    client_address = address[0]
            
    if word == 'Heartbeat':
        client_status[address] = float(current_time)
        response_message = f'Heartbeat response to {address}'
        serverSocket.sendto(response_message.encode(), address)

    if rand < 4:
        continue

    if word == 'Ping':
        message = message.upper()
        serverSocket.sendto(message.encode(), address)

        if address not in client_seq.keys():
            client_seq[address] = int(sequence_number)
        else:
            last_seq = client_seq[address]
            seq = int(sequence_number)
            #The time difference is calculated and it is checked if any packet has been lost
            if seq != last_seq + 1:
                print(f"Lost packets from {address}: {last_seq+1} - {seq-1}")
            client_seq[address] = seq
