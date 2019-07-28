import requests
import threading
import time
import sys

class PlaylistGetter:
	def __init__(self, token):
		self.token = token

	def __call__(self):
		global playlists
		global arg

		headers = {'Authorization':'Bearer ' + self.token}
		r = requests.get("https://api.spotify.com/v1/users/" + arg + "/playlists", params = {'limit':50}, headers = headers)
		playlists = []
		while True:
			jsonResponse = r.json()
			nextReq = jsonResponse['next']
			temp = jsonResponse['items']
			playlists.extend(map(lambda x: x['id'], temp))
			if nextReq is None:
				break
			else:
				r = requests.get(nextReq, headers = headers)

class TrackGetter:
	def __call__(self):
		global tracks
		global token

		headers = {'Authorization':'Bearer ' + token}
		tracks = {}
		for playlist in playlists:
			r = requests.get("https://api.spotify.com/v1/playlists/" + playlist + "/tracks", headers = headers, params = {'limit':100})
			while True:
				if r.status_code == 429:
					waitTime = r.headers['Retry-After']
					time.sleep(waitTime)
					r = requests.get(r.request.url, headers = headers)
				else:
					jsonResponse = r.json()
					nextReq = jsonResponse['next']
					temp = jsonResponse['items']
					temp = map(lambda x: x['track'], temp)
					tracks.update(map(lambda x: [x['name'],x['artists'][0]['name']], temp))
					if nextReq is None:
						break
					else:
						r = requests.get(nextReq, headers = headers)




def printTracks(list):
	global tracks

	f = open("tracks.txt", "w+")
	for track in tracks:
		f.write(tracks[track] + "  -  " + track+ "\r\n")
	f.close()

arg = len(sys.argv)
if arg != 2:
	raise EnvironmentError("You must insert a Spotify username as the only parameter")
arg = sys.argv[1]
body_param = {'grant_type':'client_credentials'}
heads = {'Authorization':'Basic OGY3NzE4ODg1ZDJhNDEzMDgwMjQwYTRjZmUzMWQ0ZDQ6OTBhNWZlNmE3MWZlNDRjMjhjYTVmNWY1YzM1ZjY4OTI='}

r = requests.post("https://accounts.spotify.com/api/token", data = body_param, headers = heads)

# print(r.text)
# print(r.status_code)

token = r.json()['access_token']

getter = threading.Thread(target = PlaylistGetter(token))
getter.start()
getter.join()
getter = threading.Thread(target = TrackGetter())
getter.start()
print("TrackList is retrieving all your tracks... Please be patient")
getter.join()
print("DONE!")
printTracks(tracks)
print("You have " + str(len(tracks)) + " tracks in your playlists")


