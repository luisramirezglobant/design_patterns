import logging

from webcamera import WebCamera
from youtube_service import YoutubeStreamingService
from drone_camera import DroneCamera
from twitch_service import TwitchStreamingService

def main():
    logging.basicConfig(level=logging.INFO)

    # Create a device and a streaming service
    device = WebCamera()
    service = YoutubeStreamingService(device)

    # Start streaming
    reference = service.start_stream()
    service.fill_buffer(reference)
    service.stop_stream(reference)

    # Create another device and streaming service
    device2 = DroneCamera()
    service2 = TwitchStreamingService(device2)

    # Start streaming as well
    reference2 = service2.start_stream()
    service2.fill_buffer(reference2)
    service2.stop_stream(reference2)


if __name__ == "__main__":
    main()

