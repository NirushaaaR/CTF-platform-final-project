from django.http.response import HttpResponseForbidden, HttpResponseServerError, JsonResponse
from django.conf import settings

from datetime import datetime, timedelta
import math
import jwt

def tiny_jwt(request):
    if not request.user.is_superuser:
        raise HttpResponseForbidden()

    payload = {
        "sub": str(request.user.pk),
        "name": request.user.username,
        "exp": math.floor((datetime.now() + timedelta(minutes=10)).timestamp()) # 10 minutes expiration
    }

    # When this is set the user will only be able to manage and see files in the specified root
    # directory. This makes it possible to have a dedicated home directory for each user.
    try:
        privateKey = ""
        with open(settings.BASE_DIR / "tiny_privatekey.pem") as f:
            privateKey = f.read()  
        token = jwt.encode(payload, privateKey,algorithm='RS256')
        return JsonResponse({ "token": token.decode('utf-8') })
    except Exception as e:
        print(e)
        return HttpResponseServerError("Failed generate jwt token.")