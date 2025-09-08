import json 

with open('spotify_response_sample.info.json', encoding="utf8") as f:
    spotify_json = json.load(f)
    print(spotify_json['tracks']['items'][0]['artists'][0]['name'])
    print(spotify_json['tracks']['items'][0]['name'])
    print(spotify_json['tracks']['items'][0]['album']['name'])
    print(spotify_json['tracks']['items'][0]['external_urls']['spotify'])
    print(spotify_json['tracks']['items'][0]['uri'])