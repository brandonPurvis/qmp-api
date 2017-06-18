from qmp_api import app, celery
from qmp_api import connect_db
from ytapi import YoutubeAPI, YoutubeChannel, YoutubeVideo


@celery.on_after_configure.connect
def setup_periodic_task(sender, **kwargs):
	 sender.add_periodic_task(3600, poll_channels.s(), name='Poll Channels')


@celery.task
def poll_channels():
	ytapi = YoutubeAPI(app.config["YOUTUBE_DATA_API"])
	db = connect_db(app)

	current_subs = map(YoutubeChannel.from_api_response, ytapi.subscriptions(app.config["ROOT_CHANNEL_ID"]))
	current_sub_ids = [c.channel_id for c in current_subs]
	saved_sub_ids = [c[0] for c in db.execute('SELECT id from channels;').fetchall()]

	new_channels = [c for c in current_subs if c.channel_id not in saved_sub_ids]
	old_ids = [c for c in saved_sub_ids if c not in current_sub_ids]

	# Add Channels not current saved
	for channel in new_channels:
		args = (channel.channel_id, channel.name, channel.image, channel.description)
		db.execute('INSERT INTO channels VALUES (?, ?, ?, ?);', args)

	# Remove channels no longer in list
	for channel_id in old_ids:
		args = (channel_id,)
		db.execute('DELETE FROM channels WHERE id=?', args)

	# Commit & close
	db.commit()
	db.close()
