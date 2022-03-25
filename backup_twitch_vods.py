import argparse
import json
import logging
import time
import os
from datetime import datetime

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl
from googleapiclient.http import MediaFileUpload

import my_secrets


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def get_stream_info(username : str):
    url = f"https://api.twitch.tv/helix/streams?user_login={username}&first=1"

    headers = {
        'Authorization': my_secrets.auth,
        'Client-Id': my_secrets.client_id
    }

    res = requests.get(url, headers=headers)
    return json.loads(res.text)


def is_live(username: str):
    stream_data = get_stream_info(username)
    if len(stream_data['data']) > 0:
        logging.info(f"{username} is live")
        return True
    else:
        return False


def download_vod(username: str, directory: str, stream_data : dict):
    stream_id = stream_data['id']
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ydl_opts = {
        'outtmpl': f'{directory}/{date_str}_{username}_{stream_id}.mp4',
        'quiet': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        logging.info(f"downloading latest {username} vod")
        ydl.download([f'https://www.twitch.tv/{username}'])
        logging.info(f"finished downloading latest {username} vod")
        return ydl_opts['outtmpl']


def get_youtube_category(youtube):
    country_code = input("Enter 2 letter country code (ISO 3166-1 alpha-2 format): ")
    if len(country_code) != 2:
        print("Country code must be 2 letters")

    request = youtube.videoCategories().list(
        part="snippet",
        regionCode=country_code.upper()
    )

    response = request.execute()

    cls()
    for cat in response['items']:
        print(f"{cat['id']} - {cat['snippet']['title']}")

    category = input('Enter the number of the category you wish to upload VODs under: ')
    cls()

    return category


def auth_with_youtube():
    scopes = ["https://www.googleapis.com/auth/youtube.readonly",
              "https://www.googleapis.com/auth/youtube.upload"]
    client_secrets_file = "client_secrets.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)


def upload_to_youtube(youtube, vod_path, stream_data):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": f"{stream_data['user_name']} - {stream_data['title']} - {stream_data['game_name']}",
            "description": f"Streamed at {stream_data['started_at']}\nID: {stream_data['id']}",
            "tags": [
              stream_data['user_name'],
              stream_data['game_name'],
              stream_data['title']
            ],
            "categoryId": "20" # gaming in US
          },
          "status": {
            "privacyStatus": "private"
          }
        },
        media_body=MediaFileUpload(vod_path)
    )
    response = request.execute()
    logging.info(f"YouTube video available at: https://www.youtube.com/watch?v={response['id']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='PROG',
                                     description='Waits for a Twitch streamer to go live, then downloads their VOD. Optionally uploads the VOD straight to YouTube.')

    parser.add_argument('-u', '--username', type=str,
                        help='Username of Twitch streamer to stalk')
    parser.add_argument('-p', '--polling_rate', type=int, default=10,
                        help='Number of seconds to sleep between stalks')
    parser.add_argument('-d', '--directory', type=str, default='vods',
                        help="The directory to the save the VODs in")
    parser.add_argument('-y', '--youtube', action=argparse.BooleanOptionalAction,
                        default=False, help="Upload the recorded VOD to YouTube once it's completed")

    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s\t%(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S', level=logging.INFO)

    youtube = None
    if args.youtube:
        youtube = auth_with_youtube()

    logging.info(f"Waiting for {args.username} to turn the stream on")
    while (True):
        if not is_live(args.username):
            time.sleep(args.polling_rate)
            continue
        stream_data = get_stream_info(args.username)['data'][0]
        vod_path = download_vod(args.username, args.directory, stream_data)
        if args.youtube:
            upload_to_youtube(youtube, vod_path, stream_data)
        time.sleep(60)
