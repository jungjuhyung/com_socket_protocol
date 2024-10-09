import Parser
from DTO import InfoSensor
import socket
import threading


class Stream:
    def __init__(self, front_queue, side_queue, ceiling_queue):
        self.front_queue = front_queue  # 외부에서 전달받은 front_queue 객체
        self.side_queue = side_queue
        self.ceiling_queue = ceiling_queue
        self.info_Sensor_List = []

        self.server_ip = socket.gethostbyname(socket.gethostname())
        self.port = 9999
        self.serverID = "S0001001"
        self.frontID = "D000F001"
        self.ceilingID = "D000C001"
        self.sideID = "D000S001"

        self.parser = Parser.Parser()

        #### server소켓 설정 및 생성
        # IPv4 주소를 사용하는 TCP 소켓 생성
        # socket.AF_INET : IPv4 체계 사용, AF_INET6 사용시 IPv6 사용 가능
        # socket.SOCK_STREAM : TCP 통신 사용, SOCK_DGRAM 사용시 UDP 사용 가능
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #### keepalive 설정(클라이언트측에서도 활성화해야한다.)
        # 활성화
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # keepalive를 보내는 통신두절 간격 설정(10초)
        self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)
        # keepalive를 보내고 응답이 없을시 재확인 신호 전송 간격 설정(5초)
        self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 5)
        # keepalive 재확인 신호의 신호 갯수 설정(3개)
        self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)

        # 서버 소켓이 종료된 후에도 동일한 Host와 Post로 빠르게 재시작할 수 있도록 포트 재사용 허용 코드
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 센서에서 연결을 시도할 때 지정할 Host와 Port
        self.server_socket.bind((self.server_ip, self.port))

        # 연결 대기 및 최대 연결 대기 가능 갯수 설정
        self.server_socket.listen(3)

    def connect(self):
        try:
            client_socket, addr = self.server_socket.accept()
            print(f"센서 클라이언트 연결 : {addr}")
            keepalive = self.parser.data_encoding("KEEPLIVE", self.serverID, 9, "OK")
            client_socket.sendall(keepalive)
            response = client_socket.recv(512)
            print(f"서버 킵얼라이브 요청 확인 : {response}")

            result = self.parser.data_decoding(response)
            print(f"서버 킵얼라이브 요청 객체 : {result}")

            if result.requestID == self.frontID:
                # 클라이언트를 별도의 스레드에서 처리
                client_thread = threading.Thread(target=self.__recv_sensor, args=(client_socket, addr, self.front_queue))

                info_sensor = InfoSensor()
                info_sensor.socket = client_socket
                info_sensor.thread = client_thread
                info_sensor.clientID = result.requestID
                info_sensor.client_ip = addr
                info_sensor.statement = True
                print(f"스레드 생성 및 저장 영역 : {info_sensor}")
                self.info_Sensor_List.append(info_sensor)
                client_thread.start()
            elif result.requestID == self.sideID:
                # 클라이언트를 별도의 스레드에서 처리
                client_thread = threading.Thread(target=self.__recv_sensor, args=(client_socket, addr, self.side_queue))

                info_sensor = InfoSensor()
                info_sensor.socket = client_socket
                info_sensor.thread = client_thread
                info_sensor.clientID = result.requestID
                info_sensor.sensor_ip = addr
                info_sensor.statement = True
                self.info_Sensor_List.append(info_sensor)
                client_thread.start()
            elif result.requestID == self.ceilingID:
                # 클라이언트를 별도의 스레드에서 처리
                client_thread = threading.Thread(target=self.__recv_sensor, args=(client_socket, addr, self.ceiling_queue))

                info_sensor = InfoSensor()
                info_sensor.socket = client_socket
                info_sensor.thread = client_thread
                info_sensor.clientID = result.requestID
                info_sensor.sensor_ip = addr
                info_sensor.statement = True
                self.info_Sensor_List.append(info_sensor)
                client_thread.start()
        except Exception as e:
            print(f"아이디 요청 connect함수 오류 : {e}")

    #### 스레드에서 실행될 함수 정의
    def __recv_sensor(self, client_socket, addr, queue_list):
        print(f"클라이언트 스레드 생성 완료: {addr}")
        try:
            while True:
                # 클라이언트의 메시지를 수신
                response = client_socket.recv(1024)
                result = self.parser.data_decoding(response)
                if not response:
                    print("클라이언트 스레드 응답 오류")
                    break
                print(f"서버가 클라이언트로부터 데이터 수신 => {addr} : {response}\n")
                if result.commend == 1:
                    queue_list.put(result.data)
                elif result.commend == 2:
                    continue
        except Exception as e:
            print(f"클라이언트 연결 오류: {e}")
        finally:
            client_socket.close()  # 클라이언트 소켓 종료
            for i in self.info_Sensor_List:
                if i.socket == client_socket:
                    self.info_Sensor_List.remove(i)
            print(self.info_Sensor_List)
            print(f"클라이언트 연결 종료: {addr}")

    def send_sensor(self, cmd, data):
        for i in self.info_Sensor_List:
            message = self.parser.data_encoding(i.clientID, self.serverID, cmd, data)
            i.socket.sendall(message)
