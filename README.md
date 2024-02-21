# Add Top Last.fm Tracks to a Spotify Playlist

This project uses the Last.fm API to fetch a user's top tracks and then uses the Spotify Web API to search for those tracks and add to a playist.

## Requirements

- Python 3
- A Spotify Developer account
- A Last.fm account

## Setup

1. Clone this repository.
2. Install the Pylast and Spotipy libraries.
3. Set up your Spotify Developer account and create a new application. Note down the Client ID and Client Secret.
4. Set up your Last.fm account and note down the API Key, API Secret, username, and password.
5. Export these as environment variables in a .env file:
    ```bash
     SPOTIPY_CLIENT_ID='your-spotify-client-id'
     SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
     API_KEY='your-lastfm-api-key'
     API_SECRET='your-lastfm-api-secret'
     LASTFM_USERNAME='your-lastfm-username'
     LASTFM_PASSWORD='your-lastfm-password'
    ```

6. Setup paramters in setup.py.

## Usage

1. Run the Last.fm converter script:

    ```bash
    python lastfmTracks.py
    ```

   This will create a text file named 'output.txt' in the project directory. Each line of the file will contain a track name and an artist name, separated by ' - '.

2. Run the Spotify track finder script:

    ```bash
    python main.py
    ```

   This script will search for each track on Spotify and print the URI of the first match it finds. If it doesn't find a match using the track name and artist name together, it will try searching just for the artist name, and then just for the track name and then add that to playlist.

## Limitations

The Spotify Web API's search function isn't perfect, and there may be cases where it can't find a match for a given track name or artist name. The script tries to mitigate this by using different search strategies, but it may not always be successful.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the terms of the MIT license.