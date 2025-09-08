from dotenv import load_dotenv
import os
import get_music_from_yt_link
load_dotenv()

url = os.getenv("url")# change to receive from message
YOUTUBE_OPERATIONAL_API_URL=os.getenv("YOUTUBE_OPERATIONAL_API_URL")

song_info = get_music_from_yt_link.find_music_info(url, YOUTUBE_OPERATIONAL_API_URL)

if song_info != []:
    print(song_info)

    #else failed

