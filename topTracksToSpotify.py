# Import the required modules
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, redirect, url_for, session
from dotenv import load_dotenv
import os
import time
import setup

# Import setup variables
tracks_num = setup.tracks_num
period = setup.period

# Import env variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Initialize Flask app
app = Flask(__name__)

# Set the name of the session cookie
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'

# Set a random secret key to sign the cookie
app.secret_key = 'YOUR_SECRET_KEY'

# Set the key for the token info in the session dictionary
TOKEN_INFO = 'token_info'


# Route to handle logging in
@app.route('/')
def login():
    # Create a SpotifyOAuth instance and get the authorization URL
    auth_url = create_spotify_oauth().get_authorize_url()
    # Redirect the user to the authorization URL
    return redirect(auth_url)


@app.route('/redirect')
def redirect_page():
    # Clear the session
    session.clear()
    # Get the authorization code from the request parameters
    code = request.args.get('code')
    # Exchange the authorization code for an access token and refresh token
    token_info = create_spotify_oauth().get_access_token(code)
    # Save the token info in the session
    session[TOKEN_INFO] = token_info
    # Redirect the user to the save_top_tracks route
    return redirect(url_for('save_top_tracks', _external=True))


@app.route('/saveTopTracks')
def save_top_tracks():
    try:
        # Get the token info from the session
        token_info = get_token()
    except:
        # If the token info is not found, redirect the user to the login route
        print('User not logged in')
        return redirect("/")

    # Create a Spotipy instance with the access token
    sp = spotipy.Spotify(auth=token_info['access_token'])

    # Get the user's playlists
    current_playlists = sp.current_user_playlists()['items']
    top_tracks_playlist_id = None

    # Get user ID
    user_id = sp.current_user()['id']

    # Find the Discover Weekly and Saved Weekly playlists
    for playlist in current_playlists:
        if playlist['name'] == f'Top {tracks_num} Tracks - {period}':
            top_tracks_playlist_id = playlist['id']

    if not top_tracks_playlist_id:
        new_playlist = sp.user_playlist_create(user_id, f'Top {tracks_num} Tracks - {period}', public=True,
                                               collaborative=False, description=f"Your top {tracks_num} tracks - {period}")
        top_tracks_playlist_id = new_playlist['id']
    else:
        # Remove all tracks from the playlist
        sp.user_playlist_replace_tracks(user_id, top_tracks_playlist_id, [])

    # Get the top tracks from output.txt
    song_uri = []
    with open('output.txt', 'r') as file:
        lines = file.readlines()
        for line in lines[:tracks_num]:  # Only get the top tracks
            name, artist = line.strip().rsplit(' - ', 1)  # Split only on the last ' - '
            results = sp.search(q=f'track:{name} artist:{artist}', type='track', limit=10)
            if results['tracks']['items']:
                song_uri.append(results['tracks']['items'][0]['uri'])
            else:
                # Try searching just for the track name
                results = sp.search(q=f'track:{name}', type='track', limit=10)
                if results['tracks']['items']:
                    song_uri.append(results['tracks']['items'][0]['uri'])
                else:
                    # try searching just for the artist name
                    results = sp.search(q=f'artist:{artist}', type='track', limit=10)
                    if results['tracks']['items']:
                        song_uri.append(results['tracks']['items'][0]['uri'])
    
    # add the tracks to the Saved Weekly playlist
    sp.user_playlist_add_tracks(user_id, top_tracks_playlist_id, song_uri, None)
 
    # return a success message
    return (f'Sucessfully added top {tracks_num} tracks to playlist')

# function to get the token info from the session
def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        # if the token info is not found, redirect the user to the login route
        redirect(url_for('login', _external=False))
    
    # check if the token is expired and refresh it if necessary
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id, 
        client_secret=client_secret, 
        redirect_uri=url_for('redirect_page', _external=True), 
        scope="user-top-read playlist-modify-private playlist-modify-public user-library-modify user-library-read playlist-read-private ugc-image-upload",
        )
    
if __name__ == '__main__':
    app.run(debug=True)