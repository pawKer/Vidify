import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import json
import numpy as np
import urllib
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
            self.data = None

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
                data = json.dumps(sp.current_playback())
                data = json.loads(data)
            except Exception:
                raise CouldNotFetchPlaybackException(
                    'Something went wrong when' \
                    'fetching current playback.')

            if data != None:
                song_title = data['item']['name']
                # This can be updated to include all the artists of a song (currently just the main one)
                artist = data['item']['artists'][0]['name']
                data = {
                    "artist": artist,
                    "song_title": song_title
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
            raise CouldNotRefreshTokenException('Could not refresh token.')

    def connected_to_chromecast(self, name):
        """Checks if connected to a Chromecast.

        Args:
            name (str): Name of Chromecast

        Returns:
            bool: True if connected to a Chromecast, False otherwise.

        """
        return self.data and self.data['device']['name'] == name

    def new_song(self, old_song_id):
        """Checks if a new song is playing.

        Args:
            old_song_id (str): The song id given by the Spotify API.

        Returns:
            bool: True if new song, False otherwise.

        """
        if self.data:
            is_active = self.data['device']['is_active']
            current_song_id = self.get_current_song_id()
            return is_active and current_song_id != old_song_id
        else:
            return False

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
