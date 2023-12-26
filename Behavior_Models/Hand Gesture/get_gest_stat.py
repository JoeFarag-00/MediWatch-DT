import socket

server_address = ('127.0.0.1', 5000)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)

server_socket.listen(1)

print("Waiting for a connection...")

client_socket, client_address = server_socket.accept()

print(f"Connection from {client_address}")

while True:
    data = client_socket.recv(1024)  

    if not data:
        break
    if data is not None:
        result = data.decode('utf-8')

        print("Received Result:", result)

client_socket.close()
server_socket.close()

