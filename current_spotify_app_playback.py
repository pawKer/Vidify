from SwSpotify import spotify, SpotifyNotRunning
from player_client import PlayerClient
import logging
log = logging.getLogger('flask_web_server.service')
class CurrentSpotifyAppPlayback(PlayerClient):
    data = None

    def __init__(self):
        self.data = self.get_current_song()

    def get_current_song(self):
        newData = None
        try:
            title, artist = spotify.current()
            newData = {
                "artist": artist,
                "song_title": title
            }
            self.data = newData
        except SpotifyNotRunning as e:
            log.warning("Spotify is not running - open the Spotify app and start playing a song")

        return self.data