# Backup a streamer's Twitch VODs

Waits for a Twitch streamer to go live, then downloads their VOD. There's probably a better command line tool for this but I couldn't find one.

### To Use:

- Download the [Python 3.10](https://www.python.org/downloads/)
- Clone the repo & navigate to the dir
    - `git clone https://github.com/skend/<name_here>`
    - `cd backup_twitch_vods`
- Install the required dependencies
    - `pip install -r requirements.txt`
- [Register a Twitch application to get your Auth token and Client-Id](https://dev.twitch.tv/docs/authentication#registration)
- Add your auth token and client-id to the my_secrets.py file (example below):
    - ```
        auth = 'Bearer 8uossvabcdefgh123456tblte5i25w'
        client_id = 't2ujbhtfvabcdefgh123456xz3yiuk'
        ```
- Run `python backup_twitch_vods.py -h" to see how to run


```
λ python backup_twitch_vods.py -h
usage: PROG [-h] [-u USERNAME] [-p POLLING_RATE] [-d DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Username of Twitch streamer to stalk
  -p POLLING_RATE, --polling_rate POLLING_RATE
                        Number of seconds to sleep between stalks
  -d DIRECTORY, --directory DIRECTORY
                        The directory to the save the vods in
```


### Examples:

`python backup_twitch_vods.py -u mizkif -p 10 -d "/home/skend/twitch/no_content_streamer"`