import queue

import Stream
import DataLogger
import DataClass
import time

front_queue = queue.Queue()
ceiling_queue = queue.Queue()
side_queue = queue.Queue()

codeData = DataClass.CodeData()
dataLogger = DataLogger.DataLogger()
stream = Stream.Stream(front_queue, side_queue, ceiling_queue)


def scheduler_start():
    try:
        print(f"서버 IP : {stream.server_ip}\n")
        while True:
            print(f"현재 연결 수 : {len(stream.info_Sensor_List)}\n")
            if len(stream.info_Sensor_List) != 3:
                stream.connect()
                continue
            stream.send_sensor(codeData.dataCmd, "1")
            ai_count = 0
            while ai_count != 5:
                if front_queue.qsize() >= 1 and side_queue.qsize() >= 1 and ceiling_queue.qsize() >= 1:
                    ai_count += 1
                    print(f"카운트 : {ai_count}번째\n")
                    if len(dataLogger.source_Data_Set) > 9:
                        dataLogger.source_Data_Set.pop(0)
                        dataLogger.source_Data_Update(front_queue,side_queue,ceiling_queue)
                    else:
                        dataLogger.source_Data_Update(front_queue, side_queue, ceiling_queue)
                    print(f"데이터 로거 : {dataLogger.source_Data_Set}\n"
                          f"데이터 로거 갯수 : {len(dataLogger.source_Data_Set)}\n")

                else:
                    continue


            status = input("위험(e) or 안전(s) or 계속(c) >> ")
            change_status = True
            if status == "e":
                stream.send_sensor(codeData.changeCmd, codeData.redData)
                while change_status:
                    if front_queue.qsize() >= 1 and side_queue.qsize() >= 1 and ceiling_queue.qsize() >= 1:
                        front_queue.get()
                        side_queue.get()
                        ceiling_queue.get()
                        change_status = False
            elif status == "s":
                stream.send_sensor(codeData.changeCmd, codeData.greenData)
                while change_status:
                    if front_queue.qsize() >= 1 and side_queue.qsize() >= 1 and ceiling_queue.qsize() >= 1:
                        front_queue.get()
                        side_queue.get()
                        ceiling_queue.get()
                        change_status = False
            elif status == "c":
                continue
            else:
                continue

    except KeyboardInterrupt:
        print("서버 종료")
    finally:
        stream.server_socket.close()


if __name__ == "__main__":
    scheduler_start()
