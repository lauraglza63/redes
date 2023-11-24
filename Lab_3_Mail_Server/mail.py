from client_information import client_information
from base64 import b64encode
from utils import *
import ssl

try:
    user_email, user_password, user_destination_email, user_subject, user_body = client_information()

    mail_server = 'smtp.gmail.com'
    mail_port = 587

    # Connect to the mail server
    client_socket = connect_to_server(mail_server, mail_port)
    print(client_socket.recv(1024).decode())

    # Send EHLO command
    print(send_command(client_socket, 'HELO Alice\r\n'))

    # Upgrade to a secure connection using STARTTLS
    print(send_command(client_socket, 'STARTTLS\r\n'))

    # Wrap the socket with SSL
    ssl_client_socket = ssl.wrap_socket(client_socket, ssl_version=ssl.PROTOCOL_SSLv23)

    # Authentication
    email_A = b64encode(user_email.encode()).decode()
    email_P = b64encode(user_password.encode()).decode()
    
    print(send_command(ssl_client_socket, 'AUTH LOGIN\r\n'))
    print(send_command(ssl_client_socket, email_A + '\r\n'))
    print(send_command(ssl_client_socket, email_P + '\r\n'))

    # Send MAIL FROM command
    print(send_command(ssl_client_socket, 'MAIL FROM: <{}>\r\n'.format(user_email)))

    # Send RCPT TO command
    print(send_command(ssl_client_socket, 'RCPT TO: <{}>\r\n'.format(user_destination_email)))

    # Send DATA command
    print(send_command(ssl_client_socket, 'DATA\r\n'))

    # Send message data
    msg = '\r\n{}'.format(user_body)
    ssl_client_socket.send('Subject: {}\r\n\r\n{}'.format(user_subject, msg).encode())

    # Message ends with a single period
    print(send_command(ssl_client_socket, '\r\n.\r\n'))

    # Send QUIT command
    print(send_command(ssl_client_socket, 'QUIT\r\n'))

    # Close the SSL socket
    ssl_client_socket.close()
    print('Success')

except Exception as e:
    print(f"An error occurred: {e}")
