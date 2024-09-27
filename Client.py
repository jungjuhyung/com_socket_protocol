## CLIENT ##

import socket
import time
import struct
from _thread import *
import Packet as packet

HOST = '192.168.0.11' ## server에 출력되는 ip를 입력해주세요 ##
PORT = 9999
client_id = 0x00000002

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

try:
    while True:
        # 서버로부터 명령 수신
        data = client_socket.recv(512)
        print(data)
        if packet.response_check(data):
            target, req_device, cmd = packet.cmd_parser(data)
            print(f"target : {target}")
            print(f"req_device : {req_device}")
            print(f"cmd : {cmd}")
            if cmd ==7:
                # 명령을 받으면 데이터 송신
                print("아이디 확인 cmd")
                client_socket.sendall(packet.response_id(target,client_id))
                print(f"클라이언트가 서버에게 데이터 송신: {packet.response_id(target,client_id)}")
            elif cmd == 1:
                print("확인")
            else:
                print(f"알 수 없는 명령: {data}")
except KeyboardInterrupt:
    print("클라이언트 종료")

client_socket.close()