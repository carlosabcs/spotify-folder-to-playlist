from auth import generate_token, refresh_token, get_session
from dotenv import load_dotenv
import argparse
import os
from processor import get_track_ids
from playlist_creation import get_user_profile, create_playlist, add_tracks_to_playlist

def main():
    load_dotenv()

    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    MAIN_DIR = os.getenv('MAIN_DIR')
    REDIRECT_URI = os.getenv('REDIRECT_URI')

    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=str, help="The name of the folder with the music files")
    parser.add_argument("playlist", type=str, help="The name of the playlist to be created")
    parser.add_argument(
        "public",
        type=bool,
        help="Whether or not the playlist should be public",
        default=True
    )
    parser.add_argument(
        "--authorize",
        action="store_true",
        help="Give the requested authorizations to the service"
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Refresh the access token"
    )
    args = parser.parse_args()

    if args.authorize:
        generate_token(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
        ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    elif args.refresh:
        refresh_token(REFRESH_TOKEN, CLIENT_ID)
        ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    else:
        if ACCESS_TOKEN:
            print('The access token is not active anymore, run again the script with the --refresh flag enabled.')
        else:
            print('Please run again the script with the --authorize flag enabled.')
        return
    
    session = get_session(ACCESS_TOKEN)
    user_id = get_user_profile(session)
    track_ids = get_track_ids(session, folder=f'{MAIN_DIR}{args.folder}/')
    playlist_id = create_playlist(session, user_id, args.playlist, args.public)
    add_tracks_to_playlist(session, playlist_id, track_ids)

if __name__ == "__main__":
    main()
