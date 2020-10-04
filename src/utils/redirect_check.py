from django.shortcuts import redirect
from django.utils.http import is_safe_url
from django.conf import settings


def redirect_after_login(request):
    nxt = request.GET.get("next", None)
    if nxt is None or not is_safe_url(
        nxt, {request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return redirect(nxt)