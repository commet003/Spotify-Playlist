import spotipy
import requests
# from pprint import pprint
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import os


SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://127.0.0.1:9090",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

date_input = input("Pick a date you would like the top 100 songs for (Please use the format YYYY-MM-DD): ")
year = date_input.split("-")[0]


URL = f"https://www.billboard.com/charts/hot-100/{date_input}"
response = requests.get(URL)
URL_HTML = response.text
soup = BeautifulSoup(URL_HTML, 'html.parser')

songs_list = soup.find_all(name='span', class_='chart-element__information__song text--truncate color--primary')
songs_titles = [song.getText() for song in songs_list]
song_uris = []

for song in songs_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date_input} Billboard 100", public=False)
# print(playlist)

sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=song_uris)