import requests
from auth import Auth

class PlaybackState:
	def __init__(self, song_name, artist_name, album_name):
		self.song_name = song_name
		self.artist_name = artist_name
		self.album_name = album_name

	def __str__(self):
		return f"{self.song_name}\n{self.artist_name} - {self.album_name}"
	
	def to_display(self, frame=0, line_length=16):
		display = ""
		line_1 = self.song_name.ljust(line_length)
		line_2 = f"{self.artist_name}: {self.album_name}".ljust(line_length)
		
		# make text scroll
		line_1_offset = 0
		if len(line_1) > line_length:
			line_1_overflow = len(line_1) - line_length
			line_1_offset = frame % (line_1_overflow + 1)
	
		display += line_1[line_1_offset:line_1_offset + line_length]
			
		line_2_offset = 0
		if len(line_2) > line_length:
			line_2_overflow = len(line_2) - line_length
			line_2_offset = frame % (line_2_overflow + 1)

		display += line_2[line_2_offset:line_2_offset + line_length]

		return display

class Spotify:
	def __init__(self, token, client_id, client_secret):
		self.client_id = client_id
		self.client_secret = client_secret
		self.token = Auth(client_id, client_secret).token
		print(f"TOKEN IS {self.token}")
		

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

	# takes in an int between 1 and 100 as the volume
	def set_volume(self, vol):
		if not 0 <= vol <= 100:
			return
		req = requests.put(
			f"https://api.spotify.com/v1/me/player/volume?volume_percent={vol}",
			headers={
					"Authorization": f"Bearer {self.token}"
			}
		)
	