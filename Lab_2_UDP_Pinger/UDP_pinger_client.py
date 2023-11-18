import time
from socket import *
from statistics import mean

server_host = '127.0.0.1'  # Change this to the actual server IP or name
server_port = 12000

client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1.0)

total_pings = 10
successful_pings = 0
rtt_list = []

for sequence_number in range(total_pings):
    start_time = time.time()

    message = f'Ping {sequence_number + 1} {start_time}'
    
    client_socket.sendto(message.encode(), (server_host, server_port))
    
    try:
        response, server_address = client_socket.recvfrom(1024)
        
        rtt = time.time() - start_time
        rtt_list.append(rtt)
        
        
        print(f'Response from {server_host}: {response.decode()}, RTT = {rtt} seconds')
        
        successful_pings += 1
    except timeout:
        print('Request timed out')

client_socket.close()

if successful_pings > 0:
    percent = (total_pings - successful_pings) / total_pings * 100
    print(f'\nPing statistics for {server_host}:')
    print(f'    Packets: Sent = {total_pings}, Received = {successful_pings}, Lost = {total_pings - successful_pings} ({percent:.2f}% loss)')
    print(f'Approximate round trip times in seconds:')
    print(f'    Minimum = {min(rtt_list):.5f} s, Maximum = {max(rtt_list):.5f} s, Average = {mean(rtt_list) :.5f} s')
else:
    print(f'\nNo responses received. All pings lost.')

