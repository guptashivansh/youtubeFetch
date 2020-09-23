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
        # AIzaSyBpHQLIyDjThRPlbfWvW-vV3hmn2locRjM
        service = build('youtube', 'v3', developerKey='AIzaSyAPwUBHA2EYoFusv8KcXFUI7VFFZ2FXXSY')
        result = service.search().list(part="snippet",q="how to make tea",type="video",order="date",publishedAfter="2010-01-01T00:00:00Z").execute()
        # result = service.search().list(part="snippet",q="tea how",type="video",order="date").execute()
        # result = service.search().list(part="snippet",q="tea how",type="video",order="date", publishedAfter="2019").execute()
        # response = request.execute()
        # print(result)
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
        pass
    