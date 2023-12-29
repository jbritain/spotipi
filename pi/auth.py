# I just want anyone reading this mess to know that large portions of it were suggested by ChatGPT,
# I could not find a better way to authenticate with minimal user input than to just start a web server
# and perform the authentication that way

import requests
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, urlencode
import webbrowser
import threading
import base64

class Auth:
	def __init__(self, client_id, client_secret):
		self.token = load_token()
		if self.token is None:
			self.token = get_token(client_id, client_secret)

# we store the token in local storage in case we restart and the token is still valid or something idk
# also used to load the token after it's written by my web server clusterfuck
def load_token():
	try:
		with open("token.txt", "r") as token:
			return token.read()
	except Exception:
		return None

# a web server which listens on port 8080 and handles authentication with spotify
# this is what the redirect URI for the spotify API settings talks to
class CallbackHandler(http.server.BaseHTTPRequestHandler):
	
	# allow additional params for client id and secret to be passed into callback
	# I briefly considered doing this in the state parameter of the request URL
	# but soon realised that was a fucking horrible idea
	def __init__(self, request, client_address, server, client_id, client_secret):
		self.client_id = client_id
		self.client_secret = client_secret
		super().__init__(request, client_address, server)

	# prevent logging to console
	def log_message(self, format, *args):
		pass

	# listens for requests
	def do_GET(self):
		# extract url params from request
		url_parts = urlparse(self.path)
		query_params = parse_qs(url_parts.query)

		code = query_params.get('code')[0] # get the returned code, idk why it's in an array

		# encode the client id and secret in base64
		credentials = f"{self.client_id}:{self.client_secret}"
		credentials_base64 = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

		# send request back with code
		req = requests.post(
			"https://accounts.spotify.com/api/token",
			headers={
				"Content-Type": "application/x-www-form-urlencoded",
				"Authorization": f"Basic {credentials_base64}"
			},
			data=urlencode({
				"grant_type": "authorization_code",
				"code": code,
				"redirect_uri": "http://localhost:8080",
				"scope": "user-read-playback-state user-modify-playback-state user-read-currently-playing"
			})
		)

		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

		if (req.status_code == 200):
			token = req.json().get("access_token")

			# store the token in the text file
			# this is almost the worst way of communicating between threads
			# but it kinda makes sense since we would store this at some point anyway
			with open("token.txt", "w") as f:
				f.write(token)

			# if everything worked just close the tab lmao
			self.wfile.write(b"<script>window.close()</script>authorized!") 
		else:
			# otherwise respond with the error
			self.wfile.write(req.content)

		# kill the server since we don't need it anymore, with a slight delay so the response can be sent
		threading.Timer(1, self.server.shutdown).start()

# start webserver and open the authentication page in the user's browser
def get_token(client_id, client_secret):
	httpd = socketserver.TCPServer(('localhost', 8080), lambda request, client_address, server: CallbackHandler(request, client_address, server, client_id, client_secret))
	webbrowser.open(f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri=http://localhost:8080&scope=user-read-playback-state user-modify-playback-state user-read-currently-playing")
	httpd.serve_forever()
	return load_token()