import os
from dotenv import load_dotenv
load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyOAuth

#make into class so this can be instatiated in instance
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("spotify_client_id"),
                                               client_secret=os.getenv("spotify_client_secret"),
                                               redirect_uri=os.getenv("redirect_uri"),
                                               scope="playlist-modify-public, playlist-modify-private"))

playlist_id = os.getenv('playlist_id')
yt_music_info = [' アイドル','Yoasobi']
spotify_track_uri = ''

def search_spotify_for_match(yt_music_info):
    results = sp.search(q='track:'+yt_music_info[0]+' artist:'+yt_music_info[1],type='track')
    spotify_music_info=[]

    if len(results) > 0:

        print('song match found')
        spotify_music_info = [
            results['tracks']['items'][0]['artists'][0]['name'],
            results['tracks']['items'][0]['name'],
            results['tracks']['items'][0]['album']['name'],
            results['tracks']['items'][0]['external_urls']['spotify'],
            results['tracks']['items'][0]['uri']
        ]
        
        print('artist: '+spotify_music_info[0])
        print('title: '+spotify_music_info[1])
        print('album: '+spotify_music_info[2])
        print('spotify url: '+spotify_music_info[3])
        print('spotify uri: '+spotify_music_info[4])

        return spotify_music_info[4]

def check_if_track_in_playlist(spotify_track_uri):
    results = sp.playlist_items(playlist_id)
    for item in results['items']:        
        if item['track']['uri'] == spotify_track_uri:
            return True
    return False



spotify_track_uri = search_spotify_for_match(yt_music_info)


in_playlist = (check_if_track_in_playlist(spotify_track_uri))


def add_to_playlist(spotify_track_uri):
    sp.playlist_add_items(playlist_id,spotify_track_uri)

if not in_playlist:
   add_to_playlist([spotify_track_uri])
   print('the song has been added to playlist')
        

    
