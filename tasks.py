import sqlite3.dbapi2 as sqlite3
from invoke import task


@task
def reset_db(ctx):
	from qmp_api import app
	db = sqlite3.connect(app.config['DATABASE'])
	with open('schema.sql', 'r') as f:
		db.cursor().executescript(f.read())
	db.commit()
	db.close()

@task
def run(ctx):
	from qmp_api import app
	app.run(debug=True)

@task
def celery(ctx):
	ctx.run("celery worker --app=qmp_api.celery --loglevel=info -B")