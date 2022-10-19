import pickle
from urllib.error import HTTPError
from googleapiclient.discovery import build
import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

vid_id_list = []
pl_cr_id = ''

try:
    f = open('assets/mood.txt', 'r')

    credentials = None

    queries = {
        'sad': 'lofi chill songs', 
        'happy': 'upbeat cheery lively songs lyrics', 
        'neutral': 'trending songs lyrics', 
        'angry': 'metal songs lyrics',
        'fear': 'soothing songs lyrics',
        'surprised': 'rap songs lyrics'
    }

    quan = 3
    now = datetime.datetime.now()

    print('Loading Credentials From File...')
    with open('assets/token.pickle', 'rb') as token:
        credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())

    youtube = build('youtube', 'v3', credentials=credentials)

    mood = f.read()
    f.close()
    f = open('assets/mood.txt', 'w')

    pl_search_request = youtube.search().list(
        part='snippet',
        q = queries[mood],
        type = "playlist",
        relevanceLanguage = "en",
    )

    pl_response = pl_search_request.execute()
    vid_id_list = []

    pl_id = []
    for i in range(4):
        pl_id.append(pl_response["items"][i]['id']['playlistId'])

    for i in range(quan):
        pl_url_req = youtube.playlistItems().list(
            part='contentDetails', 
            playlistId = pl_id[i]
        )

        pl_url_res = pl_url_req.execute()

        for j in range(quan):
            vid_id = pl_url_res['items'][j]['contentDetails']['videoId']
            vid_id_list.append(vid_id)
            
    pl_insert_req = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": 'Generated Playlist: ' + queries[mood],
                    "description": f'Generated on {now.strftime("%d-%m%Y %I:%M:%S %p")}, by Moody™ (all rights reserved).',
                    "tags": [
                    "sample playlist",
                    "API call"
                    ],
                    "defaultLanguage": "en"
                },
                "status": {
                    "privacyStatus": "public"
                }
                }
        )

    pl_ins_response = pl_insert_req.execute()
    pl_cr_id = pl_ins_response["id"]
    
    pl_del_request = youtube.playlists().delete(
        id=pl_cr_id
    )

except HttpError:
    f.write('quota')
    f.close
    exit()

try:
    for _id in vid_id_list:
        print(_id)
        yt_pl_it = youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": pl_cr_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": _id
                        }
                    }
                }
            )
        yt_pl_it_res = yt_pl_it.execute()

    f.write(f"https://www.youtube.com/playlist?list={pl_cr_id}")

    f.close()

except HttpError:
    f.write('err')
    f.close()