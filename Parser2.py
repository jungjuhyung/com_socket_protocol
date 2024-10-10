import struct
from DataClass import DecodingData
from scipy import interpolate
import numpy as np


"""
 - STX, ETX => 1byte(uint8)
 - device_id => 8byte(ASCII 문자)
 - CMD => 2byte(ASCII 숫자)
 - OK신호 => 2byte(ASCII 문자)
 - status_signal => 2byte (ASCII 슷자)
 - 측정idx => 2byte 패딩(1~5 ASCII 슷자)
 - 적외선 데이터 => 8*8*3(각 데이터를 3byte씩 ASCII 슷자)
 - 거리 데이터 => 8*8*3(각 데이터를 3byte씩 ASCII 슷자)
 - 온도 센서 => 최대 5~6byte(ASCII 슷자)
 - 습도 센세 => 최대 4byte(ASCII 슷자)
 - 조도 센서 => 최대 5byte(ASCII 슷자)
"""

# 요청 시작, 끝 제어문자 => B(1byte 부호없는 정수) 로 패킹
STX = 0x02 # 1byte
ETX = 0x03 # 1byte

# 응답 시작, 끝 제어문자 => B 로 패킹
SOH = 0x01 # 1byte
EOH = 0x04 # 1byte


# clientID => 8s(8byte 문자열)로 패킹
"""
serverID = S0001001 # 8byte
client_fID = D000F001 # 8byte
client_sID = D000S001 # 8byte
client_cID = D000C001 # 8byte
"""

class Parser :

    def data_encoding(self, targetID, requestID, cmd, data):
        packet = struct.pack(
            f'=B8s8s2s{len(data)}sB',
            STX,  # STX
            targetID.encode('utf-8'),  # 타겟 장치
            requestID.encode('utf-8'),  # 요청 장치
            cmd.encode('utf-8'),  # 요청 명령
            data.encode('utf-8'),
            ETX  # ETX
        )
        return packet

    def data_decoding(self, data):
        if data[0] == SOH and data[-1] == EOH:
            data = data[1:-1]
            d_data = DecodingData()

            targetID, requestID, commend = struct.unpack("8s8s2s", data[0:18])
            d_data.targetID = targetID.decode("utf-8")
            d_data.requestID = requestID.decode("utf-8")
            d_data.commend = commend.decode("utf-8")
            d_data.data = data[18:].decode("utf-8")

            return d_data
        else:
            return None


    def interpolation_64(self, ir_arr_8):
        # cubic interpolation on the image
        # at a resolution of (pix_mult*8 x pix_mult*8)
        xx, yy = (np.linspace(0, 8, 8),
                  np.linspace(0, 8, 8))
        grid_x, grid_y = (np.linspace(0, 8, 64),
                          np.linspace(0, 8, 64))
        f = interpolate.interp2d(xx, yy, ir_arr_8, kind='cubic')
        return f(grid_x, grid_y).ravel()
