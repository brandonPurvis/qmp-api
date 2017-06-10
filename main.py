import json
import youtube_api
from flask import Flask

app = Flask(__name__)
ROOT = 'UCjYn4RyjCCMJX67Rck4sq5A'


@app.route('/')
def get_root():
	root_channel = youtube_api.get_channel(ROOT)
	return json.dumps(root_channel.dict())

@app.route('/channels')
def get_channels():
	channels = youtube_api.get_channel_subscriptions(ROOT)
	return json.dumps(channels)

if __name__ == '__main__':
    app.run()