
## CLIENT ##

import socket
import time
import ClientParser2
import random
from DataClass import CodeData

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999
serverID = "S0001001"
clientID = "D000S001"
parser = ClientParser2.Parser()


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
            if result.commend == CodeData.dataCmd:
                for i in range(1, 6):
                    ir_data = [random.randint(0, 400) for _ in range(64)]
                    distance_data = [random.randint(0, 400) for _ in range(64)]
                    temp_data = round(random.uniform(-20, 40), 2)
                    mois_data = random.randint(1, 99)
                    ill_data = random.randint(1, 999)

                    ir_data_str = ''.join(f'{num:03d}' for num in ir_data)
                    distance_data_str = ''.join(f'{num:03d}' for num in distance_data)
                    result = f"{i:02d},{ir_data_str},{distance_data_str},{temp_data},{mois_data},{ill_data}"

                    message = parser.data_encoding(serverID, clientID, CodeData.dataCmd, result)
                    # 명령을 받으면 데이터 송신
                    client_socket.sendall(message)
                    print(f"클라이언트가 서버에게 데이터 송신: {message}")
                    time.sleep(0.1)
            elif result.commend == CodeData.changeCmd:
                if result.data == "00":
                    message = parser.data_encoding(serverID, clientID, CodeData.changeCmd, "green_change_OK")
                    client_socket.sendall(message)
                elif result.data == "01":
                    message = parser.data_encoding(serverID, clientID, CodeData.changeCmd, "red_change_OK")
                    client_socket.sendall(message)
                else:
                    message = parser.data_encoding(serverID, clientID, CodeData.changeCmd, "change_OK")
                    client_socket.sendall(message)
            elif result.commend == CodeData.keepCmd:
                message = parser.data_encoding(serverID, clientID, CodeData.keepCmd, "OK")
                # 명령을 받으면 데이터 송신
                client_socket.sendall(message)
    except KeyboardInterrupt:
        print("클라이언트 종료")
        client_socket.close()


if __name__ == "__main__":
    client_start()