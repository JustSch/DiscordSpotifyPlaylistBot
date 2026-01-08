import os
import logging
from dotenv import load_dotenv
load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyOAuth
logger = logging.getLogger('spotify playlist bot')

class SearchAndAdd:

    def search_spotify_for_match(self, yt_music_info):
        results = self.sp.search(q='track:'+yt_music_info[0]+' artist:'+yt_music_info[1],type='track')
        spotify_music_info=[]
        if len(results['tracks']['items']) == 0:
            logger.info('the song could not be found on spotify. Skipping.....')
            return ''
        elif len(results['tracks']['items']) > 0:

            logger.info('song match found')
            
            for track in results['tracks']['items']:
                if track['artists'][0]['name'] == yt_music_info[1] and track['name'] == yt_music_info[0]:
                    spotify_music_info = [
                        track['artists'][0]['name'],
                        track['name'],
                        track['album']['name'],
                        track['external_urls']['spotify'],
                        track['uri']
                    ]
                    break
                
            if not spotify_music_info: 
                logger.info('results were found but none of them matched the music info from the video')
                return ''
            
            logger.info('artist: '+spotify_music_info[0])
            logger.info('title: '+spotify_music_info[1])
            logger.info('album: '+spotify_music_info[2])
            logger.info('spotify url: '+spotify_music_info[3])
            logger.info('spotify uri: '+spotify_music_info[4])

            return spotify_music_info[4]

    def check_if_track_in_playlist(self, spotify_track_uri):
        results = self.sp.playlist_items(self.playlist_id)
        for item in results['items']: 
            if [item['track']['uri']] == spotify_track_uri:
                return True
        return False


    def add_to_playlist(self, spotify_track_uri):
        in_playlist = (self.check_if_track_in_playlist(spotify_track_uri))
        if in_playlist:
            logger.info('the track is already part of the playlist. Skipping.....')
        else:
            self.sp.playlist_add_items(self.playlist_id,spotify_track_uri)
            logger.info('the song has been added to playlist')

    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("spotify_client_id"),
                                                client_secret=os.getenv("spotify_client_secret"),
                                                redirect_uri=os.getenv("spotify_redirect_uri"),
                                                scope="playlist-modify-public, playlist-modify-private",
                                                open_browser=False))
        self.playlist_id = os.getenv('playlist_id')
        






        

    
