import mutagen
import os
import re
import requests
from typing import List
import urllib.parse

MAIN_API = 'https://api.spotify.com/v1'

def get_music_filenames_from_folder(folder: str) -> List[str]:
    try:
        return [
            filename for filename in os.listdir(folder)
            if filename.endswith(('.flac', '.mp3', '.m4a'))
        ]
    except Exception as e:
        print(f'Error loading folder: {e}')
        return []


def search_tracks(
    session: requests.Session,
    audiofile: object
) -> List[object]:
    q = f'track:{ audiofile["title"] }'
    if audiofile['album']:
        q += f' album:{ audiofile["album"] }'
    params = {
        'q': q,
        'type': 'track',
        'limit': 5,
    }
    response = session.get(
        f'{ MAIN_API }/search?{ urllib.parse.urlencode(params) }'
    )
    tracks = response.json()['tracks']
    return tracks['items']


def clean_album_name(album_name: str) -> str:
    return re.sub(
        r'\(explicit\)', '', # explicit
        re.sub(r'\(\d+\)', '', album_name.lower()) # numbers
    ).strip()


def parse_mutagen_file(audiofile: str, filename: str) -> object:
    return {
        'album': clean_album_name(audiofile.get('album', [''])[0]),
        'artist': audiofile.get('artist', [''])[0],
        'discnumber': audiofile.get('discnumber', [''])[0],
        'title': audiofile.get('title', [
            filename.replace('.mp3', '').replace('.flac', '').replace('.m4a', '')
        ])[0],
        'year': audiofile.get('originalyear', [''])[0],
    }


def get_track_ids(session: requests.Session, folder: str) -> List[str]:
    track_ids = []
    filenames = get_music_filenames_from_folder(folder)
    for filename in filenames:
        print(f'  {filename}...')
        audiofile = parse_mutagen_file(
            mutagen.File(f'{folder}{filename}', easy=True),
            filename
        )
        tracks = search_tracks(session, audiofile)
        if len(tracks):
            track_ids.append(tracks[0]['id'])
        else:
            print(f'  😢 { filename } was not found', audiofile)
    found_percentage = round((len(track_ids) / len(filenames) * 100), 2)
    print(f'✔️  {len(track_ids)}/{len(filenames)} ({found_percentage}%) tracks found')
    return track_ids
