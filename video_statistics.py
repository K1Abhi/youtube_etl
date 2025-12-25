import requests
import json
import os 
from dotenv import load_dotenv


load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
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
    print(get_playlist())


































