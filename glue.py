from spotify import SpotifyClient
from youtube import YoutubeClient


class Glue(object):

    def __int__(self, yt_json_source, sp_creds_source):
        self.yt_json_source = yt_json_source
        self.sp_creds_source = sp_creds_source

    def generate(self, new_playlist_name, playlist_description, is_public):

        # ------ YOUTUBE ------

        # Get necessary YouTube credentials.
        youtube_client = YoutubeClient(self.yt_json_source)

        # Get the playlist ID the user wants to convert.
        yt_playlist_id = youtube_client.get_playlists()

        # Get the tracks from that playlist.
        tracks = youtube_client.get_playlist_tracks(yt_playlist_id)

        # ----- SPOTIFY ------

        # Get necessary Spotify credentials
        user_id, api_token = None, None
        secret_file = open(self.sp_creds_source)
        for i, line in enumerate(secret_file):
            if i == 1:
                user_id = line.rstrip('\n')
            if i == 3:
                api_token = line

        spotify_client = SpotifyClient(api_token, user_id)

        # Create the new playlist
        sp_playlist_id = spotify_client.create_playlist(new_playlist_name, playlist_description, is_public)

        # Get song URI of our query.
        song_uris = []
        for track_title in tracks:
            song_uris.append(spotify_client.search_general(track_title))

        # Add the songs to the playlist.
        for song_uri in song_uris:
            spotify_client.add_to_playlist(sp_playlist_id, song_uri)

        # Done!
