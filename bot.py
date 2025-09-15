from dotenv import load_dotenv
import os
import get_music_from_yt_link
import search_and_add_to_playlist
import nest_asyncio
import discord
from urllib.parse import urlsplit, urlunsplit

nest_asyncio.apply()
load_dotenv()

url = os.getenv("url")
YOUTUBE_OPERATIONAL_API_URL=os.getenv("YOUTUBE_OPERATIONAL_API_URL")

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

spotify_search_and_adder = search_and_add_to_playlist.SearchAndAdd()


@client.event
async def on_ready():
    print('Spotify PlayList Bot is now running')

def extract_urls(text):
    urls = []
    split_text = text.split()
    for t in split_text:
        parsed = urlsplit(t)
        if parsed.scheme and parsed.netloc:
            urls.append(t)
    return urls

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    urls_in_message = extract_urls(message.content)

    for url in urls_in_message:
        netloc = urlsplit(url).netloc 
        if netloc == 'youtu.be' or netloc== 'www.youtube.com':
            song_info = get_music_from_yt_link.find_music_info(url, YOUTUBE_OPERATIONAL_API_URL)
       
            if song_info != []:
                song_list = []
                if ',' in song_info[1]:
                    song_list.append([song_info[0],artist,song_info[1]])
                    artists = song_info[1].split(',')
                    for artist in artists:
                        song_list.append([song_info[0],artist,song_info[1]])
                else:
                    song_list = [song_info]


                for song in song_list:
                    spotify_track_uri = spotify_search_and_adder.search_spotify_for_match(song)
                    if spotify_track_uri != '':
                        spotify_search_and_adder.add_to_playlist([spotify_track_uri])
                        
        if netloc == 'open.spotify.com':
            path = urlsplit(url).path
            if '/track/' in path:
                print('Attemping to add Spotify Track with ID: '+path.split("/track/")[1])
                spotify_search_and_adder.add_to_playlist(['spotify:track:'+path.split("/track/")[1]])


client.run(TOKEN)