from .base import *

DEBUG = False

# Channels
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [(os.environ.get("REDIS_HOST"), os.environ.get("REDIS_PORT"))],
#         },
#     },
# }

# django security
# for https only
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True 