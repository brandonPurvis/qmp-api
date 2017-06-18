import os
import sqlite3
from celery import Celery
from flask import Flask

def connect_db(app):
	db = sqlite3.connect(app.config['DATABASE'])
	return db

def make_celery(app):
    celery = Celery(
    	app.import_name,
    	backend=app.config['CELERY_RESULT_BACKEND'],
    	broker=app.config['CELERY_BROKER_URL'],
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    YOUTUBE_DATA_API=os.environ['YOUTUBE_DATA_API'],
	DATABASE=os.path.join(app.root_path, '../qmp_api.db'),
	CELERY_BROKER_URL='pyamqp://guest@localhost//',
	CELERY_RESULT_BACKEND='',
	LIKE_PLAYLIST_ID='LLjYn4RyjCCMJX67Rck4sq5A',
	SPEC_CHANNEL_PLAYLIST_ID='PLa0DseGKotuAHBwFnxFEsU5qGL9F3fxe4',
	SPEC_VIDEO_PLAYLIST_ID='PLa0DseGKotuA_ciqFFvpYr7hBsv3z8LLl',
	ROOT_CHANNEL_ID='UCjYn4RyjCCMJX67Rck4sq5A',
))
app.config.from_envvar('QMP_SETTINGS', silent=True)
celery = make_celery(app)

from qmp_api import views
from qmp_api import celery_tasks