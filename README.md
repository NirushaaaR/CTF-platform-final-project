# CTF PLATFORM DJANGO

## FIRST
cd src/ and
start copy file .env.example to .env and change it to proper environment variable
```
DEBUG=on
SECRET_KEY=some-key-here
ALLOWED_HOSTS=

# DATABASE CONFIG
DB_HOST=<WHERE IS THE DATABASE>
DB_PORT=<DATABASE PORT>
POSTGRES_DB=<DATABASE NAME>
POSTGRES_USER=<DATABASE USER>
POSTGRES_PASSWORD=<DATABASE PASSWORD>

# GOOGLE CLOUD BUCKET for media file in production
DEFAULT_FILE_STORAGE=storages.backends.gcloud.GoogleCloudStorage
GS_PROJECT_ID=<GOOGLE_CLOUD_BUCKET_PROJECT_ID>
GS_BUCKET_NAME=<NAME_OF_BUCKET>
```

install all dependencies in requirements.txt
``` bash
pip install -r requirements.txt
```

next migrate the database with command
``` bash
python manage.py migrate
```

***
## START RUNNING SERVER
``` bash
python manage.py runserver --settings=settings.local
```
server now should run on http://localhost:8000

## RUN WITH DOCKER
```
docker-compose up
```

***
## Deployment
currently the project is set to deploy to google cloud App Engine standard environment https://cloud.google.com/python/django/appengine
you will also need to set **google cloud bucket** and put credentials.json inside the src/ to handle media file upload

website >> https://ctf-platform-cloud-bucket.et.r.appspot.com/


