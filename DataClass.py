from dataclasses import dataclass, field
from threading import Thread
from socket import socket
import numpy as np


@dataclass
class InfoSensor:
    clientID: str = field(default_factory=str)
    client_ip: str = field(default_factory=str)
    thread: Thread = None
    socket: socket = None
    statement: bool = field(default_factory=bool)


@dataclass
class SourceData:
    res_idx: int = field(default_factory=int)
    clientID: str = field(default_factory=str)
    response_time: float = field(default_factory=float)
    IR_ARR_8: np.ndarray = field(default_factory=lambda: np.array([]))
    IR_ARR_64: np.ndarray = field(default_factory=lambda: np.array([]))
    Distance_8: np.ndarray = field(default_factory=lambda: np.array([]))
    Temperature: float = field(default_factory=float)
    Moisture: int = field(default_factory=int)
    Illuminance: int = field(default_factory=int)


@dataclass
class AssessmentData:
    situationResult: str = field(default_factory=str)
    res_idx: int = field(default_factory=int)
    result_time: float = field(default_factory=float)


@dataclass
class DecodingData:
    targetID: str = field(default_factory=str)
    requestID: str = field(default_factory=str)
    commend: str = field(default_factory=str)
    data: str = field(default_factory=str)

@dataclass
class CodeData:
    dataCmd: str = "01"
    changeCmd: str = "02"
    keepCmd: str = "09"
    greenData : str = "00"
    redData : str = "01"
