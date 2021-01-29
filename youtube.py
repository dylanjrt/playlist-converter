import requests
import urllib.parse
import json

import os

import google_auth_oauthlib
import googleapiclient.discovery


class YoutubeClient(object):

    def __init__(self, credentials_location):

        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            credentials_location, scopes)
        credentials = flow.run_console()
        self.youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

    def get_playlists(self):
        request = self.youtube_client.playlists().list(
            part="id,snippet",
            mine=True,
            maxResults=50
        )
        response = request.execute()

        all_playlists = response["items"]
        playlist = all_playlists[0]
        return playlist["id"]

    def get_playlist_items(self, playlist_id):
        request = self.youtube_client.playlistItems().list(
            playlistId=playlist_id,
            part="snippet"
        )

        response = request.execute()

        items = response["items"]
        snippet = items[0]
        title = snippet["title"]

        return title
