from abc import ABCMeta, abstractmethod

class YoutubeClient():
    DEFAULT_VIDEO_ID = "GfKs8oNP9m8"
    
    @abstractmethod
    def get_youtube_link(self) -> None:
        """
        """