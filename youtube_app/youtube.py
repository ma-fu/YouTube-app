from googleapiclient.discovery import build
import os

api_key = os.getenv('API_KEY')

class YouTube:
    def __init__(self):
        self.youtube = build('youtube','v3',developerKey=api_key)

    def search_video(self,q=False,channel=False,tkn=False):
        tips = {
                'part':'id,snippet',
                'order':'date',
                'maxResults':50
                }
        if q:
            tips['q']=q
        if channel:
            tips['channelId']=channel
        if tkn:
            tips['pageToken']=tkn

        return self.youtube.search().list(**tips).execute()
