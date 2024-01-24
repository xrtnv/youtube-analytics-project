import os
from datetime import timedelta

import isodate
from googleapiclient.discovery import build

from src.video import Video


class PlayList(Video):
    def __init__(self, playlist_id: str) -> None:
        playlist = super().get_service().playlists().list(id=playlist_id, part="id, snippet").execute()
        self.playlist_id = playlist_id

        self.title = playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlist['items'][0]['id']}"

        playlist_videos = super().get_service().playlistItems().list(playlistId=playlist_id,
                                                                     part='contentDetails',
                                                                     ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        self.video_response = super().get_service().videos().list(part='contentDetails,statistics',
                                                                  id=','.join(video_ids)
                                                                  ).execute()

    @property
    def total_duration(self):
        total_duration = 0

        for video in self.video_response['items']:
            duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(duration).seconds
            total_duration += duration

        return timedelta(seconds=total_duration)

    def show_best_video(self):
        max_likes: int = 0
        bests_video: str = ""

        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > max_likes:
                max_likes = int(video['statistics']['likeCount'])
                bests_video = video['id']
        return f"https://youtu.be/{bests_video}"
