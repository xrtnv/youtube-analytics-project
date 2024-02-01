import json
import os
import re
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.title = None
        self.link = None
        self.views = None
        self.like_count = None

        youtube = self.get_service()
        video = youtube.videos().list(id=self.video_id, part='snippet,statistics').execute()
        if len(video['items']) > 0:
            video_snippet = video['items'][0]['snippet']
            video_statistics = video['items'][0]['statistics']
            self.title = video_snippet['title']
            self.link = f'https://www.youtube.com/watch?v={self.video_id}'
            self.views = video_statistics['viewCount']
            self.like_count = video_statistics['likeCount']


    def __str__(self):
        return self.title

    @staticmethod
    def get_service():
        api_key = str(os.getenv('YOUTUBE_API_KEY'))
        return build('youtube', 'v3', developerKey=api_key)


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return super().__str__()
