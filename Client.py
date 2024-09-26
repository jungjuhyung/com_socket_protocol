## CLIENT ##

import socket
import time
from _thread import *

HOST = '' ## server에 출력되는 ip를 입력해주세요 ##
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

try:
    while True:
        # 서버로부터 명령 수신
        command = client_socket.recv(1024).decode('utf-8')
        if command == "SEND_DATA":
            # 명령을 받으면 데이터 송신
            data_to_send = f"Sensor Data at {time.time()}"
            client_socket.sendall(data_to_send.encode('utf-8'))
            print(f"클라이언트가 서버에게 데이터 송신: {data_to_send}")
        else:
            print(f"알 수 없는 명령: {command}")
except KeyboardInterrupt:
    print("클라이언트 종료")

client_socket.close()