import socket
import time
import threading
import Parser as packet
import queue
from _thread import *

front_queue = queue.Queue()
ceiling_queue = queue.Queue()
side_queue : queue.Queue()

host_ip = socket.gethostbyname(socket.gethostname())
port = 9999
host_id = "1"

print(f"Host ip >> {host_ip}")
print(type(host_ip))

#### 스레드에서 실행될 함수 정의
def handle_client(client_socket, addr):
    print(f"클라이언트 연결됨: {addr}")
    try:
        while True:
            # 클라이언트의 메시지를 수신
            response = client_socket.recv(1024).decode('utf-8')
            if not response:
                break
            print(f"서버가 클라이언트로부터 데이터 수신: {response}")
    except Exception as e:
        print(f"클라이언트 연결 오류: {e}")
    finally:
        client_socket.close()  # 클라이언트 소켓 종료
        client_sockets.remove(client_socket)  # 클라이언트 소켓 리스트에서 제거
        print(f"클라이언트 연결 종료: {addr}")

#### server소켓 설정 및 생성

# IPv4 주소를 사용하는 TCP 소켓 생성
# socket.AF_INET : IPv4 체계 사용, AF_INET6 사용시 IPv6 사용 가능
# socket.SOCK_STREAM : TCP 통신 사용, SOCK_DGRAM 사용시 UDP 사용 가능
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#### keepalive 설정(클라이언트측에서도 활성화해야한다.)
# 활성화
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
# keepalive를 보내는 통신두절 간격 설정(10초)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)
# keepalive를 보내고 응답이 없을시 재확인 신호 전송 간격 설정(5초)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 5)
# keepalive 재확인 신호의 신호 갯수 설정(3개)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)




# 서버 소켓이 종료된 후에도 동일한 Host와 Post로 빠르게 재시작할 수 있도록 포트 재사용 허용 코드
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 센서에서 연결을 시도할 때 지정할 Host와 Port
server_socket.bind((host, port))

# 연결 대기 및 최대 연결 대기 가능 갯수 설정
server_socket.listen(3)

#### sensor소켓과 server소켓 연결
try:
    while True:
        client_socket, addr = server_socket.accept()
        client_socket.sendall(packet.request_id(0x00000000,host_id))
        data = client_socket.recv(512)
        if packet.response_check(data):
            target, req_device, cmd = packet.cmd_parser(data)
            client_sockets[req_device] = client_socket

            # 클라이언트를 별도의 스레드에서 처리
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_threads[req_device] = client_thread
            client_thread.start()
            print(f"클라이언트 소켓 리스트 : {client_sockets}")
            print(f"클라이언트 스레드 리스트 : {client_threads}")
        if len(client_sockets)==3:
            # 20ms 마다 모든 클라이언트에게 데이터 전송 요청
            while True:
                for client_id, client_socket in client_sockets.items():
                    client_socket.sendall(packet.request_data(client_id, host_id))
                print("서버가 모든 클라이언트에게 데이터 전송 요청을 보냈습니다.")
                time.sleep(0.02)  # 20ms 대기
        else:
            continue
except KeyboardInterrupt:
    print("서버 종료")
finally:
    server_socket.close()

