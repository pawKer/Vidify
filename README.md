# Vidify Web

### Automatically play the video for your currently playing song on Spotify in your browser

![](demo/vidify.gif)

## Running the app

## The plug-and-play way

Since the v1.0 release this is now very simple! You just have to download the executable file from [here](https://github.com/pawKer/Vidify/releases/tag/v1.0) if you're on Windows. On MacOS or Linux you will need to run it via python at the moment. You can find instructions for how to do that below.

## The customizable way

If you prefer, the app also supports using the Spotify and Youtube APIs instead of using the SwSpotify and youtube-dl libraries. However, for these you have to provide your own API keys and run it using python. The advantage of doing this is you get better Youtube video matches and you don't have to have the Spotify app open on the computer where you are running the app.

## Installing the Python version

### Requirements

To download all of the python libraries required run the following command. This project requires Python 3.x.

`pip install -r requirements.txt`

The spotipy library needs to be updated by hand since apparently the pip install is outdated.

You can do that like so:

`pip install git+https://github.com/plamere/spotipy.git --upgrade`

### Configuration

Skip to `Running the app` if you're trying to just run the default app.
To run the app you will need to use your own API keys for Spotify and Youtube. You can find documentation on how to get these on Google.
After you have them, create a file `config.py` with the following content

```
client_id="<YOUR-SPOTIFY-CLIENT-ID>"
client_secret="<YOUR-SPOTIFY-CLIENT-SECRET>"
youtube_client_secret="<YOUR-YOUTUBE-CLIENT-SECRET>"
redirect_uri="http://localhost:8888/callback/"
refresh_token="<YOUR-SPOTIFY-REFRESH-TOKEN>"
```

### Refresh token

The Spotify API will not allow access after 1h of continous access so we need to refresh our authorisation. For that we need a refresh token. To obtain that you can use the `python get_refresh_token.py <YOUR-SPOTIFY-USERNAME>` utility script. This will open a window in your browser and you will have to allow access to Spotify. You will then be redirected to an URL which you need to copy and paste back into the script. Your refresh token will then be printed. Grab that and place it in the `config.py` file you created above.

### Running the app

You can run the server by doing `python gui_main.py`. This will start the GUI and a new tab will be opened in your default browser. The main page should be there and you should now be able to play any song on Spotify and get the corresponding video to play.

You can select what services you want to use by passing the following command line arguments `python server.py <SPOTIFY-SERVICE> <YOUTUBE-SERVICE>`.
The possible values are SPOTIFY-SERVICE: `api` or `app` and YOUTUBE-SERVICE: `yt-api` or `yt-dl`. The defaults are `app` and `yt-dl` because these don't require API credentials.

# Raspberry Pi Version (not up-to-date)

I wanted to have this script run on a Pi all the time and play the videos on a monitor but unfortunately it is not very good at playing Youtube videos directly from the website so I had to adapt the script. Instead of running it as a web server, I made a script that uses OMXPlayer and youtube-dl.

It uses youtube-dl to get the youtube video download link and then passes that link to OMXPlayer. The rest of the functionality is the same as above.

# How it works

I use the spotipy library for the Spotify API to get the current playing song on Spotify and then look for the corresponding Youtube video for that song using the Youtube API. An endpoint that retrieves the video id in Flask is checked continously from the front-end in Javascript and the video is autoplayed in a video frame in HTML.
When the song is changed on Spotify, the video will automatically change on the webpage.
The newer version does the same thing but without using the APIs and instead making use of the SwSpotify library which reads the current playing status from the Spotify app running on your computer and the youtube-dl library which finds the youtube url for your search.

The song on Spotify and the video aren't synced since sometimes videos are longer than the songs and there is also a short delay in the matching process.

# Package command

`pyinstaller -w -F --add-data "templates;templates" --add-data "static;static" gui_main.py`
