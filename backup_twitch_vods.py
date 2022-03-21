import requests
import json
import time
import youtube_dl
import argparse
import log
import my_secrets
from datetime import datetime


def is_live(username : str):
    url = f"https://api.twitch.tv/helix/streams?user_login={username}&first=1"

    headers = {
        'Authorization': my_secrets.auth,
        'Client-Id': my_secrets.client_id
    }

    log.info(f"checking if {username} is live")
    res = requests.get(url, headers=headers)
    parsed = json.loads(res.text)
    if len(parsed['data']) > 0:
        log.info(f"{username} is live")
        return True
    else:
        log.info(f"{username} is offline")
        return False


def download_vod(username : str, directory : str):
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ydl_opts = {
        'outtmpl': f'{directory}/{date_str}_{username}_%(id)s.%(ext)s',
        'quiet': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        log.info(f"downloading latest {username} vod")
        ydl.download([f'https://www.twitch.tv/{username}'])
        log.info(f"finished downloading latest {username} vod")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('-u', '--username', type=str, help='Username of Twitch streamer to stalk')
    parser.add_argument('-p', '--polling_rate', type=int, help='Number of seconds to sleep between stalks')
    parser.add_argument('-d', '--directory', type=str, help="The directory to the save the vods in")
    args = parser.parse_args()

    while (True):
        if not is_live(args.username):
            time.sleep(args.polling_rate)
            continue
        download_vod(args.username, args.directory)
        time.sleep(30)
