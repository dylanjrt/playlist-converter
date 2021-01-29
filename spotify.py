import requests
import urllib.parse
import json


class SpotifyClient(object):
    trying
    to
    change

    def __init__(self, api_token, user_id):
        self.api_token = api_token
        self.user_id = user_id

    def search_generally(self, input):
        query = urllib.parse.quote(f'{input}')
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )
        response_json = response.json()
        results = response_json['tracks']['items']
        if results:
            return results[0]['uri']
        raise Exception(f"No results found for {input}")

    # Get the spotify uri of the given song.
    def search_song(self, artist, track):
        query = urllib.parse.quote(f'{artist} {track}')
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )
        response_json = response.json()
        results = response_json['tracks']['items']
        if results:
            return results[0]['uri']
        raise Exception(f"No results found for {artist} : {track}")

    # Get the playlist ID that we are creating.
    def create_playlist(self, playlist_name, playlist_description, bool_public):
        query = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"

        request_body = json.dumps({
            "name": playlist_name,
            "description": playlist_description,
            "public": bool_public
        })

        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )
        response_json = response.json()

        return response_json["id"]

    # Add the song to our created playlist.
    def add_to_playlist(self, playlist_id, uri):
        query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        uris = [uri]
        request_data = json.dumps(uris)
        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )
