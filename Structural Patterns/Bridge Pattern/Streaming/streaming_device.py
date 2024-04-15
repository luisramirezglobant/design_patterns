from typing import Protocol
from abc import ABC

from data import BufferData

class StreamingDevice(ABC):
    def get_buffer_data(self) -> BufferData:
        ...