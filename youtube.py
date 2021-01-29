from pytube import YouTube

import os

import google_auth_oauthlib
import googleapiclient.discovery
import youtube_dl


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

        titles = {}
        playlist_ids = []
        index = 0
        for data in all_playlists:
            titles[index] = data["snippet"]["localized"]["title"]
            playlist_ids.append(data["id"])
            index += 1

        for k, v in titles.items():
            print(k, v)
        selection = input("Select the corresponding number of the playlist you would like to convert.")

        return playlist_ids[int(selection)]

    def get_playlist_tracks(self, playlist_id):
        request = self.youtube_client.playlistItems().list(
            playlistId=playlist_id,
            part="snippet"
        )

        response = request.execute()

        all_songs = []
        for data in response["items"]:
            video_id = data["snippet"]["resourceId"]["videoId"]
            artist, track = self.get_artist_and_track(video_id)

            if artist and track:
                all_songs.append({"artist": artist, "track": track})

        return all_songs

    @staticmethod
    def get_artist_and_track(video_id):

        youtube_url = f"https://www.youtube.com/watch?v={video_id}"

        video = YouTube(youtube_url)
        meta = video.metadata

        artist = meta[0]["Artist"]
        track = meta[0]["Song"]

        return artist, track


