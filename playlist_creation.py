from typing import List
import json
import requests

MAIN_API = 'https://api.spotify.com/v1'

def get_session(access_token: str) -> requests.Session:
    headers = {"Authorization": f"Bearer {access_token}"}
    session = requests.Session()
    session.headers = headers
    return session


def get_user_profile(session: requests.Session) -> str:
    response = session.get(f'{MAIN_API}/me/')
    profile = response.json()
    print('✔️  Logged in as:', profile['display_name'])
    return profile['id']


def create_playlist(
    session: requests.Session,
    user_id: str,
    playlist_name: str,
    is_public: bool
) -> str:
    response = session.post(
        f'{MAIN_API}/users/{user_id}/playlists/',
        data=json.dumps({
            'name': playlist_name,
            'public': is_public,
            'description': 'Created using the Spotify Playlist generator',
        })
    )
    playlist_id = response.json()['id']
    print('✔️  Playlist created successfully!')
    return playlist_id


def add_tracks_to_playlist(
    session: requests.Session,
    playlist_id: str,
    track_ids: List[str]
) -> None:
    session.post(
        f'{MAIN_API}/playlists/{playlist_id}/tracks',
        data=json.dumps({
            'uris': [f'spotify:track:{track_id}' for track_id in track_ids]
        })
    )
    print('✔️  Tracks added to the playlist. Enjoy!')
