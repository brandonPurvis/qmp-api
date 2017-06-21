from flask import jsonify

from qmp_api import app, db
from qmp_api.models import Channel


@app.route('/channels')
def channels():
	channel_list = []
	for channel in Channel.query.all():
		channel_list.append({
			'channel_id': channel.id,
			'name': channel.name,
			'image': channel.image,
			'description': channel.description,
		})
	return(jsonify({'items': channel_list}))