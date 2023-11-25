import dotenv
import json
import requests
import urllib.parse

SESSION_API = 'https://accounts.spotify.com/api'

def get_user_authorization(client_id: str, redirect_uri: str) -> None:
    params = {
        'client_id': client_id,
        'scope': 'user-read-private user-read-email playlist-modify-public playlist-modify-private',
        'response_type': 'code',
        'redirect_uri': redirect_uri,
    }
    print('Please access the following URL and grant the requested permissions:')
    print(f'https://accounts.spotify.com/authorize?{ urllib.parse.urlencode(params) }')


def refresh_token(refresh_token: str, client_id: str) -> None:
    params = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'client_id': client_id,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(
        f'{ SESSION_API }/token',
        data=params,
        headers=headers
    )
    if response.status_code == 200:
        json_response = json.loads(response.text)
        dotenv.set_key('.env', 'ACCESS_TOKEN', json_response['access_token'])
        dotenv.set_key('.env', 'REFRESH_TOKEN', json_response['refresh_token'])
    else:
        print(f"Error refreshing token: {response.status_code}")


def get_access_token(
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    authorization: str
) -> None:
    auth_data = {
        "grant_type": "authorization_code",
        "code": authorization,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(
        f'{SESSION_API}/token',
        data=auth_data,
        headers=headers
    )
    if response.status_code == 200:
        json_response = response.json()
        dotenv.set_key('.env', 'ACCESS_TOKEN', json_response['access_token'])
        dotenv.set_key('.env', 'REFRESH_TOKEN', json_response['refresh_token'])
    else:
        print(f"Error getting access token: {response.status_code}")


def generate_token(
    client_id: str,
    client_secret: str,
    redirect_uri: str
) -> None:
    get_user_authorization(client_id, redirect_uri)
    auth_code = input('Add here the auth code provided: ')
    get_access_token(client_id, client_secret, redirect_uri, auth_code)


def get_session(access_token: str) -> requests.Session:
    headers = {"Authorization": f"Bearer {access_token}"}
    session = requests.Session()
    session.headers = headers
    return session
