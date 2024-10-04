import socket

host = socket.gethostbyname(socket.gethostname())
port = 9999
host_id = 1

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(type(server_socket))