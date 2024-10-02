import struct


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
data_req = 1 # 2byte
date_res = 2 # 2byte
status_req = 3 # 2byte
status_res = 4 # 2byte
id_req = 5 # 2byte
id_res = 6 # 2byte

# device id => Q(8byte 부호없는 정수)로 패킹
"""
host_id = 0x00000001 # 8byte
sensor1_id = 0x00000002 # 8byte
sensor2_id = 0x00000003 # 8byte
sensor3_id = 0x00000004 # 8byte
"""

# status_signal => B로 패킹
red = 1
green = 2

def cmd_parser(data):
    print(f"정제 전 : {data}")
    print(len(data))
    data = data[1:-1]
    print(f"정제 후 : {data}")
    print(len(data))
    target, req_device, cmd = struct.unpack("QQH", data)
    return target, req_device, cmd

def request_check(data):
    return data[0] == 0x02 and data[-1] == 0x03

def response_check(data):
    return data[0] == 0x01 and data[-1] == 0x04

def request_id(target_device,request_device):
    packet = struct.pack(
    '=BQQHB',
        STX,  # STX
        target_device,  # 타겟 장치
        request_device,  # 요청 장치
        id_req, # 요청 명령
        ETX  # ETX
    )
    return packet

def response_id(target_device,request_device):
    packet = struct.pack(
    '=BQQHB',
        SOH,  # STX
        target_device,  # 타겟 장치
        request_device,  # 요청 장치
        id_res, # 서버 id
        EOH  # ETX
    )
    return packet

def request_data(target_device,request_device):
    packet = struct.pack(
        '=BQQHB',
        STX,  # STX
        target_device,  # 타겟 장치
        request_device,  # 요청 장치
        data_req,
        ETX  # ETX
    )

    return packet

def response_data(req_idx:int, res_idx:int, target_device,request_device, inf):
    packet = struct.pack(
        '=BQQf64B',
        SOH,  # STX
        target_device,  # 타겟 장치
        request_device,  # 요청 장치
        *inf,
        EOH
    )
    return packet