from qmp_api import app, celery, db
from qmp_api.models import Channel
from ytapi import YoutubeAPI, YoutubeChannel, YoutubeVideo


@celery.on_after_configure.connect
def setup_periodic_task(sender, **kwargs):
	sender.add_periodic_task(3600, poll_channels.s(), name='Poll Channels')


@celery.task
def poll_channels():
	ytapi = YoutubeAPI(app.config["YOUTUBE_DATA_API"])
	subscriptions_response = ytapi.subscriptions(app.config["ROOT_CHANNEL_ID"])

	retreived_subs = map(YoutubeChannel.from_api_response, subscriptions_response)
	saved_subs = Channel.query.all()

	retreived_sub_ids = [c.channel_id for c in retreived_subs]
	saved_sub_ids = [channel.id for channel in saved_subs]

	new_subs = [c for c in retreived_subs if c.channel_id not in saved_sub_ids]
	old_subs = [c for c in saved_subs if c.id not in retreived_sub_ids]

	# Add Channels not current saved
	for new_sub in new_subs:
		sub = Channel.from_object(new_sub)
		db.session.add(sub)

	# Remove channels no longer in list
	for old_sub in old_subs:
		db.session.delete(old_sub)

	# Commit & close
	db.session.commit()