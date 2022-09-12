import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

USER_NAME = "usr"
CLIENT_ID = "id" # spotify id
CLINENT_SECRET ="password" # spotify password

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLINENT_SECRET,
        show_dialog=True,
        cache_path="token.txt" ## token file that you will need from spotify.
    )
)
user_id = sp.current_user()["id"]   ## to get current user id

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:") # ask user which times music playlist he wants to create
URL = f"https://www.billboard.com/charts/hot-100/{date}"  # url of songs names in that time

name_of_playlist = f"{date} Bilboard 100" #name of playlist
response = requests.get(URL) # to get response from url
website_html = response.text # website in html format

soup = BeautifulSoup(website_html, "html.parser") # to make website soup object

all_songs = soup.find_all(name="span", class_ ="chart-element__information__song") # song  tags names from web site
song_names = [song.getText() for song in all_songs] # all of the song names with list comprhension from songs tags names
song_uris = []

year = date.split("-")[0]  ## just to take year of the date and search it in spotify
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")  ## search for song name in song names with name, time
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"] ## url is in this path
        song_uris.append(uri) # append url on uri list
    except IndexError: # expect index error because the song might not be in spotify
        print(f"{song} doesn't exist in Spotify. Skipped.") #print out that info if it isn't in spotify


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)  # create playlist

sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=song_uris) # append the songs on playlist