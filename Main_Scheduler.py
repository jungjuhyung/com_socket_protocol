import queue
import Stream
import DataLogger
import DTO

front_queue = queue.Queue()
ceiling_queue = queue.Queue()
side_queue = queue.Queue()

data_cmd = 1 # 2byte
change_cmd = 2 # 2byte
keepalive_cmd = 9 # 2byte

red = "1"
green = "2"


stream = Stream.Stream(front_queue, side_queue, ceiling_queue)


def scheduler_start():
    try:
        print(f"서버 IP : {stream.server_ip}")
        while True:
            print(f"현재 연결 수 : {len(stream.info_Sensor_List)}")
            if len(stream.info_Sensor_List) != 3:
                stream.connect()
                continue
            stream.send_sensor(data_cmd, "1")
            ai_count = 0
            while ai_count != 5:
                if front_queue.qsize() >= 1 and side_queue.qsize() >= 1 and ceiling_queue.qsize() >= 1:
                    ai_count += 1
                    print(f"카운트 : {ai_count}번쨰")
                    f_data = front_queue.get()
                    s_data = side_queue.get()
                    c_data = ceiling_queue.get()
                    print(f"전방 데이터 : {f_data}\n"
                          f"측면 데이터 : {s_data}\n"
                          f"천장 데이터 : {c_data}")
                else:
                    continue

    except KeyboardInterrupt:
        print("서버 종료")
    finally:
        stream.server_socket.close()


if __name__ == "__main__":
    scheduler_start()
