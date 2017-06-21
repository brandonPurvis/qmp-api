from invoke import task

@task
def create_db(ctx):
	from qmp_api import db
	db.create_all()

@task
def run(ctx):
	from qmp_api import app
	app.run(debug=True)

@task
def celery(ctx):
	ctx.run("celery worker --app=qmp_api.celery --loglevel=info -B")