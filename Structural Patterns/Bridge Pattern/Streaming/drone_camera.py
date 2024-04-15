from data import BufferData
from streaming_device import StreamingDevice

class DroneCamera(StreamingDevice):
    def get_buffer_data(self) -> BufferData:
        return "###DSLR Camera Buffer Data###"