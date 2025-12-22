import requests
import json

API_KEY = "AIzaSyDB-Y2qADKD2LXtvNZ2VeA27LRywNe40eU"
CHANNEL_HANDLE = "MrBeast"


def get_playlist():

    try:
        response = requests.get(
            f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        )

        data = response.json()
        channel_playlistId = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        return channel_playlistId

    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    id = get_playlist()
    print(id)


































