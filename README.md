# spotify_youtube_match

This is a repo for a quick tool I implemented that looks at your current playing song on Spotify and plays the corresponding Youtube video in a webpage running on localhost.

I use the spotipy library for the Spotify API to get the current playing song on Spotify and then look for the corresponding Youtube video for that song using the Youtube API. An endpoint that retrieves the video id in Flask is checked continously from the front-end in Javascript and the video is autoplayed in a video frame in HTML. 
When the song is changed on Spotify, the video will automatically change on the webpage.

The song on Spotify and the video aren't synced since sometimes videos are longer than the songs and there is also a short delay in the matching process.

I don't know what the use for this can be. I use it for background videos while I play music on Spotify.
