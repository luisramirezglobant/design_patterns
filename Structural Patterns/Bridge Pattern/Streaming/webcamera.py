from data import BufferData
from streaming_device import StreamingDevice

class WebCamera(StreamingDevice):
    def get_buffer_data(self) -> BufferData:
        return "###Webcamera buffer data###"