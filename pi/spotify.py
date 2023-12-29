import requests
from auth import Auth

class PlaybackState:
  def __init__(self, song_name, artist_name, album_name):
    self.song_name = song_name
    self.artist_name = artist_name
    self.album_name = album_name

  def __str__(self):
    return f"{self.song_name}\n{self.artist_name} - {self.album_name}"

class Spotify:
  def __init__(self, token, client_id, client_secret):
    self.client_id = client_id
    self.client_secret = client_secret
    self.token = Auth(client_id, client_secret).token
    

  def refresh_token(self):
    req = requests.post(
      "https://accounts.spotify.com/api/token",
      headers = {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      data = {
        "grant_type": "client_credentials",
        "client_id": self.client_id,
        "client_secret": self.client_secret
      }
    )
    return req.json().get("access_token")
  
  def get_player(self):
    req = requests.get(
      "https://api.spotify.com/v1/me/player",
      headers={
          "Authorization": f"Bearer {self.token}"
      }
    )
    return req.json()

  def get_playback_info(self):
    player = self.get_player()

    return PlaybackState(player["item"]["name"], player["item"]["artists"][0]["name"], player["item"]["album"]["name"])
