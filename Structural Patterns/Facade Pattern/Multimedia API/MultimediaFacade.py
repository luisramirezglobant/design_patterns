class AudioPlayer:
    def load_audio(self, filename):
        print(f"Loading audio file: {filename}")
        # Simulate loading audio data from file

    def play_audio(self):
        print("Playing audio")
        # Simulate playing audio

    def stop_audio(self):
        print("Stopping audio")
        # Simulate stopping audio playback

class VideoPlayer:
    def load_video(self, filename):
        print(f"Loading video file: {filename}")
        # Simulate loading video data from file

    def play_video(self):
        print("Playing video")
        # Simulate playing video

    def stop_video(self):
        print("Stopping video")
        # Simulate stopping video playback

class ImageLoader:
    def load_image(self, filename):
        print(f"Loading image file: {filename}")
        # Simulate loading image data from file

    def display_image(self):
        print("Displaying image")
        # Simulate displaying image

class MultimediaFacade:
    def __init__(self):
        self.audio_player = AudioPlayer()
        self.video_player = VideoPlayer()
        self.image_loader = ImageLoader()

    def play_media(self, filename, media_type):
        if media_type == 'audio':
            self.audio_player.load_audio(filename)
            self.audio_player.play_audio()
        elif media_type == 'video':
            self.video_player.load_video(filename)
            self.video_player.play_video()
        elif media_type == 'image':
            self.image_loader.load_image(filename)
            self.image_loader.display_image()

    def stop_media(self, media_type):
        if media_type == 'audio':
            self.audio_player.stop_audio()
        elif media_type == 'video':
            self.video_player.stop_video()

# Usage
multimedia_player = MultimediaFacade()
multimedia_player.play_media("song.mp3", "audio")
multimedia_player.play_media("movie.mp4", "video")
multimedia_player.play_media("picture.jpg", "image")
multimedia_player.stop_media("audio")