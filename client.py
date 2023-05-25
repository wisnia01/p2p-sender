import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 9999)

# Connect to the server
client_socket.connect(server_address)

# Send data to the server
data = 'Hello, server!'
client_socket.send(data.encode())

# Receive a response from the server
response = client_socket.recv(1024)
print('Received response:', response.decode())

# Close the client socket
client_socket.close()