from flask import jsonify

from qmp_api import app
from qmp_api import connect_db


@app.route('/channels')
def channels():
	db = connect_db(app)
	result = db.execute('SELECT * FROM channels;')
	results = result.fetchall()
	channel_list = []
	for result in results:
		channel_list.append({
			'channel_id': result[0],
			'name': result[1],
			'image': result[2],
			'description': result[3]
		})
	return(jsonify({'items': channel_list}))