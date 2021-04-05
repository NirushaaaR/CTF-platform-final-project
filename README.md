# CTF PLATFORM DJANGO

## Requirements

1) [python](https://www.python.org/downloads/) 3.8

## Installation

1) เข้าไปที่โฟร์เดอร์ src/
``` bash
cd src/
```
2) copy ไฟล์ .env.example เป็น .env แล้วเปลี่ยนตัวแปร
```
DEBUG=on
SECRET_KEY=คียร์ไรก็ได้แต่ต้องเก็บเป็นความลับ
ALLOWED_HOSTS=*

# DATABASE CONFIG
DB_HOST=โฮส์ของ database เช่น localhost 127.0.0.1
DB_PORT=PORT ที่รัน Database อยู่ (default postgres 5432)
POSTGRES_DB=ชื่อของ database ที่จะใช้เก็บข้อมูล
POSTGRES_USER=ชื่อผู้ใช้ของ database (postgres)
POSTGRES_PASSWORD=password ของใช้นั้น (postgres)

# GOOGLE CLOUD BUCKET สำหรับจัดการกับ media ไฟล์ตอน production
DEFAULT_FILE_STORAGE=storages.backends.gcloud.GoogleCloudStorage
GS_PROJECT_ID=โปรเจค ID ของ Google cloud bucket ที่ได้สร้างไว้
GS_BUCKET_NAME=ชื่อของ bucket ที่ได้สร้างไว้
```

3) install dependencies จากใน requirements.txt
``` bash
pip install -r requirements.txt
```

4) migrate ข้อมูลใส่ database ด้วยคำสั่ง
``` bash
python manage.py migrate
```

5) รัน server สำหรับ developement
``` bash
python manage.py runserver --settings=settings.local
```
server จะรันอยู่ที่ http://localhost:8000

หรือรันด้วย docker-compose 
``` bash
docker-compose up
```

***
## Development

1) ส่วน Tutorial จะอยู่ใน src/core/ แยกเป็น Room ต่าง ๆ แทน tutorial
2) ส่วน Game จะอยู่ใน src/game/ 
3) ส่วนจัดการ deploy docker image จะเป็น javascript ไฟล์ใน src/app/static/js/manageDocker.js และใน src/docker_instance

***
## Deployment

ตอนนี้ระบบทำการ deploy บน google cloud App Engine standard environment >> https://ctf-platform-cloud-bucket.et.r.appspot.com/

ขั้นตอนการ deploy ทำตาม https://cloud.google.com/python/django/appengine

ทำการติดตั้ง **google cloud bucket** สำหรับจัดการ media file ต่าง ๆ ที่จะถูกอัพโหลดขึ้นไปและเอา credentials.json ของโปรเจคที่เป็นเจ้าของ bucket นี้ไปใส่ไว้ใน src/ ด้วย



