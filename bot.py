from dotenv import load_dotenv
import os
import get_music_from_yt_link
import search_and_add_to_playlist
import nest_asyncio
import re
import discord
from urllib.parse import urlsplit

nest_asyncio.apply()
load_dotenv()

url = os.getenv("url")# change to receive from message
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
    # Extract URLs from text using regex to handle markdown and other formatting
    url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
    return re.findall(url_pattern, text)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Extract URLs using regex instead of splitting by spaces
    urls_in_message = extract_urls(message.content)

    for url in urls_in_message:
        netloc = urlsplit(url).netloc 
        if netloc == 'youtu.be' or netloc== 'www.youtube.com':
            song_info = get_music_from_yt_link.find_music_info(url, YOUTUBE_OPERATIONAL_API_URL)
            if song_info != []:
                spotify_track_uri = spotify_search_and_adder.search_spotify_for_match(song_info)
                spotify_search_and_adder.add_to_playlist([spotify_track_uri])
        if netloc == 'open.spotify.com':
            path = urlsplit(url).path
            if '/track/' in path:
                print(path.split("/track/")[1])
                spotify_search_and_adder.add_to_playlist(['spotify:track:'+path.split("/track/")[1]])


client.run(TOKEN)