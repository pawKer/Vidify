import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import json
from player_client import PlayerClient
import logging
log = logging.getLogger('flask_web_server.service')
class CurrentSpotifyApiPlayback(PlayerClient):
    """Module for getting information about current Spotify playback.

    Attributes:
        auth (SpotifyOAuth): The SpotifyOAuth object to use.
        refresh_token (str): Refresh token given by Spotify.
        data (JSON): Current playback.

    """

    def __init__(self, client_id, client_secret, redirect_uri, refresh_token):
        """Initializes the class with the current playback.

        Args:
            client_id (str): Client id for your Spotify application
            redirect_uri (str): Redirect URI used by your Spotify
                application.
            refresh_token (str): Refresh token given by Spotify to
                update your credentials.

        """
        self.auth = oauth2.SpotifyOAuth(client_id,
                                        client_secret,
                                        redirect_uri)
        self.refresh_token = refresh_token
        self.data = self.current_playback()

    def update_current_playback(self):
        """Updates the current playback."""
        try:
            self.data = self.current_playback()
        except (CouldNotRefreshTokenException,
                CouldNotFetchPlaybackException):
            self.data = {
                    "artist": '',
                    "song_title": '',
                    "is_playing": 0
            }

    def current_playback(self):
        """Fetches the current playback.

        Returns:
            JSON: The current playback.

        Raises:
            CouldNotFetchPlaybackException: If it failed to load
                current playback.

        """
        token = self._refresh_token()
        if token:
            try:
                sp = spotipy.Spotify(auth=token)
                data = json.dumps(sp.current_user_playing_track())
                data = json.loads(data)
            except Exception:
                raise CouldNotFetchPlaybackException()
            
            if data != None:
                is_playing = 0

                if data['is_playing']:
                    is_playing = 1
                
                data = {
                    "artist": data['item']['artists'][0]['name'],
                    "song_title": data['item']['name'],
                    "is_playing": is_playing
                }
            else:
                data = {
                    "artist": '',
                    "song_title": '',
                    "is_playing": 0
                }
            return data

    def _refresh_token(self):
        """Refreshes the access token.

        Returns:
            str: The updated token.

        Raises:
            CouldNotRefreshTokenException: If it failed to refresh
                the credentials token.

        """
        try:
            return self.auth.refresh_access_token(self.refresh_token)\
                ['access_token']
        except Exception:
            raise CouldNotRefreshTokenException()

    def get_current_song(self):
        """Returns the current song id.

        Returns:
            str: Song id.

        Raises:
            NotPlayingAnywhereExcpetion: If Spotify is not active on
                any device.

        """
        self.update_current_playback()
        if self.data:
            return self.data
        else:
            raise NotPlayingAnywhereException()


class NotPlayingAnywhereException(Exception):
    """Raises when Spotify is not active on any device."""
    def __init__(self):
        self.message = "Spotify is not active on any device"
    pass


class CouldNotRefreshTokenException(Exception):
    """Raises when token could not be refreshed"""
    def __init__(self):
        self.message = "Spotify token could not be refreshed"
    pass


class CouldNotFetchPlaybackException(Exception):
    """Raises when current playback could not be fetched."""
    def __init__(self):
        self.message = "Spotify current playback could not be fetched."
    pass

class NoArtworkException(Exception):
    """Raises when the current playback has no artwork."""
    def __init__(self):
        self.message = "Spotify current playback has no artwork."
    pass
