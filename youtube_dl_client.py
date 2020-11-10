import youtube_dl
import logging
from youtube_client import YoutubeClient
log = logging.getLogger('flask_web_server.service')
class YoutubeDlClient(YoutubeClient):

    def get_youtube_link(self, song_title, artist):
        youtube_id = None
        tries = 0
        while youtube_id == None and tries < 3:
            with youtube_dl.YoutubeDL() as ytdl:
                try:
                    log.info("Attempt number " + str(tries + 1))
                    data = ytdl.extract_info("ytsearch:" + song_title + " " + artist, download=False)
                except Exception as e:
                    # Any kind of error has to be caught, so that it doesn't only
                    # send the error signal when the download wasn't successful
                    # (a DownloadError from youtube_dl).
                    log.warning("YouTube-dl wasn't able to obtain the video: %s",
                                str(e))
                else:
                    if len(data['entries']) == 0:
                        log.warning("YouTube-dl returned no entries")
                    else:
                        youtube_id = data['entries'][0]['id']
                        break
            tries = tries + 1
        if youtube_id == None:
            log.warning("Could not find youtube video after  " + str(tries) + " attempts. Using default.")
            return self.DEFAULT_VIDEO_ID
        else:
            return youtube_id