from abc import ABCMeta, abstractmethod

class PlayerClient():
    @abstractmethod
    def get_current_song(self) -> None:
        """
        """