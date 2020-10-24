from SwSpotify import spotify, SpotifyNotRunning
from player_client import PlayerClient
import logging
class CurrentSpotifyAppPlayback(PlayerClient):
    previousData = None
    def __init__(self):
        self.data = self.current_playback()

    def update_current_playback(self):
        self.previousData = self.data
        self.data = self.current_playback()

    def current_playback(self):
        data = None
        try:
            title, artist = spotify.current()
            data = {
                "artist": artist,
                "song_title": title
            }
        except SpotifyNotRunning as e:
            logging.warn("Spotify is not running - open the Spotify app and start playing a song")
        return data