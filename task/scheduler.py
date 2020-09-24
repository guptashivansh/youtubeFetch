from django_cron import CronJobBase, Schedule
import os

from googleapiclient.discovery import build
from .models import *


class fetchYoutubeVideoData(CronJobBase):
    RUN_EVERY_MINS = .01


    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'task.fetchData'

    def do(self):
        print('Hello World')
        valid = False
        youtubeKeys = os.getenv('YOUTUBE_KEY').split(",")
        # print(youtubeKeys[0])
        for key in youtubeKeys:
            service = build('youtube', 'v3', developerKey=key)
            result = service.search().list(part="snippet",q="how to make tea",type="video",order="date",publishedAfter="2010-01-01T00:00:00Z").execute()
            valid = True
            # result = service.search().list(part="snippet",q="tea how",type="video",order="date").execute()
            # result = service.search().list(part="snippet",q="tea how",type="video",order="date", publishedAfter="2019").execute()
            # response = request.execute()
            # print(result)
            if valid:
                break

        if valid:
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