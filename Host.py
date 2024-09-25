import socket
from _thread import *

sensor_sockets = []

Host = socket.gethostbyname(socket.gethostname())
Port = 9999

print(f"Host ip >> {Host}")

#### 스레드에서 실행될 함수 정의

def threaded(sensor_socket, addr):
    print('>> Connected by :', addr[0], ':', addr[1])

    ## process until client disconnect ##
    while True:
        try:
            ## send client if data recieved(echo) ##
            data = sensor_socket.recv(1024)

            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break

            print('>> Received from ' + addr[0], ':', addr[1], data.decode())

            ## chat to client connecting client ##
            ## chat to client connecting client except person sending message ##
            for client in sensor_sockets:
                if client != sensor_socket:
                    client.send(data)

        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break

    if sensor_socket in sensor_sockets:
        sensor_sockets.remove(sensor_socket)
        print('remove client list : ', len(sensor_sockets))

    sensor_socket.close()


#### server소켓 설정 및 생성

# IPv4 주소를 사용하는 TCP 소켓 생성
# socket.AF_INET : IPv4 체계 사용, AF_INET6 사용시 IPv6 사용 가능
# socket.SOCK_STREAM : TCP 통신 사용, SOCK_DGRAM 사용시 UDP 사용 가능
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 소켓이 종료된 후에도 동일한 Host와 Post로 빠르게 재시작할 수 있도록 포트 재사용 허용 코드
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 센서에서 연결을 시도할 때 지정할 Host와 Port
server_socket.bind((Host, Port))

server_socket.listen()


#### sensor소켓과 server소켓 연결
try:
    while True:
        print('>> Wait')

        server_socket, addr = server_socket.accept()
        sensor_sockets.append(server_socket)
        start_new_thread(threaded, (server_socket, addr))
        print("참가자 수 : ", len(sensor_sockets))
except Exception as e:
    print('에러 : ', e)

finally:
    server_socket.close()

