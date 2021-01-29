from spotify import SpotifyClient
from youtube import YoutubeClient

def run():

    USER_ID = user_id
    API_TOKEN = api_token

    # Begin with YouTube
    youtube_client = YoutubeClient("./creds/client_secret.json")
    playlists = youtube_client.get_playlists()
    titles = youtube_client.get_playlist_items(playlists)

    # Then go for Spotify
    spotify_client = SpotifyClient(API_TOKEN, USER_ID)

    # Create a playlist
    playlist_id = spotify_client.create_playlist("New Shit", "This is my first attempt.", False)

    # song_uri = spotify_client.search_song("Andy Shauf", "Neon Skyline")

    # Get the song uri of our query

    song_uris = []
    for title in titles:
        song_uris.append(spotify_client.search_generally(title))

    for song_uri in song_uris:
        spotify_client.add_to_playlist(playlist_id, song_uri)


if __name__ == '__main__':
    run()
