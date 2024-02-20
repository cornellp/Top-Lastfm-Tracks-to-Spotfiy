import pylast
import os
import setup
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Authenticate with Last.fm
username = os.getenv('LASTFM_USERNAME')
password_hash = pylast.md5(os.getenv('LASTFM_PASSWORD'))

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash,
)

#Define period of time to get top tracks from
period = setup.period
tracks_num = setup.tracks_num

if period == "1 Week":
    period = pylast.PERIOD_7DAYS
elif period == "1 Month":
    period = pylast.PERIOD_1MONTH
elif period == "3 Months":
    period = pylast.PERIOD_3MONTHS
elif period == "6 Months":
    period = pylast.PERIOD_6MONTHS
elif period == "12 Months":
    period = pylast.PERIOD_12MONTHS
elif period == "Overall":
    period = pylast.PERIOD_OVERALL

# Get the user's top tracks
top_tracks = network.get_user(username).get_top_tracks(limit=tracks_num, period=period)

# Print the top tracks
for track in top_tracks:
    # Save the tracks to a file
    with open('output.txt', 'w', encoding='utf-8') as file:
        for track in top_tracks:
            file.write(f"{track.item.title} - {track.item.artist}\n")