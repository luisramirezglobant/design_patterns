from dataclasses import dataclass
from abc import ABC

from streaming_device import StreamingDevice

@dataclass
class StreamingService(ABC):
    device: StreamingDevice

    def start_stream(self) -> str:
        ...
    
    def fill_buffer(self, reference: str) -> None:
        ...
    
    def stop_stream(self, reference: str) -> None:
        ...