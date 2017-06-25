import os
import sqlite3
from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


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
app.config.from_object('qmp_api.settings')
app.config.from_object('qmp_api.secrets')

db = SQLAlchemy(app)
celery = make_celery(app)

from qmp_api import models
from qmp_api import views
from qmp_api import celery_tasks