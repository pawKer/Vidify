# Spotify Youtube Match

This is a repo for a quick tool I implemented that looks at your current playing song on Spotify and plays the corresponding Youtube video in a webpage running on localhost.

I use the spotipy library for the Spotify API to get the current playing song on Spotify and then look for the corresponding Youtube video for that song using the Youtube API. An endpoint that retrieves the video id in Flask is checked continously from the front-end in Javascript and the video is autoplayed in a video frame in HTML. 
When the song is changed on Spotify, the video will automatically change on the webpage.

The song on Spotify and the video aren't synced since sometimes videos are longer than the songs and there is also a short delay in the matching process.

I don't know what the use for this can be. I use it for background videos while I play music on Spotify.

# Requirements
The spotipy library needs to be updated by hand since apparently the pip install is outdated.
You can do that like so:
`pip install git+https://github.com/plamere/spotipy.git --upgrade`

# Running the tool
First you would need to use your own Spotify and Youtube API keys. After doing that, make sure you have all the python dependecies installed. Then, you can just run the server by doing `python server.py` and then visit `localhost:5000`. The webpage with the video should be there and you should now be able to play any song on Spotify and get the corresponding video to play.

# Raspberry Pi Version
I wanted to have this script run on a Pi all the time and play the videos on a monitor but unfortunately it is not very good at playing Youtube videos directly from the website so I had to adapt the script. Instead of running it as a web server, I made a script that uses OMXPlayer and youtube-dl.

It uses youtube-dl to get the youtube video download link and then passes that link to OMXPlayer. The rest of the functionality is the same as above.
