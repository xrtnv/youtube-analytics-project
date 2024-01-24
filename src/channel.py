import json
import os
import re

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        if not re.match(r"^[a-zA-Z0-9_-]{24}$", channel_id):
            raise ValueError("Invalid YouTube channel ID")
        self._channel_id = channel_id

        youtube = self.get_service()
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        channel_snippet = channel['items'][0]['snippet']
        channel_statistics = channel['items'][0]['statistics']

        self.title = channel_snippet['title']
        self.description = channel_snippet['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscribers = channel_statistics['subscriberCount']
        self.video_count = channel_statistics['videoCount']
        self.total_views = channel_statistics['viewCount']

    @property
    def channel_id(self):
        return self._channel_id

    def fetch_info(self) -> None:
        """Получает информацию о канале через API."""
        try:
            youtube = self.get_service()
            channel = youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()
            return channel
        except Exception as e:
            pass

    def get_info(self) -> None:
        """Возвращает информацию о канале в виде строки."""
        return self.fetch_info()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(self.get_info())

    @staticmethod
    def get_service():
        api_key = str(os.getenv('YOUTUBE_API_KEY'))
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, path):

        channel_data = {
            'channel_id': self._channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscribers': self.subscribers,
            'video_count': self.video_count,
            'total_views': self.total_views
        }
        with open(path, 'w+') as file:
            json.dump(channel_data, file)
