from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db.models import Q

from django.conf import settings

from core.utils import redirect_after_login


def login(request):
    """ login the user """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login สำเร็จ")
            return redirect_after_login(request)

        # wrong credentials
        redirect_to = request.path
        if request.GET.get("next"):
            redirect_to += f"?next={request.GET.get('next')}"
        messages.error(request, "Email หรือ Password ผิด")
        return redirect(redirect_to)

    else:
        if request.user.is_authenticated:
            # user already login
            return redirect("index")
        return render(request, "core/login.html", {"next": request.GET.get("next")})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_exists = (
            get_user_model()
            .objects.filter(Q(username__iexact=username) | Q(email__iexact=email))
            .exists()
        )
        if user_exists:
            messages.error(request, "ไม่สามารถใช้ email หรือ username นี้ได้")
            return redirect("register")

        user = get_user_model().objects.create_user(
            username=username, email=email, password=password
        )
        auth.login(request, user)
        return redirect("index")

    else:
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, "core/register.html")


@require_POST
def logout(request):
    auth.logout(request)
    response = redirect("index")
    messages.success(request, "Logout สำเร็จ")
    return response