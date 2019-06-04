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
from flask import Flask, render_template
from flask import request

# Get youtube link from song title and artist
def get_youtube_link(song_title, artist):

    # For each row in the dataframe
    # Build the query from the data
    temp_query = ""
    youtube_view_counts = []
    youtube_video_titles = []
    cur_index=1


    # Build the query as song_title + artists (from the Spotify API)
    temp_query += song_title.replace(',', "") + " " + artist.replace('[', "").replace(']', "").replace(',', "")

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

    #print("QUERY ============================")

    max_viewcount = 0
    max_viewcount_title = ""
    max_viewcount_id = ""

    # Iterate through the first 5 results to find the relevant video with most views
    for item in j_results_query['items']:


        #print("Video title: ", item['snippet']['title'])

        # Video title of a video to match the query string
        video_title = item['snippet']['title']


        #print("Video id: ", item['id']['videoId'])

        # Get the video ID of a video to match the query string
        video_id = item['id']['videoId']

        # Next, using this video ID we need to get the view count of that video
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
            # Hope this makes sense :) 
            if int(view_count) > max_viewcount and song_title.split('(', 1)[0].split('-', 1)[0].rstrip().lower() in video_title.lower():
                max_viewcount = int(view_count)
                max_viewcount_title = video_title
                #max_viewcount_id = j_results_stats['items'][0]['id']
                max_viewcount_id = video_id

    print("CHOICE IS: ", max_viewcount_title, " ---- ", max_viewcount, " ---- ", max_viewcount_id)

    temp_query = ""
    return max_viewcount_id
    


app = Flask(__name__)

# Spotify auth
username = "217unxkx4en4irnq4nkvgax6y"
scope = "user-read-currently-playing"
redirect_uri = "http://localhost:8888/callback/"
token = util.prompt_for_user_token(username, scope, config.client_id, config.client_secret, redirect_uri)
sp = spotipy.Spotify(auth=token)
sp.trace=False

# Get current playing song from Spotify and initialize track
track = sp.current_user_playing_track()
if track != None:
	song_title = track['item']['name']
	artist = track['item']['artists'][0]['name']
	currentId = get_youtube_link(song_title, artist)

@app.route('/')
def index():
	# Main page
	return render_template('index.html')

@app.route('/api/')
def api_get_name():
	# Endpoint for front end to get current track that will be called from UI client
	track = sp.current_user_playing_track()
	if track == None:
		return ""
	else:
		song_title = track['item']['name']
		artist = track['item']['artists'][0]['name']
		currentId = get_youtube_link(song_title, artist)
		return currentId

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')