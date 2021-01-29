from spotify import SpotifyClient
from youtube import YoutubeClient


def run():

    youtube_json_location = "./creds/client_secret.json"

    # ------ YOUTUBE ------

    # Get necessary YouTube credentials.
    youtube_client = YoutubeClient(youtube_json_location)

    # Get the playlist ID the user wants to convert.
    yt_playlist_id = youtube_client.get_playlists()

    # Get the tracks from that playlist.
    tracks = youtube_client.get_playlist_tracks(yt_playlist_id)

    # ----- SPOTIFY ------

    # Get necessary Spotify credentials
    user_id, api_token = None, None
    secret_file = open("./creds/secrets2.txt")
    for i, line in enumerate(secret_file):
        if i == 1:
            user_id = line.rstrip('\n')
        if i == 3:
            api_token = line

    spotify_client = SpotifyClient(api_token, user_id)

    # Create a new playlist.
    playlist_name = "The Test"
    playlist_description = "My first true try."
    public_on = False

    sp_playlist_id = spotify_client.create_playlist(playlist_name, playlist_description, public_on)

    # Get song URI of our query.
    song_uris = []
    for track_title in tracks:
        song_uris.append(spotify_client.search_general(track_title))

    for song_uri in song_uris:
        spotify_client.add_to_playlist(sp_playlist_id, song_uri)


if __name__ == '__main__':
    run()
