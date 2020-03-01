import config
from youtube_api_client import YoutubeApiClient
from current_spotify_playback import CurrentSpotifyPlayback
from flask import Flask, render_template
from flask import request

app = Flask(__name__)

redirect_uri="http://localhost:8888/callback/"

spotifyClient = CurrentSpotifyPlayback(config.client_id, config.client_secret, redirect_uri, config.refresh_token)
youtubeClient = YoutubeApiClient(config.youtube_client_secret)

# Get current playing song from Spotify and initialize track
track = spotifyClient.current_playback()
if track != None:
	song_title = track['item']['name']
	# This can be updated to include all the artists of a song (currently just the main one)
	artist = track['item']['artists'][0]['name']
	currentId = youtubeClient.get_youtube_link(song_title, artist)

previousId = ""
previousTitle = ""
@app.route('/api/')
def api_get_name():
    global previousTitle
    global previousId
    global spotifyClient
    global youtubeClient
    # Endpoint for front end to get current track that will be called from UI client
    spotifyClient.update_current_playback()
    track = spotifyClient.current_playback()
    if track == None:
        return "GfKs8oNP9m8"
    else:
        song_title = track['item']['name']
        artist = track['item']['artists'][0]['name']

        # This reduces the number of youtube api calls if the song hasn't changed on spotify
        if song_title == previousTitle:
            return previousId
        else:
            currentId = youtubeClient.get_youtube_link(song_title, artist)
            previousId = currentId
            previousTitle = song_title
            return currentId

@app.route('/')
def index():
	# Main page
	return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')