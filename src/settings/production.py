from .base import *

DEBUG = False

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# GOOGLE CLOUD STORAGE FOR MEDIA FILES
from google.oauth2 import service_account
GS_CREDENTIALS = None
if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        "credentials.json"
    )

DEFAULT_FILE_STORAGE = os.environ.get("DEFAULT_FILE_STORAGE")
GS_PROJECT_ID = os.environ.get("GS_PROJECT_ID")
GS_BUCKET_NAME = os.environ.get("GS_BUCKET_NAME")
MEDIA_URL = "https://storage.googleapis.com/{}/".format(GS_BUCKET_NAME)