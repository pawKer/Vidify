import config
from youtube_api_client import YoutubeApiClient
from current_spotify_api_playback import CurrentSpotifyApiPlayback
from current_spotify_app_playback import CurrentSpotifyAppPlayback
from flask import Flask, render_template
from flask import request
import sys
import os
import logging

# Logic for exposing the templates and static folders to PyInstaller
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask("flask_web_server", template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask("flask_web_server")

app.logger.setLevel(logging.INFO)
redirect_uri="http://localhost:8888/callback/"

spotifyClient = None
if len(sys.argv) == 2:
    if sys.argv[1] == "api":
        app.logger.info("Using Spotify API - config needs to be populated with API key")
        spotifyClient = CurrentSpotifyApiPlayback(config.client_id, config.client_secret, redirect_uri, config.refresh_token)
    elif sys.argv[1] == "app":
        app.logger.info("Using Spotify Desktop APP")
        spotifyClient = CurrentSpotifyAppPlayback()
    else:
        app.logger.info("Default: Using Spotify Desktop APP")
        spotifyClient = CurrentSpotifyAppPlayback()
else:
    app.logger.info("Default: Using Spotify Desktop APP")
    spotifyClient = CurrentSpotifyAppPlayback()

youtubeClient = YoutubeApiClient(config.youtube_client_secret)

previousId = ""
previousTitle = ""

# Endpoint for front end to get current track that will be called from UI client
@app.route('/api/')
def api_get_name():
    global previousTitle
    global previousId
    global spotifyClient
    global youtubeClient
    try:
        track = spotifyClient.get_current_song()
        if track == None:
            return youtubeClient.DEFAULT_VIDEO_ID
        else:
            # This reduces the number of youtube api calls if the song hasn't changed on spotify
            if track['song_title'] == previousTitle:
                return previousId
            else:
                currentId = youtubeClient.get_youtube_link(track['song_title'], track['artist'])
                previousId = currentId
                previousTitle = track['song_title']
                return currentId
    except Exception as e:
        app.logger.error("An error occured in the app: " + str(e))
    
    return youtubeClient.DEFAULT_VIDEO_ID

@app.route('/')
def index():
	# Main page
	return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', use_reloader=False)
