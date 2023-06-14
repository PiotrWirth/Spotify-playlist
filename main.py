import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URL = os.environ.get("REDIRECT_URL")

year = input("Which year do you want to travel to? Type the date in this format YYYY:")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{year}-06-24/")

web_page = response.text

soup = BeautifulSoup(web_page,'html.parser')

data = soup.select(selector=".o-chart-results-list__item > h3")

titles=[title.getText().strip() for title in data]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

titles_urls = []

for song in titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        titles_urls.append(result['tracks']['items'][0]['uri'])
    except IndexError:
        pass

playlist = sp.user_playlist_create(user=user_id,name=f"100 top songs from {year}",public=False)
sp.playlist_add_items(playlist_id=playlist['id'],items=titles_urls)
