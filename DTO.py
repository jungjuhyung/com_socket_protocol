from dataclasses import dataclass
from threading import Thread
from socket import socket

@dataclass
class Info_Sensor :
    sensor_code : str
    sensor_ip : str
    thread : Thread
    socket : socket
    statement : bool

@dataclass
class Source_Data :
    req_idx : int
    res_idx : int
    sensor_code : str
    response_time : float
    IR_ARR_8 : list
    IR_ARR_64 : list
    Distance_8 : list
    Temperature : float
    Moisture : int
    Illuminance : float

@dataclass
class Assessment_Data :
    situationResult : str
    req_idx : int
    res_idx : int
    result_time : float
