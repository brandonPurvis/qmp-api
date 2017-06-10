from datetime import datetime


def get_youtube_datetime(string_datetime):
	return datetime.strptime(string_datetime, "%Y-%m-%dT%H:%M:%S.000Z")