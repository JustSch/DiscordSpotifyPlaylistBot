import yt_dlp
import os
import requests
import logging
from urllib.parse import urlsplit, parse_qs
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger('spotify playlist bot')


def get_music_from_api(video_id, youtube_operation_api_url):
    song_info = []
    logger.info('Attempting to get music info of video '+video_id+' with API')#change to log to file
    params = {'part':'musics', 'id': video_id}
    req = requests.get(youtube_operation_api_url+'/videos',params)

    if req.status_code == 200:
        req_json = req.json()

        if (req_json['items'][0]['musics']!= []):
            song_info_from_request = req_json['items'][0]['musics'][0] 

            if 'album' in song_info_from_request:
                song_info = [song_info_from_request['song'],song_info_from_request['artist'],song_info_from_request['album']]
            else:
                song_info = [song_info_from_request['song'],song_info_from_request['artist'],'']

    return song_info



def get_music_from_yt_dlp(url,video_id):
    song_info = []
    logger.info('Attempting to get music info of video '+video_id+' with yt-dlp')
    ydl = yt_dlp.YoutubeDL({})
    with ydl:
        video = ydl.extract_info(url, download=False)
        if 'track' in video and 'artist' in video and 'album' in video:
            song_info = [video['track'],video['artist'],video['album']]
    return song_info

def find_music_info(url,youtube_operation_api_url):
    split_url = urlsplit(url)
    video_id = ''
    song_info = []

    if split_url.netloc == 'youtu.be':
        video_id = split_url.path[1:]

    if split_url.netloc == 'www.youtube.com':
        parsed_queries = parse_qs(split_url.query)
        video_id = parsed_queries['v'][0]
    song_info = get_music_from_api(video_id,youtube_operation_api_url)

    if song_info == None or song_info == []:
        logger.info('Could not get music info from API. Trying with yt-dlp')
        song_info = get_music_from_yt_dlp(url, video_id)
        
        if song_info == []:
            logger.info('Could not get music info from yt-dlp. Video might not contain music info')

    if song_info != None and song_info != []:
        logger.info('music info found')

    return song_info


