from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys
import csv
import pandas as pd
import numpy as np
import math
import seaborn as sns
import config
import spotipy.util as util
import requests
import urllib
import webbrowser
import re
from flask import Flask, render_template
from flask import request

# Get youtube link from song title and artist
def get_youtube_link(song_title, artist):
    temp_query = ""
   
    # Build the query as song_title + artists (from the Spotify API)
    temp_query += re.sub('[^0-9a-zA-Z ]+', '', song_title).lower() + " " + artist.replace('[', "").replace(']', "").replace(',', "").lower()

    params_for_query = {"part": "snippet",
                        "maxResults": 5,
                        "order": "relevance",
                        "pageToken": "",
                        "q": temp_query,
                        "key": config.youtube_client_secret,
                        "type": "video",
                        }
    url1 = "https://www.googleapis.com/youtube/v3/search"

    # Get top 5 video results ordered by relevance
    # TODO: Still some matching problems - how to get the most relevant video with the most views from official sources?
    page_query = requests.request(method="get", url=url1, params=params_for_query)
    j_results_query = json.loads(page_query.text)

    max_viewcount = 0
    max_viewcount_title = ""
    max_viewcount_id = ""
    better_pick = ""

    if 'items' in j_results_query:
	    # Iterate through the first 5 results to find the relevant video with most views
	    for item in j_results_query['items']:

	        # Video title of a video to match the query string
	        video_title = item['snippet']['title']

	        # Get the video ID of a video to match the query string
	        video_id = item['id']['videoId']

	        # Next, using this video ID we need to get the view count of that video from the API
	        params_for_stats = {"part": "statistics",
	                            "id": video_id,
	                            "key": config.youtube_client_secret,
	                           }
	        url2 = "https://www.googleapis.com/youtube/v3/videos"
	        page_stats = requests.request(method="get", url=url2, params=params_for_stats)
	        j_results_stats = json.loads(page_stats.text)

	        # Check if problem with retrieving statistics
	        if 'items' in j_results_stats:
	            # Get the view count
	            view_count  = j_results_stats['items'][0]['statistics']['viewCount']

	            # This is my hacky matching condition
	            # The video we want to match to our spotify song has to be the version of the song with the most views
	            # BUT we also need to make sure that it is the same song
	            # The .split() gets rid of some useless parts in a song title from spotify such as this
	            # e.g. Spotify title = "Eastside (feat. Elton John)" - > "Eastside"
	            # e.g. If we want the matching song for "Ariana Grande - thank u, next" and the results from the YT API are 
	            #           1. "Ariana Grande - thank u, next (1 million views)"
	            #           2. "Ariana Grande - breathin (5 million views)"
	            # We would be tempted to just take the one with more views but in fact we need to double check so we only update the max
	            # if the string "thank u, next" is also in the youtube video title
	            # I also remove all non-alphanumeric characters from the song title
	            # Hope this makes sense :) 
	            
	            # Get the video with the highest viewcount that also matches the spotify song
	            # If song title is not in youtube video title then we just rely on the number
	            # of views
	            cleaned_song_title = re.sub('[^0-9a-zA-Z ]+', '', song_title.split('(', 1)[0].split('-', 1)[0].rstrip().lower())
	            if int(view_count) > max_viewcount:
	                max_viewcount = int(view_count)
	                max_viewcount_title = video_title
	                max_viewcount_id = video_id
	                if cleaned_song_title in video_title.lower():
	                	better_pick = video_id

	    print("CHOICE IS: ", max_viewcount_title, " ---- ", max_viewcount, " ---- ", max_viewcount_id)
	    if better_pick == "":
	    	return max_viewcount_id
	    else:
	    	return better_pick
    else:
        return ""
    


app = Flask(__name__)

# Spotify auth
# This should be your spotify username
username = "217unxkx4en4irnq4nkvgax6y"

# We need authorized requests for reading the current playing song
scope = "user-read-currently-playing"

redirect_uri = "http://localhost:8888/callback/"
token = util.prompt_for_user_token(username, scope, config.client_id, config.client_secret, redirect_uri)
sp = spotipy.Spotify(auth=token)
sp.trace=False

# Get current playing song from Spotify and initialize track
track = sp.current_user_playing_track()
if track != None:
	song_title = track['item']['name']
	# This can be updated to include all the artists of a song (currently just the main one)
	artist = track['item']['artists'][0]['name']
	currentId = get_youtube_link(song_title, artist)

@app.route('/')
def index():
	# Main page
	return render_template('index.html')

previousId = ""
previousTitle = ""
@app.route('/api/')
def api_get_name():
	global previousTitle
	global previousId
	global sp
	global username
	global scope
	global redirect_uri
	# Endpoint for front end to get current track that will be called from UI client
	try:
		track = sp.current_user_playing_track()
	except:
		# This refreshes auth token which expires every hour - might be a dirty fix
		token = util.prompt_for_user_token(username, scope, config.client_id, config.client_secret, redirect_uri)
		sp = spotipy.Spotify(auth=token)
		track = sp.current_user_playing_track()
	if track == None:
		return ""
	else:
		song_title = track['item']['name']
		artist = track['item']['artists'][0]['name']

		# This reduces the number of youtube api calls if the song hasn't changed on spotify
		if song_title == previousTitle:
			return previousId
		else:
			currentId = get_youtube_link(song_title, artist)

			previousId = currentId
			previousTitle = song_title
			return currentId

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')