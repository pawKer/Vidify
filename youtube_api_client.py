import json
import config
import requests
import urllib
import re

class YoutubeApiClient():

    def __init__(self, apiKey):
        self.key = apiKey

    def get_youtube_link(self, song_title, artist):
        temp_query = ""
    
        # Build the query as song_title + artists (from the Spotify API)
        temp_query += re.sub('[^0-9a-zA-Z ]+', '', song_title).lower() + " " + artist.replace('[', "").replace(']', "").replace(',', "").lower()

        params_for_query = {"part": "snippet",
                            "maxResults": 5,
                            "order": "relevance",
                            "pageToken": "",
                            "q": temp_query,
                            "key": self.key,
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
                                    "key": self.key,
                                }
                url2 = "https://www.googleapis.com/youtube/v3/videos"
                page_stats = requests.request(method="get", url=url2, params=params_for_stats)
                j_results_stats = json.loads(page_stats.text)

                # Check if problem with retrieving statistics
                if 'items' in j_results_stats:
                    # Get the view count
                    view_count  = j_results_stats['items'][0]['statistics']['viewCount']

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
            return "GfKs8oNP9m8"