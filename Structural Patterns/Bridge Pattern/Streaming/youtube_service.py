import logging

from data import generate_id
from streaming_service import StreamingService

class YoutubeStreamingService(StreamingService):
    def start_stream(self):
        stream_reference = generate_id()
        logging.info(f"Starting stream on Youtube with reference: {stream_reference}")
        return stream_reference

    def fill_buffer(self, reference):
        buffer_data = self.device.get_buffer_data()
        logging.info(f"Received buffer data {buffer_data}. Sending it to Youtube stream {reference}")

    def stop_stream(self, reference):
        logging.info(f"Stopping stream with reference {reference} on Youtube")