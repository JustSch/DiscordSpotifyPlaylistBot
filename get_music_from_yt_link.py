import yt_dlp
import os
import requests
from urllib.parse import urlsplit, parse_qs
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("url")# change to receive from message

YOUTUBE_OPERATIONAL_API_URL=os.getenv("YOUTUBE_OPERATIONAL_API_URL")

split_url = urlsplit(url)
video_id = ''
song_info = []

if split_url.netloc == 'youtu.be':
    video_id = split_url.path[1:]

if split_url.netloc == 'www.youtube.com':
    parsed_queries = parse_qs(split_url.query)
    video_id = parsed_queries['v'][0]



def get_music_from_api():
    song_info = []
    print('Attempting to get music info of video '+video_id+' with API')#change to log to file
    params = {'part':'musics', 'id': video_id}
    req = requests.get(YOUTUBE_OPERATIONAL_API_URL+'/videos',params)

    if req.status_code == 200:
        req_json = req.json()

        song_info_from_request = req_json['items'][0]['musics'][0] 

        song_info = [song_info_from_request['song'],song_info_from_request['artist'],song_info_from_request['album']]

    return song_info



def get_music_from_yt_dlp():
    song_info = []
    print('Attempting to get music info of video '+video_id+' with yt-dlp')
    ydl = yt_dlp.YoutubeDL({})
    with ydl:
        video = ydl.extract_info(url, download=False)
        if 'track' in video and 'artist' in video and 'album' in video:
            song_info = [video['track'],video['artist'],video['album']]
    return song_info

song_info = get_music_from_api()

if song_info == None or song_info == []:
    print('Could not get music info from API. Trying with yt-dlp')
    song_info = get_music_from_yt_dlp()

if song_info != []:
    print(song_info)#change to send message and tell of success

#else failed
