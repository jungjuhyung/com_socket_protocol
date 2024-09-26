import socket
import time
import threading
from _thread import *

client_sockets = []

Host = socket.gethostbyname(socket.gethostname())
Port = 9999

print(f"Host ip >> {Host}")

#### 스레드에서 실행될 함수 정의

def handle_client(client_socket, addr):
    print(f"클라이언트 연결됨: {addr}")
    client_sockets.append(client_socket)  # 클라이언트 소켓 추가

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

# 서버 소켓이 종료된 후에도 동일한 Host와 Post로 빠르게 재시작할 수 있도록 포트 재사용 허용 코드
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 센서에서 연결을 시도할 때 지정할 Host와 Port
server_socket.bind((Host, Port))

# 최대 3개까지 연결 가능
server_socket.listen(3)


#### sensor소켓과 server소켓 연결
try:
    while True:
        client_socket, addr = server_socket.accept()
        # 클라이언트를 별도의 스레드에서 처리
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()


        if(len(client_sockets) == 3):
            # 20ms 마다 모든 클라이언트에게 데이터 전송 요청
            while True:
                message = "SEND_DATA".encode('utf-8')
                for client in client_sockets:
                    client.sendall(message)
                print("서버가 모든 클라이언트에게 데이터 전송 요청을 보냈습니다.")
                time.sleep(0.02)  # 20ms 대기
        else:
            continue
except KeyboardInterrupt:
    print("서버 종료")
finally:
    server_socket.close()

