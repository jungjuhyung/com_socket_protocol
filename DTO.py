from dataclasses import dataclass, field
from threading import Thread
from socket import socket


@dataclass
class InfoSensor:
    clientID: str = field(default_factory=str)
    client_ip: str = field(default_factory=str)
    thread: Thread = field(default=None)
    socket: socket = field(default=None)
    statement: bool = field(default_factory=bool)


@dataclass
class SourceData:
    req_idx: int = field(default_factory=int)
    res_idx: int = field(default_factory=int)
    clientID: str = field(default_factory=str)
    response_time: float = field(default_factory=float)
    IR_ARR_8: list = field(default_factory=list)
    IR_ARR_64: list = field(default_factory=list)
    Distance_8: list = field(default_factory=list)
    Temperature: float = field(default_factory=float)
    Moisture: int = field(default_factory=int)
    Illuminance: float = field(default_factory=float)


@dataclass
class AssessmentData:
    situationResult: str = field(default_factory=str)
    req_idx: int = field(default_factory=int)
    res_idx: int = field(default_factory=int)
    result_time: float = field(default_factory=float)


@dataclass
class DecodingData:
    targetID: str = field(default_factory=str)
    requestID: str = field(default_factory=str)
    commend: int = field(default_factory=int)
    data: str = field(default_factory=str)
