from abc import ABCMeta, abstractmethod

class PlayerClient():
    @abstractmethod
    def current_playback(self) -> str:
        """
        """
    @abstractmethod
    def update_current_playback(self) -> None:
        """
        """