import os
from dotenv import load_dotenv
load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SearchAndAdd:

    def search_spotify_for_match(self, yt_music_info):
        results = self.sp.search(q='track:'+yt_music_info[0]+' artist:'+yt_music_info[1],type='track')
        spotify_music_info=[]
        if len(results['tracks']['items']) == 0:
            print('the song could not be found on spotify. Skipping.....')
            return ''
        elif len(results['tracks']['items']) > 0:

            print('song match found')
            
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

            print('artist: '+spotify_music_info[0])
            print('title: '+spotify_music_info[1])
            print('album: '+spotify_music_info[2])
            print('spotify url: '+spotify_music_info[3])
            print('spotify uri: '+spotify_music_info[4])

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
            print('the track is already part of the playlist. Skipping.....')
        else:
            self.sp.playlist_add_items(self.playlist_id,spotify_track_uri)
            print('the song has been added to playlist')

    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("spotify_client_id"),
                                                client_secret=os.getenv("spotify_client_secret"),
                                                redirect_uri=os.getenv("spotify_redirect_uri"),
                                                scope="playlist-modify-public, playlist-modify-private"))
        self.playlist_id = os.getenv('playlist_id')
        






        

    
