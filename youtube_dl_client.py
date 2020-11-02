import youtube_dl
import logging
from youtube_client import YoutubeClient
log = logging.getLogger('flask_web_server.service')
class YoutubeDlClient(YoutubeClient):

    def get_youtube_link(self, song_title, artist):
        with youtube_dl.YoutubeDL() as ytdl:
            try:
                log.info(song_title)
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
                    return self.DEFAULT_VIDEO_ID
                else:
                    return data['entries'][0]['id']