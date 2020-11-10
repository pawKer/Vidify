from SwSpotify import spotify, SpotifyClosed, SpotifyPaused
from player_client import PlayerClient
import logging
log = logging.getLogger('flask_web_server.service')
class CurrentSpotifyAppPlayback(PlayerClient):
    data = None
    def __init__(self):
        self.data = {
                "artist": '',
                "song_title": '',
                "is_playing": 0
            }

    def get_current_song(self):
        try:
            title, artist = spotify.current()
            log.info("Playing on Spotify: {artist} - {title}".format(artist=artist, title=title))
            self.data = {
                "artist": artist,
                "song_title": title,
                "is_playing": 1
            }
        except SpotifyPaused:
            self.data['is_playing'] = 0
            log.info("Spotify is paused")
        except SpotifyClosed:
            log.warning("Spotify is not running - open the Spotify app and start playing a song")
        return self.data