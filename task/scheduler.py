from django_cron import CronJobBase, Schedule
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .models import *
from datetime import datetime, timedelta

# youtubeKeys = None

class fetchYoutubeVideoData(CronJobBase):
    RUN_EVERY_MINS = .01


    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'task.fetchData'

    def do(self):
        print('Hello World')
        valid = False
        youtubeKeys = os.getenv('YOUTUBE_KEY').split(",")

        # global youtubeKeys
        # if youtubeKeys is None:
        #     print(Keys.objects.all())
        #     keys = os.getenv('YOUTUBE_KEY').split(",")
        #     youtubeKeys = dict((k,1) for k in keys)
            # youtubeKeys = os.getenv('YOUTUBE_KEY').split(",")
    
        time_now = datetime.now()
        last_api_call = time_now -timedelta(minutes=.01)
        # print(youtubeKeys[0])
        for key in youtubeKeys:
            try:
                print(key)
                service = build('youtube', 'v3', developerKey=key)
                if service:
                    request = service.search().list(part="snippet",q="how to make tea",type="video",order="date",publishedAfter="2010-01-01T00:00:00Z",maxResults=5)
                    result = request.execute()
                    # print(result)
                    valid = True
                if valid:
                    break
                # if youtubeKeys[key]:
                #     if service:
                #         request = service.search().list(part="snippet",q="how to make tea",type="video",order="date",publishedAfter="2010-01-01T00:00:00Z",maxResults=5)
                #         result = request.execute()
                #         # print(result)
                #         valid = True
                #     if valid:
                #         break
            except HttpError as err:
                # youtubeKeys[key] = 0
                # print(youtubeKeys)
                print(err)
                code = err.resp.status
                if not(code == 400 or code == 403):
                    break
            # except Exception as e:
                # print(type(e))

    
        for item in result['items']:
                video_id = item['id']['videoId']
                publishedDateTime = item['snippet']['publishedAt']
                title = item['snippet']['title']
                description = item['snippet']['description']
                thumbnailsUrls = item['snippet']['thumbnails']['default']['url']
                channel_id = item['snippet']['channelId']
                channel_title = item['snippet']['channelTitle']
                print(title)
                Videos.objects.create(
                    video_id=video_id,
                    title=title,
                    description=description,
                    channel_id=channel_id,
                    channel_title=channel_title,
                    publishedDateTime=publishedDateTime,
                    thumbnailsUrls=thumbnailsUrls,
                )