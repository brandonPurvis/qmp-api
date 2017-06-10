from apiclient.discovery import build


API_KEY = 'AIzaSyDPRG9co3-DkVg-ek58XZD3YSbkmCi08X0'
YOUTUBE = build('youtube', 'v3', developerKey=API_KEY)


class Channel(object):
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
        channel_id = resp['id']
        return cls(name, image, description, channel_id)

    def link(self):
        return 'http://www.youtube.com/channel/{}'.format(self.channel_id)

    def dict(self):
        return {
            'name': self.name,
            'image': self.image,
            'desc': self.description,
            'link': self.link(),
            'channel_id': self.channel_id,
        }

    def __str__(self):
        return "Channel {}".format(self.name)

    def __repr__(self):
        return '<Channel>{}</Channel>'.format(self.dict())


def get_channel(channel_id):
    search_response = YOUTUBE.channels().list(
        part='snippet',
        id=channel_id,
    ).execute()
    if not search_response.get('items'):
        return None
    return Channel.from_api_response(search_response['items'][0])


def get_channel_videos(channel_id):
    channel_resources = YOUTUBE.channels().list(
        part='ContentDetails',
        id=channel_id
    ).execute()
    uploads_playlist_id = channel_resources['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos = YOUTUBE.playlistItems().list(
        playlistId=uploads_playlist_id,
        part="snippet",
    ).execute()
    return videos['items']


def get_channel_subscriptions(channel_id, pageToken=None):
    subscriptions = YOUTUBE.subscriptions().list(
        part='snippet',
        channelId=channel_id,
        maxResults=10,
        pageToken=pageToken,
    ).execute()
    items = map(lambda x: Channel.from_api_response(x).dict(), subscriptions['items'])
    nextPageToken = subscriptions.get('nextPageToken')
    if nextPageToken:
        next_items = get_channel_subscriptions(channel_id, pageToken=nextPageToken)
        items += next_items
    return items
