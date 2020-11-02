import re
class Utils():
    def clean_song_title(song_title):
        cleaned_song_title = song_title.split('(', 1)[0].split('-', 1)[0].rstrip().lower()
        cleaned_song_title = re.sub('(?i)^!(?:(?![×Þß÷þø])[-0-9a-zÀ-ÿ ])+$', '', cleaned_song_title)
        return cleaned_song_title
    def clean_artist_name(artist_name):
        cleaned_artist_name = artist_name.replace('[', "").replace(']', "").replace(',', "").lower()
        return cleaned_artist_name