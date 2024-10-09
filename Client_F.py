## CLIENT ##

import socket
import time
import ClientParser

HOST = '172.30.115.35' ## server에 출력되는 ip를 입력해주세요 ##
PORT = 9999
serverID = "S0001001"
clientID = "D000F001"
parser = ClientParser.Parser()


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
client_socket.connect((HOST, PORT))

def client_start():
    try:
        while True:
            # 서버로부터 명령 수신
            response = client_socket.recv(512)
            print(f"확인 : {response}")

            result = parser.data_decoding(response)
            print(f"센서 커맨드 확인 : {result.commend}")
            if result.commend == 1:
                for i in range(1, 6):
                    message = parser.data_encoding(serverID, clientID, 1, "no"+str(i)+"fData")
                    # 명령을 받으면 데이터 송신
                    client_socket.sendall(message)
                    print(f"클라이언트가 서버에게 데이터 송신: {message}")
                    time.sleep(3)
            elif result.commend == 2:
                message = parser.data_encoding(serverID, clientID, 2, "OK")
                client_socket.sendall(message)
            elif result.commend == 9:
                message = parser.data_encoding(serverID, clientID, 9, "OK")
                # 명령을 받으면 데이터 송신
                client_socket.sendall(message)
    except KeyboardInterrupt:
        print("클라이언트 종료")
        client_socket.close()


if __name__ == "__main__":
    client_start()