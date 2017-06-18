from apiclient.discovery import build


class YoutubeChannel(object):
    def __init__(self, name, image, desc, channel_id):
        self.name = name
        self.image = image
        self.description = desc
        self.channel_id = channel_id

    @classmethod
    def from_api_response(cls, resp):
        name = resp['snippet']['title']
        image = resp['snippet']['thumbnails']['high']['url']
        description = resp['snippet']['description']
        channel_id = resp['snippet']['resourceId']['channelId']
        return cls(name, image, description, channel_id)

    def __str__(self):
        return "Channel {}".format(self.name)

    def __repr__(self):
        return '<Channel>{} {}</Channel>'.format(
            self.name,
            self.channel_id,
        )


class YoutubeVideo(object):
    def __init__(self, name, image, desc, video_id, channel_id):
        self.video_id = video_id
        self.channel_id = channel_id
        self.name = name
        self.image = image
        self.description = desc

    @classmethod
    def from_api_response(cls, resp):
        pass

    def __str__(self):
        return "Video {}".format(self.name)

    def __repr__(self):
        return "<Video>{} {}</Video>".format(
            self.name,
            self.video_id,
        )


class YoutubeAPI(object):
    def __init__(self, api_key):
        self.service = build('youtube', 'v3', developerKey=api_key)

    def channel(self, channel_id):
        channel_response = self.service.channels().list(
            part='snippet',
            id=channel_id,
        ).execute()
        return channel_response['items'][0]

    def video(self, video_id):
        video_response = self.service.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        try:
            return video_response['items'][0]
        except IndexError:
            raise ValueError('Cannot find video {}'.format(video_id))

    def subscriptions(self, channel_id): 
        items = []
        nextPageToken = ''
        while nextPageToken is not None:
            subscriptions_response = self.service.subscriptions().list(
                part='snippet',
                channelId=channel_id,
                pageToken=nextPageToken or None,
            ).execute()
            items += subscriptions_response['items']
            nextPageToken = subscriptions_response.get('nextPageToken')
        return items

    def playlist(self, playlist_id):
        items = []
        nextPageToken = ''
        while nextPageToken is not None:
            playlist_response = self.service.playlistItems().list(
                part='ContentDetails',
                playlistId=playlist_id,
                pageToken=nextPageToken or None,
            ).execute()
            nextPageToken = playlist_response.get('nextPageToken')

            # Convert response to a list of videos
            playlist_videos = []
            for playlist_item in playlist_response['items']:
                video_id = playlist_item['contentDetails']['videoId']
                try:
                    video_resp = self.video(video_id)
                    playlist_videos.append(video_resp)
                except ValueError:
                    pass

            items += playlist_videos
            
        return items

    def playlist_ids(self, playlist_id):
        items = []
        nextPageToken = ''
        while nextPageToken is not None:
            playlist_response = self.service.playlistItems().list(
                part='ContentDetails',
                playlistId=playlist_id,
                pageToken=nextPageToken or None,
            ).execute()
            nextPageToken = playlist_response.get('nextPageToken')

            # Convert response to a list of videos
            playlist_video_ids = []
            for playlist_item in playlist_response['items']:
                video_id = playlist_item['contentDetails']['videoId']
                playlist_video_ids.append(video_id)
                
            items += playlist_video_ids
            
        return items