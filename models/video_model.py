from lib import utils

class VideoModel(object):
	def __init__(self, channel_id, title, description, image, pub_date, video_id):
		self.channel_id = channel_id
		self.title = title
		self.desc = description
		self.image = image 
		self.video_id = video_id
		self.pub_date = pub_date

	@classmethod
	def from_resp(cls, resp):
		channel_id = resp['channelId']
		title = resp['title']
		desc = resp['description']
		image = resp['thumbnails']['high']
		pub_date = utils.get_youtube_datetime(resp['publishedAt'])
		video_id = resp['resourceId']['videoId']
		return cls(channel_id, title, desc, image, pub_date, video_id)

	@classmethod
	def placeholder(cls):
		return cls('', '', '', '', utils.get_youtube_datetime("1970-01-01T12:00:00.000Z"), '')

	@property
	def dict(self):
		return {
			'channel_id': self.channel_id,
			'title': self.title,
			'desc': self.desc,
			'image': self.image,
			'video_id': self.video_id,
			'pub_date': self.pub_date,
		}