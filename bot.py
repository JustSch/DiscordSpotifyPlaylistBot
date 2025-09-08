from dotenv import load_dotenv
import os
import get_music_from_yt_link
import search_and_add_to_playlist
load_dotenv()

url = os.getenv("url")# change to receive from message
YOUTUBE_OPERATIONAL_API_URL=os.getenv("YOUTUBE_OPERATIONAL_API_URL")
spotify_search_and_adder = search_and_add_to_playlist.SearchAndAdd()

song_info = get_music_from_yt_link.find_music_info(url, YOUTUBE_OPERATIONAL_API_URL)

if song_info != []:
    spotify_track_uri = spotify_search_and_adder.search_spotify_for_match(song_info)
    spotify_search_and_adder.add_to_playlist([spotify_track_uri])
    
    #else failed

