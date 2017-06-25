# QMP API

An API for the Q Media Project


## SETUP
	- `pip install -r requirements.txt`
	- In qmp_api create file `secrets.py` and populate with API KEY for YOUTUBE_DATA_API

##  RUNNING
	- `invoke create_db`
	- `invoke celery`
	- `invoke run`