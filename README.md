# Spotify Youtube Match

This is a repo for a quick tool I implemented that looks at your current playing song on Spotify and plays the corresponding Youtube video in a webpage running on localhost.

I use the spotipy library for the Spotify API to get the current playing song on Spotify and then look for the corresponding Youtube video for that song using the Youtube API. An endpoint that retrieves the video id in Flask is checked continously from the front-end in Javascript and the video is autoplayed in a video frame in HTML. 
When the song is changed on Spotify, the video will automatically change on the webpage.

The song on Spotify and the video aren't synced since sometimes videos are longer than the songs and there is also a short delay in the matching process.

I don't know what the use for this can be. I use it for background videos while I play music on Spotify.

# Requirements
To download all of the pyhton libraries required run the following command

`pip install -r requirements.txt`

The spotipy library needs to be updated by hand since apparently the pip install is outdated.

You can do that like so:

`pip install git+https://github.com/plamere/spotipy.git --upgrade`

# Configuration
To run the app you will need to use your own API keys for Spotify and Youtube. You can find documentation on how to get these on Google.
After you have them, create a file `config.py` with the following content

```
client_id="<YOUR-SPOTIFY-CLIENT-ID>"
client_secret="<YOUR-SPOTIFY-CLIENT-SECRET>"
youtube_client_secret="<YOUR-YOUTUBE-CLIENT-SECRET>"
redirect_uri="http://localhost:8888/callback/"
refresh_token="<YOUR-SPOTIFY-REFRESH-TOKEN>"
```
# Refresh token
The Spotify API will not allow access after 1h of continous access so we need to refresh our authorisation. For that we need a refresh token. To obtain that you can use the `python get_refresh_token.py <YOUR-SPOTIFY-USERNAME>` utility script. This will open a window in your browser and you will have to allow access to Spotify. You will then be redirected to an URL which you need to copy and paste back into the script. Your refresh token will then be printed. Grab that and place it in the `config.py` file you created above.

# Running the app
You can run the server by doing `python server.py` and then visit `localhost:5000`. The webpage with the video should be there and you should now be able to play any song on Spotify and get the corresponding video to play.

# Raspberry Pi Version
I wanted to have this script run on a Pi all the time and play the videos on a monitor but unfortunately it is not very good at playing Youtube videos directly from the website so I had to adapt the script. Instead of running it as a web server, I made a script that uses OMXPlayer and youtube-dl.

It uses youtube-dl to get the youtube video download link and then passes that link to OMXPlayer. The rest of the functionality is the same as above.
