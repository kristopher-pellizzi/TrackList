# TrackList
Utility python script to retrieve the tracks a Spotify user has in his/her playlists

-----
## Usage
**TrackList** is very simple to be used:
1. Be sure that python3 is installed in your system
2. If not already installed, install *requests* module by launching from terminal
```bash
pip install requests
```
3. Download the script spotify_tracks.py and launch it from terminal with command
```bash
python3 spotify_tracks.py <username>
```
replacing *username* with Spotify username.

After some seconds (***Actual time varies according to the number of playlists and tracks the user has***) the script will produce a txt file in the same folder of the script, containing the list of couples <Author> - <Track name>
