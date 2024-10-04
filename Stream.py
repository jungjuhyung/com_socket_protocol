import queue
import Parser

class Stream:
    def __init__(self, front_queue, side_queue, ceiling_queue, host_code):
        self.front_queue = front_queue  # 외부에서 전달받은 front_queue 객체
        self.side_queue = side_queue
        self.ceiling_queue = ceiling_queue
        self.info_Sensor_List = []
        self.host_code = host_code
        self.parser = Parser.Parser(host_code)

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
