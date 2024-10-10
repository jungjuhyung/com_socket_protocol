import struct
from DataClass import DecodingData


"""
 - STX, ETX => 1byte(uint8)
 - device_id => 8byte(uint64)
 - CMD => 2byte(uint16) => 01~FF(1byte는 패딩될 예정)
 - OK신호 => 2byte(ASCII 문자)
 - status_signal => 2byte 패딩(0~99 정수)
 - 요청idx => 3byte 패딩(0부터 1씩 증가 정수)
 - 측정idx => 3byte 패딩(1~5 정수)
 - 적외선 데이터 => 8*8*3(각 데이터를 3byte씩 패딩 정수) => 여기서는 float의 4바이트로 패킹
 - 거리 데이터 => 8*8*3(각 데이터를 3byte씩 패딩 정수) => 여기서는 int의 4바이트로 패킹
 - 온도 센서 => 5byte(4byte 실수 + 1byte 온도부호로 추정)
 - 습도 센세 => 2byte(2byte uint8 0~100 정수 + 1byte %문자로 추정)
 - 조도 센서 => 5byte(4byte 실수 + 1byte 조도부호로 추정)
"""

# 요청 시작, 끝 제어문자 => B(1byte 부호없는 정수) 로 패킹
STX = 0x02 # 1byte
ETX = 0x03 # 1byte

# 응답 시작, 끝 제어문자 => B 로 패킹
SOH = 0x01 # 1byte
EOH = 0x04 # 1byte

# 커맨드(CMD) => <H(2byte 부호 없는 정수) 리틀 엔디안으로 패킹, 값울 주소의 뒤에부터 채우기
data_cmd = "01" # 2byte
change_cmd = "02" # 2byte
keepalive_cmd = "09" # 2byte

# clientID => 8s(8byte 문자열)로 패킹
"""
serverID = S0001001 # 8byte
clientID = 0x00000002 # 8byte
clientID = 0x00000003 # 8byte
clientID = 0x00000004 # 8byte
"""

class Parser :

    def data_encoding(self, targetID, requestID, cmd, data):
        packet = struct.pack(
            f'=B8s8s2s{len(data)}sB',
            SOH,  # STX
            targetID.encode('utf-8'),  # 타겟 장치
            requestID.encode('utf-8'),  # 요청 장치
            cmd.encode('utf-8'),  # 요청 명령
            data.encode('utf-8'),
            EOH  # ETX
        )
        return packet

    def data_decoding(self, data):
        if data[0] == STX and data[-1] == ETX:
            data = data[1:-1]
            d_data = DecodingData()

            targetID, requestID, commend = struct.unpack("8s8s2s", data[0:18])
            d_data.targetID = targetID.decode("utf-8")
            d_data.requestID = requestID.decode("utf-8")
            d_data.commend = commend.decode("utf-8")

            if d_data.commend == data_cmd:
                d_data.data = "데이터 커멘드"
            elif d_data.commend == change_cmd:
                print(data[18:].decode("utf-8"))
                d_data.data = data[18:].decode("utf-8")
            elif d_data.commend == keepalive_cmd:
                d_data.data = "KEEPALIVE 커멘드"

            return d_data
        else:
            return None