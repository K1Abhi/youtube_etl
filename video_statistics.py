import requests
import os
from dotenv import load_dotenv
from datetime import date
import json 

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "artbyamit_official"
maxResults = 50


def get_playlist():
    response = requests.get(
        f"https://youtube.googleapis.com/youtube/v3/channels"
        f"?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
    )
    response.raise_for_status()
    data = response.json()

    if not data.get("items"):
        raise ValueError("Invalid channel handle or API key")

    return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_video_id(channel_playlistId):
    video_ids = []
    page_token = None
    base_url = (
        f"https://youtube.googleapis.com/youtube/v3/playlistItems"
        f"?part=contentDetails&playlistId={channel_playlistId}"
        f"&key={API_KEY}&maxResults={maxResults}"
    )

    while True:
        url = base_url
        if page_token:
            url += f"&pageToken={page_token}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        for item in data.get("items", []):
            video_ids.append(item["contentDetails"]["videoId"])

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return video_ids

def extract_video_data(video_ids):
    extracted_data = []

    def batch_list(video_ids, batch_size):
        for video_id in range(0,len(video_ids), batch_size):
            yield video_ids[video_id: video_id + batch_size]

    try:
        for batch in batch_list(video_ids, maxResults):
            video_id_str = ",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={video_id_str}&key={API_KEY}"

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for items in data.get('items', []):
                video_id = items["id"]
                snippet = items["snippet"]
                contentDetails = items["contentDetails"]
                statistics = items["statistics"]

                video_data = {
                "video_id" : video_id,
                "title" : snippet["title"],
                "publishedAt" : snippet["publishedAt"],
                "duration" : contentDetails["duration"],
                "viewCount" : statistics.get("viewCount", None),
                "likeCount" : statistics.get("likeCount", None),
                "commentCount" : statistics.get("commentCount", None),

                }

                extracted_data.append(video_data)

        return extracted_data
    
    except requests.exceptions.RequestException as e:
        raise e
    
def save_to_json(extracted_data):
    file_path = f"./data/YT_data_{date.today()}_{CHANNEL_HANDLE}.json"

    with open(file_path, "w", encoding="utf-8") as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    playlist_id = get_playlist()
    video_ids = get_video_id(playlist_id)
    print("Total videos:", len(video_ids))

    video_data = extract_video_data(video_ids)
    save_to_json(video_data)
    
